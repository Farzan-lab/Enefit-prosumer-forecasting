"""
Load the raw Kaggle CSV files into Azure SQL Database.

- Reads each CSV in chunks, so large weather files don't fill your RAM.
- Parses date/time columns. Timezone-aware columns are converted to UTC and stored
  without timezone (logged, so we can document it in the data dictionary).
- Bulk-inserts with pyodbc fast_executemany.

Usage (from the repo root, with .venv active):
    python src/load_to_azure.py                      # load all tables
    python src/load_to_azure.py --tables client gas_prices   # load selected tables
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import pandas as pd
from sqlalchemy.engine import Engine

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.db import get_engine, wait_until_awake  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
CHUNK_ROWS = 100_000

# CSV file -> (table name, date/time columns)
TABLES: dict[str, tuple[str, list[str]]] = {
    "weather_station_to_county_mapping.csv": ("weather_station_to_county_mapping", []),
    "client.csv": ("client", ["date"]),
    "gas_prices.csv": ("gas_prices", ["forecast_date", "origin_date"]),
    "electricity_prices.csv": ("electricity_prices", ["forecast_date", "origin_date"]),
    "train.csv": ("train", ["datetime"]),
    "historical_weather.csv": ("historical_weather", ["datetime"]),
    "forecast_weather.csv": ("forecast_weather", ["origin_datetime", "forecast_datetime"]),
}


def parse_dates(df: pd.DataFrame, cols: list[str], log: set[str]) -> pd.DataFrame:
    for col in cols:
        if col not in df.columns:
            continue
        values = df[col].astype("string")
        has_offset = values.str.contains(r"(?:[+-]\d{2}:?\d{2}|Z)$", regex=True, na=False).any()
        if has_offset:
            # e.g. "2021-09-01 00:00:00+03:00" -> convert everything to UTC, drop tz
            df[col] = pd.to_datetime(values, utc=True, errors="coerce").dt.tz_localize(None)
            log.add(col)
        else:
            df[col] = pd.to_datetime(values, errors="coerce")
    return df


def load_table(engine: Engine, csv_name: str, table: str, date_cols: list[str]) -> int:
    path = RAW_DIR / csv_name
    tz_converted: set[str] = set()
    total, start = 0, time.time()

    for i, chunk in enumerate(pd.read_csv(path, chunksize=CHUNK_ROWS)):
        chunk = parse_dates(chunk, date_cols, tz_converted)
        chunk.to_sql(
            table,
            engine,
            if_exists="replace" if i == 0 else "append",
            index=False,
            chunksize=10_000,
        )
        total += len(chunk)
        print(f"  {table:<36} {total:>12,} rows  ({time.time() - start:,.0f}s)", end="\r")

    print(f"  {table:<36} {total:>12,} rows  ({time.time() - start:,.0f}s)  ✅")
    if tz_converted:
        print(f"    ↳ timezone-aware columns converted to UTC: {sorted(tz_converted)}")
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Load Kaggle CSVs into Azure SQL.")
    parser.add_argument("--tables", nargs="*", help="Table names to load (default: all)")
    args = parser.parse_args()

    selected = {
        f: v for f, v in TABLES.items() if not args.tables or v[0] in args.tables
    }
    missing = [f for f in selected if not (RAW_DIR / f).exists()]
    if missing:
        raise FileNotFoundError(f"Missing files in {RAW_DIR}: {missing}")

    engine = get_engine()
    print("Connecting to Azure SQL...")
    wait_until_awake(engine)
    print("Loading tables (large weather tables can take a while)...\n")

    for csv_name, (table, date_cols) in selected.items():
        load_table(engine, csv_name, table, date_cols)

    print("\nDone. Next: run notebooks/01_data_overview.py")


if __name__ == "__main__":
    main()
