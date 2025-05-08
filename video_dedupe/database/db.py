import psycopg2
from psycopg2.extras import execute_values
from video_dedupe.config import DB_URL

# SQL for creating the files table
SCHEMA = """
CREATE TABLE IF NOT EXISTS files (
    path TEXT PRIMARY KEY,
    mtime DOUBLE PRECISION,
    fp_hash TEXT,
    full_hash TEXT,
    dedupe_stage TEXT
);
"""

def get_conn():
    """Open a new database connection using the URL from config."""
    return psycopg2.connect(DB_URL)


def init_db():
    """Initialize the database schema by creating the `files` table."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(SCHEMA)
    print("✅ Schema initialized.")


def upsert_files(records):
    """Upsert RECORDS into the `files` table."""
    sql = """
    INSERT INTO files(path, mtime, fp_hash, full_hash, dedupe_stage)
    VALUES %s
    ON CONFLICT (path) DO UPDATE
      SET mtime = EXCLUDED.mtime,
          fp_hash = EXCLUDED.fp_hash,
          full_hash = EXCLUDED.full_hash,
          dedupe_stage = EXCLUDED.dedupe_stage;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            execute_values(cur, sql, records, page_size=100)
            conn.commit()
    print("✅ Files upserted.")