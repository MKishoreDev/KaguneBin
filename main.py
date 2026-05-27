from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from uuid import uuid4
from passlib.context import CryptContext

from models import PasteCreate, PasteResponse

from database import start_db
from database.funcs import (
    insert_paste,
    get_paste as db_get_paste,
    delete_paste as db_delete_paste,
    increment_views,
    list_pastes,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        start_db()
    except Exception as e:
        print(f"Error initializing database: {e}")
    yield

app = FastAPI(
    title="KaguneBin",
    lifespan=lifespan
)

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
            detail="is_expiry is true but expiry fields missing",
        )

    try:
        return datetime(
            year=paste.expiry_date.year,
            month=paste.expiry_date.month,
            day=paste.expiry_date.day,
            hour=paste.expiry_hour,
            minute=paste.expiry_minute,
            tzinfo=timezone.utc,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def is_expired(data: dict) -> bool:
    exp = data.get("expires_at")
    if exp is None:
        return False
    return datetime.now(timezone.utc) >= exp

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
        "url": data["id"],
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

@app.get("/")
def root():
    return {"message": "Welcome to KaguneBin API!"}

@app.post("/paste", response_model=PasteResponse)
def create_paste(paste: PasteCreate):
    paste_id = f"kgn_{uuid4().hex[:8]}"
    expires_at = build_expires_at(paste)
    hashed_password = pwd_context.hash(paste.password) if paste.password else None
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
    return row_to_response(data)

@app.get("/p/{paste_id}", response_model=PasteResponse)
def fetch_paste(paste_id: str, password: str | None = Query(default=None)):
    data = db_get_paste(paste_id)
    if not data:
        raise HTTPException(404, "Paste not found")

    if is_expired(data):
        db_delete_paste(paste_id)
        raise HTTPException(410, "Paste expired")

    if data["is_protected"] and not pwd_context.verify(password or "", data["password"]):
        raise HTTPException(401, "Invalid password")

    data = increment_views(paste_id)
    if data["is_burn_after_read"]:
        response = row_to_response(data)
        db_delete_paste(paste_id)
        return response

    return row_to_response(data)

@app.get("/raw/{paste_id}", response_class=PlainTextResponse)
def get_raw(paste_id: str, password: str | None = Query(default=None)):
    data = db_get_paste(paste_id)
    if not data:
        raise HTTPException(404, "Paste not found")

    if is_expired(data):
        db_delete_paste(paste_id)
        raise HTTPException(410, "Paste expired")

    if data["is_protected"] and not pwd_context.verify(password or "", data["password"]):
        raise HTTPException(401, "Invalid password")

    content = data["content"]
    increment_views(paste_id)
    if data["is_burn_after_read"]:
        db_delete_paste(paste_id)

    return content

@app.delete("/delete/{paste_id}")
def remove_paste(paste_id: str):
    deleted = db_delete_paste(paste_id)
    if not deleted:
        raise HTTPException(404, "Paste not found")
    return {
        "success": True,
        "message": "Paste deleted successfully"
    }

@app.get("/pastes")
def get_all_pastes():
    rows = list_pastes()
    return {
        "count": len(rows),
        "pastes": [row_to_response(r) for r in rows]
    }