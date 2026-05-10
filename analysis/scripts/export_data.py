"""Export experiment data from PostgreSQL to CSV files for analysis."""

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://stylefatigue:stylefatigue@localhost:5432/stylefatigue",
)

OUTPUT_DIR = Path(__file__).parent.parent / "data"

TABLES = [
    "participants",
    "sessions",
    "conversations",
    "survey_responses",
    "event_log",
]


def export():
    OUTPUT_DIR.mkdir(exist_ok=True)
    engine = create_engine(DATABASE_URL)

    for table in TABLES:
        print(f"Exporting {table}...")
        df = pd.read_sql_table(table, engine)
        output_path = OUTPUT_DIR / f"{table}.csv"
        df.to_csv(output_path, index=False)
        print(f"  -> {output_path} ({len(df)} rows)")

    print("Done.")


if __name__ == "__main__":
    export()
