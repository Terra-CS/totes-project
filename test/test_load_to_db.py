from unittest import mock
import pandas as pd
import sqlite3
import pytest
from load_to_db import load_to_db
from sqlalchemy import create_mock_engine


def dump(sql, *multiparams, **params):
    print(sql.compile(dialect=engine.dialect))


engine = create_mock_engine('postgresql+pg8000://', dump)


engine = create_mock_engine("postgresql+pg8000://", dump)


@pytest.fixture(scope="class")
def create_mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE fact_sales_order (
                sales_record_id INTEGER PRIMARY KEY,
                sales_order_id INTEGER,
                created_date INTEGER,
                created_time INTEGER,
                last_updated_date INTEGER,
                last_updated_time INTEGER,
                sales_staff_id INTEGER,
                counterparty_id INTEGER,
                units_sold INTEGER,
                unit_price INTEGER,
                currency_id INTEGER,
                design_id INTEGER,
                agreed_payment_date INTEGER,
                agreed_delivery_date INTEGER,
                agreed_delivery_location_id INTEGER)
                """
    )
    conn.commit()
    return conn


class TestLoadFact:

    # Test if "to_sql" method is being called with correct arguments
    @mock.patch("pandas.DataFrame.to_sql", return_value=mock.MagicMock())
    def test_load_to_db_with_mock(self, mock):
        fact_data = {
            "sales_order_id": "r1",
            "created_at": "r1:12345678910",
            "last_updated": "r1:12345678910",
            "staff_id": "r1",
            "counterparty_id": "r1",
            "units_sold": "r1",
            "unit_price": "r1",
            "currency_id": "r1",
            "design_id": "r1",
            "agreed_payment_date": "r1",
            "agreed_delivery_date": "r1",
            "agreed_delivery_location_id": "r1",
        }
        fact_df = pd.DataFrame(fact_data, index=[0])

        mock_engine = engine

        load_to_db([fact_df], mock_engine)

        fact_df.to_sql.assert_called_once_with(
            "fact_sales_order", mock_engine, if_exists="append", index=False
        )

    # Test if returns correct message and accepts more elements in the list
    @mock.patch("pandas.DataFrame.to_sql")
    def test_load_to_db_correctly_appends_to_fact_table(self, mock):
        df1 = {
            "sales_order_id": "r1",
            "created_at": "r1:12345678910",
            "last_updated": "r1:12345678910",
            "staff_id": "r1",
            "counterparty_id": "r1",
            "units_sold": "r1",
            "unit_price": "r1",
            "currency_id": "r1",
            "design_id": "r1",
            "agreed_payment_date": "r1",
            "agreed_delivery_date": "r1",
            "agreed_delivery_location_id": "r1",
        }
        df2 = {
            "sales_order_id": "r2",
            "created_at": "r2:12345678910",
            "last_updated": "r2:12345678910",
            "staff_id": "r2",
            "counterparty_id": "r2",
            "units_sold": "r2",
            "unit_price": "r2",
            "currency_id": "r2",
            "design_id": "r2",
            "agreed_payment_date": "r2",
            "agreed_delivery_date": "r2",
            "agreed_delivery_location_id": "r2",
        }

        df_list = [pd.DataFrame(df1, index=[0]), pd.DataFrame(df2, index=[0])]

        result = load_to_db(df_list, engine)
        assert result == "data uploaded to the data warehouse"


class TestLoadUpload:

    def test_upload_fact_table(self, create_mock_db):
        conn = create_mock_db
        data = {
            "sales_order_id": [3, 3],
            "created_date": [1, 2],
            "created_time": [1, 2],
            "last_updated_date": [1, 2],
            "last_updated_time": [1, 2],
            "sales_staff_id": [1, 2],
            "counterparty_id": [1, 2],
            "units_sold": [1, 2],
            "unit_price": [1, 2],
            "currency_id": [1, 2],
            "design_id": [1, 2],
            "agreed_payment_date": [1, 2],
            "agreed_delivery_date": [1, 2],
            "agreed_delivery_location_id": [1, 2],
        }
        df_list = [pd.DataFrame(data)]
        load_to_db(df_list, engine=conn)

        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM fact_sales_order""")
        result = cursor.fetchall()
        assert result == [
            (1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
            (2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2),
        ]
