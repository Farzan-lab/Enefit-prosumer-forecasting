-- =====================================================================
-- 01_first_look.sql: first data-quality and structure checks
-- Run from notebooks/01_data_overview.py, or in the DuckDB CLI:
--   duckdb data/processed/enefit.duckdb < sql/01_first_look.sql
-- =====================================================================

-- Q1. Time coverage of the target table
SELECT MIN(datetime) AS first_hour,
       MAX(datetime) AS last_hour,
       COUNT(DISTINCT CAST(datetime AS DATE)) AS n_days,
       COUNT(DISTINCT prediction_unit_id)     AS n_prediction_units
FROM train;

-- Q2. Missing targets: how many, and where?
SELECT is_consumption,
       COUNT(*)                                   AS n_rows,
       COUNT_IF(target IS NULL)                   AS n_missing_target,
       ROUND(100.0 * COUNT_IF(target IS NULL) / COUNT(*), 3) AS pct_missing
FROM train
GROUP BY is_consumption;

-- Q3. Volume by segment: who produces and consumes the most?
SELECT is_business,
       product_type,
       is_consumption,
       ROUND(SUM(target) / 1e6, 1) AS total_gwh,
       COUNT(DISTINCT county)      AS n_counties
FROM train
GROUP BY ALL
ORDER BY is_consumption, total_gwh DESC;

-- Q4. Data-availability check: how far behind the target date is each table?
--     (key for avoiding leakage: what was known at forecast time?)
SELECT 'train'  AS tbl, MIN(data_block_id) AS min_block, MAX(data_block_id) AS max_block FROM train
UNION ALL
SELECT 'client', MIN(data_block_id), MAX(data_block_id) FROM client
UNION ALL
SELECT 'forecast_weather', MIN(data_block_id), MAX(data_block_id) FROM forecast_weather
UNION ALL
SELECT 'electricity_prices', MIN(data_block_id), MAX(data_block_id) FROM electricity_prices;

-- Q5. Do weather stations map cleanly to counties? (NULL county = station outside any county)
SELECT county IS NULL AS unmapped, COUNT(*) AS n_stations
FROM weather_station_to_county_mapping
GROUP BY 1;
