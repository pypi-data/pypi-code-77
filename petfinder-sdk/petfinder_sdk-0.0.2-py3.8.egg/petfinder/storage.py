import sqlite3
import numpy as np
import pandas as pd
from pydantic import BaseModel
from datetime import datetime
from typing import Union, Type


class Column(BaseModel):
    name: str
    type: Union[Type[str], Type[int], Type[bool], Type[datetime]]
    primary_key: bool = False
    required: bool = False
    unique: bool = False

    def sql_declaration(self) -> str:
        dtype = "TEXT" if (self.type is str or self.type is datetime) else "INTEGER"

        flags = []
        if self.primary_key:
            flags.append("PRIMARY KEY")
        if self.required:
            flags.append("NOT NULL")
        if self.unique:
            flags.append("UNIQUE")

        return " ".join([self.name, dtype, *flags])


ANIMALS_COLUMNS = (
    Column(name="id", type=str, primary_key=True),
    Column(name="name", type=str),
    Column(name="type", type=str, required=True),
    Column(name="status", type=str, required=True),
    Column(name="organization_id", type=str),
    Column(name="species", type=str),
    Column(name="age", type=str),
    Column(name="gender", type=str),
    Column(name="size", type=str),
    Column(name="coat", type=str),
    Column(name="published_at", type=datetime),
    Column(name="status_changed_at", type=datetime),
    Column(name="breed_primary", type=str),
    Column(name="breed_secondary", type=str),
    Column(name="breed_mixed", type=bool),
    Column(name="breed_unknown", type=bool),
    Column(name="color_primary", type=str),
    Column(name="color_secondary", type=str),
    Column(name="color_tertiary", type=str),
    Column(name="spayed_neutered", type=bool),
    Column(name="house_trained", type=bool),
    Column(name="special_needs", type=bool),
    Column(name="shots_current", type=bool),
    Column(name="declawed", type=bool),
    Column(name="good_with_children", type=bool),
    Column(name="good_with_dogs", type=bool),
    Column(name="good_with_cats", type=bool),
    Column(name="description", type=str),
    Column(name="url", type=str),
    Column(name="number_of_photos", type=int, required=True),
    Column(name="contact_email", type=str),
    Column(name="contact_phone", type=str),
    Column(name="contact_address1", type=str),
    Column(name="contact_address2", type=str),
    Column(name="contact_city", type=str),
    Column(name="contact_state", type=str),
    Column(name="contact_postcode", type=str),
    Column(name="contact_country", type=str),
    Column(name="primary_photo_small", type=str),
    Column(name="primary_photo_medium", type=str),
    Column(name="primary_photo_large", type=str),
    Column(name="primary_photo_full", type=str),
)

_CREATE_ANIMALS_TABLE = f"""
CREATE TABLE IF NOT EXISTS animals (
    {','.join(c.sql_declaration() for c in ANIMALS_COLUMNS)}
);
"""

_UPSERT_ANIMAL = f"""
INSERT OR REPLACE INTO animals ({','.join(c.name for c in ANIMALS_COLUMNS)})
VALUES ({','.join('?' for c in ANIMALS_COLUMNS)})
"""

PHOTOS_COLUMNS = (
    Column(name="animal_id", type=str, required=True),
    Column(name="photo_size", type=str, required=True),
    Column(name="photo_url", type=str, required=True, unique=True),
)

_CREATE_PHOTOS_TABLE = f"""
CREATE TABLE IF NOT EXISTS photos (
    {','.join(c.sql_declaration() for c in PHOTOS_COLUMNS)},
    FOREIGN KEY(animal_id) REFERENCES animals(id)
);
"""

_UPSERT_PHOTO = f"""
INSERT OR REPLACE INTO photos ({','.join(c.name for c in PHOTOS_COLUMNS)})
VALUES ({','.join('?' for c in PHOTOS_COLUMNS)})
"""

TAGS_COLUMNS = (
    Column(name="animal_id", type=str, required=True),
    Column(name="tag", type=str, required=True),
)

_CREATE_TAGS_TABLE = f"""
CREATE TABLE IF NOT EXISTS tags (
    {','.join(c.sql_declaration() for c in TAGS_COLUMNS)},
    FOREIGN KEY(animal_id) REFERENCES animals(id)
);
"""

_UPSERT_TAG = f"""
INSERT OR REPLACE INTO tags ({','.join(c.name for c in TAGS_COLUMNS)})
VALUES ({','.join('?' for c in TAGS_COLUMNS)})
"""


