"""
Database connection helper for Azure SQL Database.

Credentials are read from a local `.env` file (never committed to git).
Copy `.env.example` to `.env` and fill in your own values.

Usage:
    from src.db import get_engine
    engine = get_engine()

Quick connection test (from the repo root):
    python src/test_connection.py
"""
from __future__ import annotations

import os
import time
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, Engine
from sqlalchemy.exc import OperationalError

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

ODBC_DRIVER = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing environment variable {name}. "
            "Copy .env.example to .env and fill in your Azure SQL details."
        )
    return value


def get_engine(echo: bool = False) -> Engine:
    """Create a SQLAlchemy engine for the Azure SQL database."""
    url = URL.create(
        "mssql+pyodbc",
        username=_require("AZURE_SQL_USER"),
        password=_require("AZURE_SQL_PASSWORD"),  # special characters are escaped safely
        host=_require("AZURE_SQL_SERVER"),
        port=1433,
        database=_require("AZURE_SQL_DATABASE"),
        query={
            "driver": ODBC_DRIVER,
            "Encrypt": "yes",
            "TrustServerCertificate": "no",
            "Connection Timeout": "60",
        },
    )
    # fast_executemany = much faster bulk inserts with pyodbc
    return create_engine(url, fast_executemany=True, pool_pre_ping=True, echo=echo)


def wait_until_awake(engine: Engine, retries: int = 6, delay_s: int = 20) -> None:
    """
    Serverless Azure SQL pauses itself when idle. The first connection after a pause
    can fail while the database resumes (often error 40613). Retry a few times.
    """
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as con:
                con.execute(text("SELECT 1"))
            return
        except OperationalError as exc:
            if attempt == retries:
                raise
            print(f"  Database not ready (attempt {attempt}/{retries}), "
                  f"probably resuming from auto-pause. Retrying in {delay_s}s...")
            print(f"  ({str(exc.orig)[:120]}...)")
            time.sleep(delay_s)
