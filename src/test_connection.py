"""
Quick check that Python can reach the Azure SQL database.

Usage (from the repo root, with .venv active):
    python src/test_connection.py
"""
import sys
import time
from pathlib import Path

from sqlalchemy import text

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.db import get_engine, wait_until_awake  # noqa: E402


def main() -> None:
    print("Connecting... (a paused serverless database can take up to ~1 minute to wake up)")
    start = time.time()
    engine = get_engine()
    wait_until_awake(engine)
    with engine.connect() as conn:
        version = conn.execute(text("SELECT @@VERSION")).scalar()
        db_name = conn.execute(text("SELECT DB_NAME()")).scalar()
    print(f"✅ Connected to '{db_name}' in {time.time() - start:.1f}s")
    print(version.splitlines()[0])


if __name__ == "__main__":
    main()
