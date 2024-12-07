from upsert_dim_tables import upsert_dim_tables
import pandas as pd
import sqlite3
import pytest


@pytest.fixture(scope="class")
def create_mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE dim_date (
                   date_id INTEGER PRIMARY KEY,
                   year INTEGER,
                   month INTEGER,
                   day INTEGER,
                   day_of_week INTEGER,
                   day_name VARCHAR (10),
                   month_name VARCHAR (10),
                   quarter INTEGER)"""
    )
    cursor.execute(
        """
    CREATE TABLE dim_design (
                   design_id INTEGER PRIMARY KEY,
                   design_name VARCHAR (40),
                   file_location VARCHAR (40),
                   file_name VARCHAR (40))"""
    )
    conn.commit()
    return conn


def test_uploads_new_data_to_warehouse(create_mock_db):
    conn = create_mock_db
    data = {
        "date_id": [1, 2],
        "year": [2023, 2023],
        "month": [1, 1],
        "day": [1, 2],
        "day_of_week": [7, 1],
        "day_name": ["Sunday", "Monday"],
        "month_name": ["January", "January"],
        "quarter": [1, 1],
    }
    df = pd.DataFrame(data)
    primary_key = df.columns[0]
    upsert_dim_tables(df, primary_key, conn)

    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM dim_date""")
    result = cursor.fetchall()
    assert result == [
        (1, 2023, 1, 1, 7, "Sunday", "January", 1),
        (2, 2023, 1, 2, 1, "Monday", "January", 1),
    ]


# test updates existing data in warehouse
def test_upsert_updates_data(create_mock_db):
    conn = create_mock_db
    data = {
        "date_id": [1, 2],
        "year": [2023, 2023],
        "month": [1, 1],
        "day": [1, 2],
        "day_of_week": [7, 1],
        "day_name": ["Sunday", "Monday"],
        "month_name": ["January", "January"],
        "quarter": [1, 1],
    }
    df = pd.DataFrame(data)
    primary_key = "date_id"
    upsert_dim_tables(df, primary_key, conn)

    data_1 = {
        "date_id": [1],
        "year": [2023],
        "month": [3],
        "day": [1],
        "day_of_week": [7],
        "day_name": ["Sunday"],
        "month_name": ["March"],
        "quarter": [1],
    }
    df_1 = pd.DataFrame(data_1)
    primary_key_1 = "date_id"
    upsert_dim_tables(df_1, primary_key_1, conn)

    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM dim_date""")
    result = cursor.fetchall()
    assert result == [
        (1, 2023, 3, 1, 7, "Sunday", "March", 1),
        (2, 2023, 1, 2, 1, "Monday", "January", 1),
    ]


# test can handle a bundle of new data and updates to existing data
def test_upsert_handle_multiple_updates(create_mock_db):
    conn = create_mock_db
    # insert data in table date
    data = {
        "date_id": [1, 2],
        "year": [2023, 2023],
        "month": [1, 1],
        "day": [1, 2],
        "day_of_week": [7, 1],
        "day_name": ["Sunday", "Monday"],
        "month_name": ["January", "January"],
        "quarter": [1, 1],
    }
    df = pd.DataFrame(data)
    primary_key = "date_id"
    upsert_dim_tables(df, primary_key, conn)

    # insert data in table design
    data_1 = {
        "design_id": [1, 2],
        "design_name": ["a", "b"],
        "file_location": ["a", "b"],
        "file_name": ["a", "b"],
    }
    df_1 = pd.DataFrame(data_1)
    primary_key_1 = "design_id"
    upsert_dim_tables(df_1, primary_key_1, conn)

    # updating table date
    data_2 = {
        "date_id": [1, 2],
        "year": [2023, 2023],
        "month": [3, 1],
        "day": [1, 2],
        "day_of_week": [7, 1],
        "day_name": ["Sunday", "Monday"],
        "month_name": ["March", "January"],
        "quarter": [1, 1],
    }
    df_2 = pd.DataFrame(data_2)
    upsert_dim_tables(df_2, primary_key, conn)

    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM dim_date""")
    result = cursor.fetchall()
    assert result == [
        (1, 2023, 3, 1, 7, "Sunday", "March", 1),
        (2, 2023, 1, 2, 1, "Monday", "January", 1),
    ]

    # updating table design
    data_3 = {
        "design_id": [1, 2, 3],
        "design_name": ["c", "d", "e"],
        "file_location": ["c", "d", "e"],
        "file_name": ["c", "d", "e"],
    }
    df_3 = pd.DataFrame(data_3)
    upsert_dim_tables(df_3, primary_key_1, conn)

    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM dim_design""")
    result = cursor.fetchall()
    assert result == [(1, "c", "c", "c"),
                      (2, "d", "d", "d"),
                      (3, "e", "e", "e")]
