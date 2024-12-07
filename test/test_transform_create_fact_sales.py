from transform_create_fact_sales import create_fact_sales
import pandas as pd


# doesn't mutate input
def test_create_fact_sales_doesnt_mutate_data():
    test_input = [
        {
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
        },
        {
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
        },
    ]
    create_fact_sales(test_input)
    assert test_input == [
        {
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
        },
        {
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
        },
    ]


# returns empty dataframe for empty input list
def test_create_fact_sales_returns_empty():
    test_input = []
    test_output = create_fact_sales(test_input)
    assert test_output is None


# returns a dataframe
def test_create_fact_sales_returns_dataframe():
    test_input = [
        {
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
        },
        {
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
        },
    ]
    test_output = create_fact_sales(test_input)
    assert isinstance(test_output, pd.DataFrame)


# returns a dataframe with correct columns
def test_create_fact_sales_returns_dataframe_with_cols():
    test_input = [
        {
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
        },
        {
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
        },
    ]
    test_output = create_fact_sales(test_input)
    assert test_output.columns.to_list() == [
        "sales_order_id",
        "created_date",
        "created_time",
        "last_updated_date",
        "last_updated_time",
        "sales_staff_id",
        "counterparty_id",
        "units_sold",
        "unit_price",
        "currency_id",
        "design_id",
        "agreed_payment_date",
        "agreed_delivery_date",
        "agreed_delivery_location_id",
    ]


# returns a dataframe with multiple rows
def test_create_fact_sales_returns_dataframe_with_rows():
    test_input = [
        {
            "sales_order_id": "r1",
            "created_at": "2024-11-14 11:57:09.915000",
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
        },
        {
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
        },
    ]
    test_output = create_fact_sales(test_input)
    expected_output = pd.DataFrame(
        {
            "sales_order_id": ["r1", "r2"],
            "created_date": ["2024-11-14", "r2:1234567"],
            "created_time": ["11:57:09.915000", "910"],
            "last_updated_date": ["r1:1234567", "r2:1234567"],
            "last_updated_time": ["910", "910"],
            "sales_staff_id": ["r1", "r2"],
            "counterparty_id": ["r1", "r2"],
            "units_sold": ["r1", "r2"],
            "unit_price": ["r1", "r2"],
            "currency_id": ["r1", "r2"],
            "design_id": ["r1", "r2"],
            "agreed_payment_date": ["r1", "r2"],
            "agreed_delivery_date": ["r1", "r2"],
            "agreed_delivery_location_id": ["r1", "r2"],
        }
    )
    pd.testing.assert_frame_equal(test_output, expected_output)
