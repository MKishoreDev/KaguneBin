import os
import psycopg

from contextlib import contextmanager

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
"""

@contextmanager
def get_conn():
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
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(SCHEMA_SQL)