def save_to_sqlite(db_file: str, animals: pd.DataFrame, photos: pd.DataFrame, tags: pd.DataFrame) -> None:
    """
    Saves a set of results into a sqlite database.
    """
    sqlite3.register_adapter(np.int64, int)
    sqlite3.register_adapter(np.int32, int)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(_CREATE_ANIMALS_TABLE)
    cursor.execute(_CREATE_PHOTOS_TABLE)
    cursor.execute(_CREATE_TAGS_TABLE)

    # Normalize the data and put it in the right order
    animals = animals.copy()
    animals["id"] = animals["id"].astype(str)
    animals = animals[[c.name for c in ANIMALS_COLUMNS]]
    # Convert True to 1 and False to 0
    animals.replace({True: 1, False: 0}, inplace=True)
    # Convert to datetime format...
    for c in ANIMALS_COLUMNS:
        if c.type is datetime:
            animals[c.name] = animals[c.name].dt.strftime("%Y-%m-%dT%H:%M%:%SZ")
    cursor.executemany(_UPSERT_ANIMAL, animals.to_records(index=False))

    # Now photos
    photos = photos.copy()
    photos["animal_id"] = photos["animal_id"].astype(str)
    photos = photos[[c.name for c in PHOTOS_COLUMNS]]
    cursor.executemany(_UPSERT_PHOTO, photos.to_records(index=False))

    # Now tags
    tags = tags.copy()
    tags["animal_id"] = tags["animal_id"].astype(str)
    tags = tags[[c.name for c in TAGS_COLUMNS]]
    cursor.executemany(_UPSERT_TAG, tags.to_records(index=False))

    conn.commit()
    conn.close()


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


def load_photos(db_file: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f"SELECT {','.join(c.name for c in PHOTOS_COLUMNS)} FROM photos")

    df = pd.DataFrame.from_records(
        cursor.fetchall(), columns=[c.name for c in PHOTOS_COLUMNS]
    )

    conn.close()
    return df


def load_tags(db_file: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f"SELECT {','.join(c.name for c in TAGS_COLUMNS)} FROM tags")
    df = pd.DataFrame.from_records(
        cursor.fetchall(), columns=[c.name for c in TAGS_COLUMNS]
    )
    conn.close()
    return df

#
# def load_results(db_file: str) -> PandasResults:
#     return PandasResults(
#         animals=load_animals(db_file),
#         photos=load_photos(db_file),
#         tags=load_tags(db_file),
#     )


def move_results():
    db_file = "/Users/phillipdupuis/databases/petfinder/sqlite.db"

    # results = load_results(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE animals;")
    conn.commit()

    # save_to_sqlite(db_file, results)


#
# def select_photos_by_state(db_file: str, state: str) -> pd.DataFrame:
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()
#
#     statement = "SELECT photo_size, photo_url, url FROM photos LEFT JOIN animals ON photos.animal_id = animals.id WHERE contact_state = ?"
#     cursor.execute(statement, (state,))
#     photos = cursor.fetchall()
#     cat = 'yo'


def check_it():
    DB_FILE = "/Users/phillipdupuis/databases/petfinder/sqlite.db"

    # animals = load_animals(DB_FILE)
    # photos = load_photos(DB_FILE)
    # results = load_results(DB_FILE)
    cat = "yooo"
    # conn = sqlite3.connect(DB_FILE)
    # cursor = conn.cursor()
    #
    # cursor.execute("SELECT * FROM animals")
    #
    # df = pd.DataFrame.from_records(
    #     cursor.fetchall(), columns=[c.name for c in ANIMALS_COLUMNS]
    # )
    #
    # for c in ANIMALS_COLUMNS:
    #     if c.type is datetime:
    #         df[c.name] = pd.to_datetime(df[c.name])
    #     elif c.type is bool:
    #         df[c.name] = df[c.name].replace({0: False, 1: True})
    #
    # cat = "hi"
    # conn.close()


if __name__ == "__main__":
    move_results()

    # conn = sqlite3.connect("/Users/phillipdupuis/databases/petfinder/sqlite.db")
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM ANIMALS")
    # df = load_animals("/Users/phillipdupuis/databases/petfinder/sqlite.db")
    # cat = "hi"
    # select_photos_by_state("/Users/phillipdupuis/databases/petfinder/sqlite.db", "MA")
