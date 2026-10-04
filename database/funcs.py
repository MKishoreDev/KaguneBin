from datetime import datetime, timezone
from typing import Optional

from database import get_conn

def insert_paste(
    *,
    paste_id: str,
    title: str,
    content: str,
    syntax: str,
    is_protected: bool,
    password: Optional[str],
    is_burn_after_read: bool,
    created_at: datetime,
    expires_at: Optional[datetime],
) -> dict:
    sql = """
        INSERT INTO pastes (
            id,
            title,
            content,
            syntax,
            is_protected,
            password,
            is_burn_after_read,
            created_at,
            expires_at
        )
        VALUES (
            %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s
        )
        RETURNING *;
    """

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            sql,
            (
                paste_id,
                title,
                content,
                syntax,
                is_protected,
                password,
                is_burn_after_read,
                created_at,
                expires_at,
            ),
        )
        return cur.fetchone()

def get_paste(paste_id: str) -> Optional[dict]:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM pastes WHERE id = %s;",
            (paste_id,),
        )
        return cur.fetchone()

def delete_paste(paste_id: str) -> bool:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "DELETE FROM pastes WHERE id = %s;",
            (paste_id,),
        )
        return cur.rowcount > 0

def increment_views(paste_id: str) -> Optional[dict]:
    sql = """
        UPDATE pastes
        SET views = views + 1
        WHERE id = %s
        RETURNING *;
    """

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (paste_id,))
        return cur.fetchone()

def increment_downloads(paste_id: str) -> Optional[dict]:
    sql = """
        UPDATE pastes
        SET downloads = downloads + 1
        WHERE id = %s
        RETURNING *;
    """

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (paste_id,))
        return cur.fetchone()

def list_pastes(limit: int = 50, offset: int = 0) -> list[dict]:
    sql = """
        SELECT * FROM pastes
        WHERE (expires_at IS NULL OR expires_at > NOW())
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s;
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (limit, offset))
        return cur.fetchall()

def cleanup_expired_pastes() -> int:
    sql = """
        DELETE FROM pastes
        WHERE expires_at IS NOT NULL AND expires_at <= NOW();
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql)
        return cur.rowcount
