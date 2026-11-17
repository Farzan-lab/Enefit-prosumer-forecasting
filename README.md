# Forecasting Prosumer Energy Behaviour ☀️⚡

**Can better forecasts of rooftop-solar customers cut an energy retailer's balancing costs?**

> 🚧 Work in progress. Findings will be added as the project develops.

## Executive Summary
_To be written at the end: 3–4 key findings in plain language + the business impact in €._

## The Problem
Energy retailers must forecast, hour by hour, how much electricity their **prosumers** (customers with solar panels) will use and produce. Forecast errors are paid for as **imbalance costs**. See the full brief: [`docs/01_problem_statement.md`](docs/01_problem_statement.md).

## Data
[Enefit – Predict Energy Behavior of Prosumers](https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers) (Kaggle). Hourly production/consumption for Estonian prosumers, with weather, client and price data.

Data is **not** included in this repo. To reproduce:
1. Accept the competition rules on Kaggle and download the data.
2. Unzip the CSV files into `data/raw/`.
3. Create an Azure SQL Database (the free offer is enough), install **ODBC Driver 18 for SQL Server**, then copy `.env.example` to `.env` and fill in your connection details.
4. `pip install -r requirements.txt`
5. `python src/test_connection.py`, then `python src/load_to_azure.py`

*No cloud account?* `python src/build_database.py` builds a local DuckDB copy instead (queries in `sql/duckdb/`).

## Architecture
```
Kaggle CSVs ──► Python (pandas, chunked) ──► Azure SQL Database ──► SQL feature views
                                                     │
                                   ┌─────────────────┴─────────────────┐
                                   ▼                                   ▼
                        Python (SQLAlchemy/pyodbc)              Power BI dashboard
                        EDA · LightGBM · SHAP                   (aggregated data)
```

## Project Structure
```
├── data/
│   ├── raw/              # Kaggle CSVs (git-ignored)
│   └── processed/        # optional local DuckDB copy (git-ignored)
├── docs/                 # Problem statement, methodology notes
├── notebooks/            # Analysis notebooks, numbered in order
├── sql/                  # T-SQL queries for Azure SQL (sql/duckdb/ = local version)
├── src/                  # Reusable Python code
└── reports/figures/      # Charts used in README / article
```

## Approach
1. Problem definition → 2. Data loading & quality (SQL) → 3. EDA → 4. Baselines & model (time-based validation) → 5. Business cost translation → 6. Dashboard → 7. Write-up

## Results
_Coming soon._

## Tech Stack
Python (pandas, SQLAlchemy, pyodbc, LightGBM, scikit-learn) · Azure SQL Database (T-SQL) · Power BI · DuckDB (local fallback) · matplotlib / plotly

## Data Licence & Disclaimer
Data: **Eesti Energia AS / Kaggle**, licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) and the competition rules. **No competition data is redistributed in this repository.**
Code is MIT-licensed. Figures and aggregated results are CC BY-NC-SA 4.0. Details: [`docs/DATA_LICENSE.md`](docs/DATA_LICENSE.md).

This is an independent, non-commercial portfolio project. It is not affiliated with or endorsed by Eesti Energia AS, Enefit or Kaggle.

## Author
_Your name · LinkedIn · email_
