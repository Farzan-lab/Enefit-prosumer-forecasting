# %% [markdown]
# # 01 · Data Overview & Quality
# **Goal:** understand what each table contains, how they connect, and what data was
# available at forecast time (`data_block_id`).
#
# This is a VS Code "percent" notebook: each `# %%` is a cell. Click **Run Cell**,
# or convert to .ipynb with `jupytext --to notebook 01_data_overview.py`.
#
# > Write your observations in the markdown cells as you go. They become the raw
# > material for the README and the LinkedIn article.

# %%
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
con = duckdb.connect(str(ROOT / "data" / "processed" / "enefit.duckdb"), read_only=True)


def q(sql: str) -> pd.DataFrame:
    """Run a SQL query and return a DataFrame."""
    return con.execute(sql).df()


# %% [markdown]
# ## 1. Tables at a glance

# %%
tables = [t[0] for t in con.execute("SHOW TABLES").fetchall()]
overview = pd.DataFrame(
    {
        "table": tables,
        "rows": [q(f"SELECT COUNT(*) n FROM {t}")["n"][0] for t in tables],
        "cols": [len(q(f"DESCRIBE {t}")) for t in tables],
    }
)
overview

# %%
# Column names and types of the main table
q("DESCRIBE train")

# %%
q("SELECT * FROM train LIMIT 10")

# %% [markdown]
# ## 2. Running the first-look SQL checks
# Each query in `sql/01_first_look.sql` answers one question. Run them one by one:

# %%
sql_text = (ROOT / "sql" / "01_first_look.sql").read_text()
queries = [s.strip() for s in sql_text.split(";") if "SELECT" in s.upper()]
for i, sql in enumerate(queries, 1):
    print(f"\n===== Q{i} =====")
    display(q(sql))  # noqa: F821  (display is available in Jupyter)

# %% [markdown]
# ## 3. My observations (fill in)
# - Time coverage: ...
# - Missing values: ...
# - Biggest segments: ...
# - Data availability / `data_block_id`: ...
# - Questions to investigate next: ...
