from contextlib import asynccontextmanager
from datetime import datetime, timezone
from uuid import uuid4
import hashlib
import base64

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    PlainTextResponse,
    StreamingResponse,
)
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext

from models import PasteCreate, PasteResponse
from config import DATABASE_URI

from database import start_db
from database.funcs import (
    insert_paste,
    get_paste as db_get_paste,
    delete_paste as db_delete_paste,
    increment_views,
    increment_downloads,
    list_pastes,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        start_db()
    except Exception as e:
        print(f"Error initializing database: {e}", datetime)

    yield

app = FastAPI(
    title="KaguneBin",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

def hash_password_for_bcrypt(password: str) -> str:
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest).decode("utf-8")

def build_expires_at(paste: PasteCreate) -> datetime | None:
    if not paste.is_expiry:
        return None

    if (
        paste.expiry_date is None
        or paste.expiry_hour is None
        or paste.expiry_minute is None
    ):
        raise HTTPException(
            status_code=400,
            detail="Expiry fields are missing",
        )

    try:
        expiry_datetime = datetime(
            year=paste.expiry_date.year,
            month=paste.expiry_date.month,
            day=paste.expiry_date.day,
            hour=paste.expiry_hour,
            minute=paste.expiry_minute,
            second=0,
            microsecond=0,
            tzinfo=timezone.utc,
        )

        now = datetime.now(timezone.utc)
        if expiry_datetime <= now:
            raise HTTPException(
                status_code=400,
                detail="Expiry time must be in the future",
            )

        return expiry_datetime

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

def is_expired(data: dict) -> bool:
    expires_at = data.get("expires_at")
    if expires_at is None:
        return False
    now = datetime.now(timezone.utc)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return now >= expires_at

def row_to_response(data: dict) -> dict:
    created_at = data["created_at"]
    expires_at = data["expires_at"]

    created_at_str = (
        created_at.isoformat()
        if hasattr(created_at, "isoformat")
        else created_at
    )

    expires_at_str = (
        expires_at.isoformat()
        if hasattr(expires_at, "isoformat")
        else expires_at
    ) if expires_at else None

    return {
        "id": data["id"],
        "title": data["title"],
        "content": data["content"],
        "syntax": data["syntax"],
        "url": f"/p/{data['id']}",
        "is_protected": data["is_protected"],
        "is_burn_after_read": data["is_burn_after_read"],
        "views": data["views"],
        "downloads": data["downloads"],
        "created_at": created_at_str,
        "expires_at": expires_at_str,
        "security": {
            "is_protected": data["is_protected"],
            "is_burn_after_read": data["is_burn_after_read"],
        },
        "stats": {
            "views": data["views"],
            "downloads": data["downloads"],
        },
        "timestamps": {
            "created_at": created_at_str,
            "expires_at": expires_at_str,
        },
    }

def validate_password(data: dict, password: str | None):
    if not data["is_protected"]:
        return

    if not password:
        raise HTTPException(
            status_code=401,
            detail="Password required",
        )

    if not pwd_context.verify(hash_password_for_bcrypt(password), data["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid password",
        )

@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("templates/index.html")

@app.get("/p/{paste_id}", response_class=HTMLResponse)
def paste_page_routed(paste_id: str):
    return FileResponse("templates/paste.html")

@app.get("/status")
def health():
    return {
        "status": "ok",
        "service": "KaguneBin",
    }

@app.post("/paste", response_model=PasteResponse)
def create_paste(paste: PasteCreate):
    try:
        paste_id = f"kgn_{uuid4().hex[:8]}"
        expires_at = build_expires_at(paste)
        hashed_password = (
            pwd_context.hash(hash_password_for_bcrypt(paste.password))
            if paste.password
            else None
        )
        print("Creating paste...")
        print("Paste ID:", paste_id)

        data = insert_paste(
            paste_id=paste_id,
            title=paste.title,
            content=paste.content,
            syntax=paste.syntax,
            is_protected=paste.is_protected,
            password=hashed_password,
            is_burn_after_read=paste.is_burn_after_read,
            created_at=datetime.now(timezone.utc),
            expires_at=expires_at,
        )
        print("Insert success:", data)
        return row_to_response(data)
    except Exception as e:
        print("ERROR IN /paste:", str(e))
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

@app.get("/api/paste/{paste_id}", response_model=PasteResponse)
def fetch_paste(paste_id: str, password: str | None = Query(default=None),):
    data = db_get_paste(paste_id)
    if not data:
        raise HTTPException(
            status_code=404,
            detail="Paste not found",
        )
    if is_expired(data):
        db_delete_paste(paste_id)

        raise HTTPException(
            status_code=410,
            detail="Paste expired",
        )

    validate_password(data, password)
    data = increment_views(paste_id)
    response = row_to_response(data)

    if data["is_burn_after_read"]:
        db_delete_paste(paste_id)

    return response

@app.get("/raw/{paste_id}", response_class=PlainTextResponse)
def get_raw(paste_id: str, password: str | None = Query(default=None),):
    data = db_get_paste(paste_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Paste not found",
        )

    if is_expired(data):
        db_delete_paste(paste_id)

        raise HTTPException(
            status_code=410,
            detail="Paste expired",
        )

    validate_password(data, password)
    content = data["content"]
    increment_views(paste_id)
    if data["is_burn_after_read"]:
        db_delete_paste(paste_id)

    return content

def get_file_extension(syntax: str) -> str:
    """Map syntax language to file extension"""
    ext_map = {
        "python": "py",
        "javascript": "js",
        "typescript": "ts",
        "java": "java",
        "cpp": "cpp",
        "c": "c",
        "csharp": "cs",
        "go": "go",
        "rust": "rs",
        "php": "php",
        "ruby": "rb",
        "swift": "swift",
        "kotlin": "kt",
        "html": "html",
        "css": "css",
        "scss": "scss",
        "json": "json",
        "xml": "xml",
        "yaml": "yaml",
        "sql": "sql",
        "bash": "sh",
        "shell": "sh",
        "text": "txt",
        "plaintext": "txt",
    }
    return ext_map.get(syntax.lower(), "txt")

@app.get("/download/{paste_id}")
def download_paste(paste_id: str, password: str | None = Query(default=None),):
    data = db_get_paste(paste_id)
    if not data:
        raise HTTPException(
            status_code=404,
            detail="Paste not found",
        )

    if is_expired(data):
        db_delete_paste(paste_id)

        raise HTTPException(
            status_code=410,
            detail="Paste expired",
        )

    validate_password(data, password)

    content = data["content"]
    syntax = data.get("syntax", "plaintext")
    title = data.get("title", paste_id)

    ext = get_file_extension(syntax)
    
    filename = f"{title}.{ext}" if ext != "txt" else f"{title}.txt"

    increment_views(paste_id)
    increment_downloads(paste_id)

    if data["is_burn_after_read"]:
        db_delete_paste(paste_id)
        
    return StreamingResponse(
        iter([content]),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return FileResponse(
        "templates/404.html",
        status_code=404,
    )
