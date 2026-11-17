# %% [markdown]
# # 01 · Data Overview & Quality
# **Goal:** understand what each table contains, how they connect, and what data was
# available at forecast time (`data_block_id`).
#
# Data lives in **Azure SQL Database**. Python connects via SQLAlchemy + pyodbc
# (see `src/db.py`). Credentials come from your local `.env` file.
#
# This is a VS Code "percent" notebook: each `# %%` is a cell. Click **Run Cell**.
#
# > Write your observations in the markdown cells as you go. They become the raw
# > material for the README and the LinkedIn article.

# %%
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import text

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.append(str(ROOT))
from src.db import get_engine, wait_until_awake  # noqa: E402

engine = get_engine()
wait_until_awake(engine)


def q(sql: str) -> pd.DataFrame:
    """Run a SQL query against Azure SQL and return a DataFrame."""
    with engine.connect() as con:
        return pd.read_sql(text(sql), con)


# %% [markdown]
# ## 1. Tables at a glance

# %%
q("""
SELECT t.name AS table_name,
       SUM(p.rows) AS n_rows,
       (SELECT COUNT(*) FROM sys.columns c WHERE c.object_id = t.object_id) AS n_cols
FROM sys.tables t
JOIN sys.partitions p ON p.object_id = t.object_id AND p.index_id IN (0, 1)
GROUP BY t.name, t.object_id
ORDER BY n_rows DESC
""")

# %%
# Column names and SQL types of the main table
q("""
SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'train'
ORDER BY ORDINAL_POSITION
""")

# %%
# Peek at a few rows (exploration only: this notebook is saved WITHOUT outputs)
q("SELECT TOP 10 * FROM dbo.train ORDER BY [datetime]")

# %% [markdown]
# ## 2. Running the first-look SQL checks
# Each query in `sql/01_first_look.sql` answers one question.

# %%
sql_text = (ROOT / "sql" / "01_first_look.sql").read_text(encoding="utf-8")
# strip comment lines, then split into individual statements
clean = "\n".join(l for l in sql_text.splitlines() if not l.strip().startswith("--"))
queries = [s.strip() for s in clean.split(";") if s.strip()]
for i, sql in enumerate(queries, 1):
    print(f"\n===== Q{i} =====")
    display(q(sql))  # noqa: F821  (display is available in Jupyter / VS Code)

# %% [markdown]
# ## 3. My observations (fill in)
# - Time coverage: ...
# - Missing values: ...
# - Biggest segments: ...
# - Data availability / `data_block_id`: ...
# - Timezones (which columns were converted to UTC during loading?): ...
# - Questions to investigate next: ...
