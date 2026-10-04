import os
from contextlib import contextmanager
import psycopg
from psycopg.rows import dict_row

from config import DATABASE_URI

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS pastes (
    id                  TEXT        PRIMARY KEY,
    title               TEXT        NOT NULL DEFAULT '',
    content             TEXT        NOT NULL,
    syntax              TEXT        NOT NULL DEFAULT 'text',

    is_protected        BOOLEAN     NOT NULL DEFAULT FALSE,
    password            TEXT,
    is_burn_after_read  BOOLEAN     NOT NULL DEFAULT FALSE,

    views               INTEGER     NOT NULL DEFAULT 0,
    downloads           INTEGER     NOT NULL DEFAULT 0,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at          TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_pastes_expires_at ON pastes (expires_at);
CREATE INDEX IF NOT EXISTS idx_pastes_created_at ON pastes (created_at DESC);
"""

@contextmanager
def get_conn():
    if not DATABASE_URI:
        raise ConnectionError("DATABASE_URI environment variable is not configured.")
    
    conn = psycopg.connect(DATABASE_URI, row_factory=dict_row)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def start_db():
    if not DATABASE_URI:
        print("[WARN] DATABASE_URI not configured. Skipping start_db().")
        return
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(SCHEMA_SQL)