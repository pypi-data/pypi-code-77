import pandas as pd
import sqlite3
import datetime
from scripts.storage import ANIMALS_COLUMNS



def load_animals(db_file: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animals")

    df = pd.DataFrame.from_records(
        cursor.fetchall(), columns=[c.name for c in ANIMALS_COLUMNS]
    )
    for c in ANIMALS_COLUMNS:
        if c.type is datetime:
            df[c.name] = pd.to_datetime(df[c.name])
        elif c.type is bool:
            df[c.name] = df[c.name].replace({0: False, 1: True})

    conn.close()
    return df


if __name__ == "__main__":
    db_file = "/Users/phillipdupuis/databases/petfinder/sqlite.db"
    df = load_animals(db_file)
    cat = "yp"