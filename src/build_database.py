"""
Load the raw Kaggle CSV files into a single DuckDB database.

Why DuckDB? The weather tables are large. DuckDB lets us do the heavy joins and
aggregations in SQL, fast, on a laptop, and pull only the small results into pandas.

Usage (from the repo root):
    python src/build_database.py
"""
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
DB_PATH = ROOT / "data" / "processed" / "enefit.duckdb"

# Expected Kaggle files -> table names
TABLES = {
    "train.csv": "train",
    "client.csv": "client",
    "gas_prices.csv": "gas_prices",
    "electricity_prices.csv": "electricity_prices",
    "historical_weather.csv": "historical_weather",
    "forecast_weather.csv": "forecast_weather",
    "weather_station_to_county_mapping.csv": "weather_station_to_county_mapping",
}


def main() -> None:
    missing = [f for f in TABLES if not (RAW_DIR / f).exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing files in {RAW_DIR}: {missing}\n"
            "Download the competition data from Kaggle and unzip it into data/raw/."
        )

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))

    for file_name, table in TABLES.items():
        path = (RAW_DIR / file_name).as_posix()
        con.execute(
            f"CREATE OR REPLACE TABLE {table} AS "
            f"SELECT * FROM read_csv_auto('{path}', header=true)"
        )
        n_rows = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        n_cols = len(con.execute(f"DESCRIBE {table}").fetchall())
        print(f"{table:<36} {n_rows:>12,} rows  {n_cols:>3} cols")

    con.close()
    print(f"\nDatabase written to {DB_PATH}")


if __name__ == "__main__":
    main()
