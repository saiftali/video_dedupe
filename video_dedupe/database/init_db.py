import os
from dotenv import load_dotenv
import psycopg2

# load .env into os.environ
load_dotenv()

def init_db():
    # pull all creds from environment
    conn = psycopg2.connect(
        host     = os.getenv("PGHOST"),
        port     = os.getenv("PGPORT"),
        user     = os.getenv("PGUSER"),
        password = os.getenv("PGPASSWORD"),
        dbname   = os.getenv("PGDATABASE"),
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    path TEXT PRIMARY KEY,
                    mtime DOUBLE PRECISION,
                    fp_hash TEXT,
                    full_hash TEXT,
                    dedupe_stage TEXT
                );
            """)
    print("✅ Schema initialized.")
    conn.close()

if __name__ == "__main__":
    init_db()
