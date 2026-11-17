-- =====================================================================
-- 01_first_look.sql: first data-quality and structure checks (T-SQL / Azure SQL)
-- Run from notebooks/01_data_overview.py, or paste into the Azure portal
-- Query editor / the VS Code MSSQL extension.
-- (DuckDB version of these queries: sql/duckdb/01_first_look.sql)
-- =====================================================================

-- Q1. Time coverage of the target table
SELECT MIN([datetime])                          AS first_hour,
       MAX([datetime])                          AS last_hour,
       COUNT(DISTINCT CAST([datetime] AS DATE)) AS n_days,
       COUNT(DISTINCT prediction_unit_id)       AS n_prediction_units
FROM dbo.train;

-- Q2. Missing targets: how many, and where?
SELECT is_consumption,
       COUNT(*)                                              AS n_rows,
       SUM(CASE WHEN target IS NULL THEN 1 ELSE 0 END)       AS n_missing_target,
       CAST(100.0 * SUM(CASE WHEN target IS NULL THEN 1 ELSE 0 END) / COUNT(*)
            AS DECIMAL(6, 3))                                AS pct_missing
FROM dbo.train
GROUP BY is_consumption;

-- Q3. Volume by segment: who produces and consumes the most?
SELECT is_business,
       product_type,
       is_consumption,
       CAST(SUM(target) / 1e6 AS DECIMAL(10, 1)) AS total_gwh,
       COUNT(DISTINCT county)                    AS n_counties
FROM dbo.train
GROUP BY is_business, product_type, is_consumption
ORDER BY is_consumption, total_gwh DESC;

-- Q4. Data-availability check: block ranges per table
--     (key for avoiding leakage: what was known at forecast time?)
SELECT 'train' AS tbl, MIN(data_block_id) AS min_block, MAX(data_block_id) AS max_block FROM dbo.train
UNION ALL
SELECT 'client', MIN(data_block_id), MAX(data_block_id) FROM dbo.client
UNION ALL
SELECT 'forecast_weather', MIN(data_block_id), MAX(data_block_id) FROM dbo.forecast_weather
UNION ALL
SELECT 'electricity_prices', MIN(data_block_id), MAX(data_block_id) FROM dbo.electricity_prices;

-- Q5. Do weather stations map cleanly to counties? (NULL county = station outside any county)
SELECT CASE WHEN county IS NULL THEN 1 ELSE 0 END AS unmapped,
       COUNT(*)                                   AS n_stations
FROM dbo.weather_station_to_county_mapping
GROUP BY CASE WHEN county IS NULL THEN 1 ELSE 0 END;
