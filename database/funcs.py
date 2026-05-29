from datetime import datetime
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

def increment_views(paste_id: str) -> dict:
    sql = """
        UPDATE pastes
        SET views = views + 1
        WHERE id = %s
        RETURNING *;
    """

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (paste_id,))

        return cur.fetchone()

def increment_downloads(paste_id: str) -> dict:
    sql = """
        UPDATE pastes
        SET downloads = downloads + 1
        WHERE id = %s
        RETURNING *;
    """

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (paste_id,))

        return cur.fetchone()

def list_pastes() -> list[dict]:
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM pastes ORDER BY created_at DESC;"
        )

        return cur.fetchall()
