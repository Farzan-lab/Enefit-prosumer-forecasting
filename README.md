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
3. Run `python src/build_database.py`.

## Project Structure
```
├── data/
│   ├── raw/              # Kaggle CSVs (git-ignored)
│   └── processed/        # DuckDB database & derived tables (git-ignored)
├── docs/                 # Problem statement, methodology notes
├── notebooks/            # Analysis notebooks, numbered in order
├── sql/                  # SQL queries (data quality, feature tables)
├── src/                  # Reusable Python code
└── reports/figures/      # Charts used in README / article
```

## Approach
1. Problem definition → 2. Data loading & quality (SQL) → 3. EDA → 4. Baselines & model (time-based validation) → 5. Business cost translation → 6. Dashboard → 7. Write-up

## Results
_Coming soon._

## Tech Stack
Python (pandas, LightGBM, scikit-learn) · DuckDB / SQL · matplotlib / plotly

## Author
_Farzan Momayezi 
· [Linkedin](www.linkedin.com/in/farzan-momayezi) 
· [Email](Farzanmomayezi@gmail.com)_
