from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from uuid import uuid4
import hashlib
import base64
import bcrypt

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    PlainTextResponse,
    StreamingResponse,
    JSONResponse,
)
from fastapi.staticfiles import StaticFiles

from models import PasteCreate, PasteResponse
from config import DATABASE_URI, BASE_URL

from database import start_db
from database.funcs import (
    insert_paste,
    get_paste as db_get_paste,
    delete_paste as db_delete_paste,
    increment_views,
    increment_downloads,
    list_pastes,
    cleanup_expired_pastes,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        start_db()
        print(f"[KaguneBin] Database initialized at {datetime.now(timezone.utc).isoformat()}")
    except Exception as e:
        print(f"[KaguneBin] Error initializing database: {e}")
    yield

app = FastAPI(
    title="KaguneBin",
    description="Dark-themed, developer-focused pastebin API inspired by Tokyo Ghoul.",
    version="1.0.1",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Enable CORS for cross-origin frontend integrations & SDKs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

def _prepare_for_bcrypt(password: str) -> bytes:
    """SHA-256 → base64 → truncate to 72 bytes (bcrypt hard limit) → encode."""
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    b64 = base64.b64encode(digest).decode("utf-8")
    return b64[:72].encode("utf-8")


def hash_password(password: str) -> str:
    """Hash a password with bcrypt. Returns a str suitable for DB storage."""
    return bcrypt.hashpw(_prepare_for_bcrypt(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain password against the stored bcrypt hash."""
    return bcrypt.checkpw(_prepare_for_bcrypt(plain), hashed.encode("utf-8"))


def build_expires_at(paste: PasteCreate) -> datetime | None:
    if paste.expires_in_hours:
        return datetime.now(timezone.utc) + timedelta(hours=paste.expires_in_hours)

    if not paste.is_expiry:
        return None

    if (
        paste.expiry_date is None
        or paste.expiry_hour is None
        or paste.expiry_minute is None
    ):
        raise HTTPException(status_code=400, detail="Expiry fields (date, hour, minute) are required when is_expiry is True")

    try:
        tz_offset = timedelta(minutes=paste.tz_offset_minutes or 0)
        local_dt = datetime(
            year=paste.expiry_date.year,
            month=paste.expiry_date.month,
            day=paste.expiry_date.day,
            hour=paste.expiry_hour,
            minute=paste.expiry_minute,
            second=0,
            microsecond=0,
        )

        expiry_datetime = local_dt.replace(tzinfo=timezone.utc) - tz_offset

        if expiry_datetime <= datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Expiry time must be in the future")

        return expiry_datetime

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def is_expired(data: dict) -> bool:
    expires_at = data.get("expires_at")
    if expires_at is None:
        return False
    now = datetime.now(timezone.utc)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return now >= expires_at


def row_to_response(data: dict, request: Request | None = None) -> dict:
    created_at = data["created_at"]
    expires_at = data.get("expires_at")

    created_at_str = (
        created_at.isoformat() if hasattr(created_at, "isoformat") else str(created_at)
    )
    expires_at_str = (
        (expires_at.isoformat() if hasattr(expires_at, "isoformat") else str(expires_at))
        if expires_at
        else None
    )

    base = str(request.base_url).rstrip("/") if request else BASE_URL
    paste_path = f"/p/{data['id']}"

    return {
        "id": data["id"],
        "title": data.get("title", ""),
        "content": data.get("content", ""),
        "syntax": data.get("syntax", "plaintext"),
        "url": paste_path,
        "is_protected": data.get("is_protected", False),
        "is_burn_after_read": data.get("is_burn_after_read", False),
        "views": data.get("views", 0),
        "downloads": data.get("downloads", 0),
        "created_at": created_at_str,
        "expires_at": expires_at_str,
        "security": {
            "is_protected": data.get("is_protected", False),
            "is_burn_after_read": data.get("is_burn_after_read", False),
        },
        "stats": {
            "views": data.get("views", 0),
            "downloads": data.get("downloads", 0),
        },
        "timestamps": {
            "created_at": created_at_str,
            "expires_at": expires_at_str,
        },
    }


def validate_password(data: dict, password: str | None):
    if not data.get("is_protected"):
        return
    if not password:
        raise HTTPException(status_code=401, detail="Password required for protected paste")
    if not verify_password(password, data.get("password") or ""):
        raise HTTPException(status_code=401, detail="Invalid password")


@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("templates/index.html")

@app.get("/docs", response_class=HTMLResponse)
def docs():
    return FileResponse("templates/docs.html")

@app.get("/p/{paste_id}", response_class=HTMLResponse)
def paste_page_routed(paste_id: str):
    return FileResponse("templates/paste.html")


@app.get("/status")
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "KaguneBin",
        "version": "1.0.1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/paste", response_model=PasteResponse)
def create_paste(paste: PasteCreate, request: Request):
    try:
        paste_id = f"kgn_{uuid4().hex[:8]}"
        expires_at = build_expires_at(paste)
        
        effective_pwd = paste.effective_password
        hashed_password = hash_password(effective_pwd) if effective_pwd else None

        data = insert_paste(
            paste_id=paste_id,
            title=paste.title.strip(),
            content=paste.content,
            syntax=paste.syntax.lower().strip() or "plaintext",
            is_protected=paste.is_protected,
            password=hashed_password,
            is_burn_after_read=paste.burn_after_read,
            created_at=datetime.now(timezone.utc),
            expires_at=expires_at,
        )
        return row_to_response(data, request)
    except HTTPException:
        raise
    except Exception as e:
        print("[KaguneBin] ERROR in /paste:", str(e))
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/paste/{paste_id}", response_model=PasteResponse)
def fetch_paste(paste_id: str, request: Request, password: str | None = Query(default=None)):
    data = db_get_paste(paste_id)
    if not data:
        raise HTTPException(status_code=404, detail="Paste not found")
    if is_expired(data):
        db_delete_paste(paste_id)
        raise HTTPException(status_code=410, detail="Paste has expired and was removed")

    validate_password(data, password)
    data = increment_views(paste_id) or data
    response = row_to_response(data, request)

    if data.get("is_burn_after_read"):
        db_delete_paste(paste_id)

    return response


@app.get("/raw/{paste_id}", response_class=PlainTextResponse)
def get_raw(paste_id: str, password: str | None = Query(default=None)):
    data = db_get_paste(paste_id)
    if not data:
        raise HTTPException(status_code=404, detail="Paste not found")
    if is_expired(data):
        db_delete_paste(paste_id)
        raise HTTPException(status_code=410, detail="Paste has expired and was removed")

    validate_password(data, password)
    content = data.get("content", "")
    increment_views(paste_id)
    if data.get("is_burn_after_read"):
        db_delete_paste(paste_id)
    return content


def get_file_extension(syntax: str) -> str:
    ext_map = {
        "python": "py", "javascript": "js", "typescript": "ts",
        "java": "java", "cpp": "cpp", "c": "c", "csharp": "cs",
        "go": "go", "rust": "rs", "php": "php", "ruby": "rb",
        "swift": "swift", "kotlin": "kt", "html": "html", "css": "css",
        "scss": "scss", "json": "json", "xml": "xml", "yaml": "yaml",
        "sql": "sql", "bash": "sh", "shell": "sh", "text": "txt", "plaintext": "txt",
        "markdown": "md", "dockerfile": "dockerfile",
    }
    return ext_map.get(syntax.lower(), "txt")


@app.get("/download/{paste_id}")
def download_paste(paste_id: str, password: str | None = Query(default=None)):
    data = db_get_paste(paste_id)
    if not data:
        raise HTTPException(status_code=404, detail="Paste not found")
    if is_expired(data):
        db_delete_paste(paste_id)
        raise HTTPException(status_code=410, detail="Paste has expired and was removed")

    validate_password(data, password)
    content = data.get("content", "")
    syntax = data.get("syntax", "plaintext")
    title = data.get("title") or paste_id
    ext = get_file_extension(syntax)
    
    # Sanitize title for filename
    safe_title = "".join(c for c in title if c.isalnum() or c in ("-", "_", " ")).strip() or paste_id
    filename = f"{safe_title}.{ext}"

    increment_views(paste_id)
    increment_downloads(paste_id)

    if data.get("is_burn_after_read"):
        db_delete_paste(paste_id)

    return StreamingResponse(
        iter([content]),
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    return FileResponse("templates/404.html", status_code=404)
