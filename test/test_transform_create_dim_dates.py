from transform_create_dim_dates import create_dim_dates
import pandas as pd


# Does not mutate input data.
def test_create_date_doesnt_mutate_data():
    test_input = [
        {
            "created_at": "2024-11-19 10:03:10.150000",
            "last_updated": "2024-11-19 10:03:10.150000",
            "agreed_payment_date": "2024-11-24",
            "agreed_delivery_date": "2024-12-24",
        }
    ]
    create_dim_dates(test_input)
    assert test_input == [
        {
            "created_at": "2024-11-19 10:03:10.150000",
            "last_updated": "2024-11-19 10:03:10.150000",
            "agreed_payment_date": "2024-11-24",
            "agreed_delivery_date": "2024-12-24",
        }
    ]


# returns empty dataframe for empty input list
def test_create_dim_date_returns_empty():
    test_input = []
    test_output = create_dim_dates(test_input)
    assert test_output is None


# returns a dataframe
def test_create_dim_date_returns_dataframe():
    test_input = [
        {
            "created_at": "2024-11-19 10:03:10.150000",
            "last_updated": "2024-11-19 10:03:10.150000",
            "agreed_payment_date": "2024-11-24",
            "agreed_delivery_date": "2024-12-24",
        }
    ]
    test_output = create_dim_dates(test_input)
    assert isinstance(test_output, pd.DataFrame)


# returns a dataframe with correct columns
def test_create_dim_date_returns_dataframe_with_cols():
    test_input = [
        {
            "created_at": "2024-11-19 10:03:10.150000",
            "last_updated": "2024-11-19 10:03:10.150000",
            "agreed_payment_date": "2024-11-24",
            "agreed_delivery_date": "2024-12-24",
        }
    ]
    test_output = create_dim_dates(test_input)
    assert test_output.columns.to_list() == [
        "date_id",
        "year",
        "month",
        "day",
        "day_of_week",
        "day_name",
        "month_name",
        "quarter",
    ]


# returns a dataframe with multiple rows
def test_create_dim_date_returns_dataframe_with_rows():
    test_input = [
        {
            "created_at": "2024-11-19 10:03:10.150000",
            "last_updated": "2024-11-19 10:03:10.150000",
            "agreed_payment_date": "2024-11-24",
            "agreed_delivery_date": "2024-12-24",
        },
        {
            "created_at": "2024-11-19 10:03:10.150000",
            "last_updated": "2024-11-19 10:03:10.150000",
            "agreed_payment_date": "2024-11-24",
            "agreed_delivery_date": "2024-12-24",
        },
    ]
    test_output = create_dim_dates(test_input)
    expected_output = pd.DataFrame(
        {
            "date_id": ["2024-11-19", "2024-11-24", "2024-12-24"],
            "year": ["2024", "2024", "2024"],
            "month": ["11", "11", "12"],
            "day": ["19", "24", "24"],
            "day_of_week": ["2", "0", "2"],
            "day_name": ["Tuesday", "Sunday", "Tuesday"],
            "month_name": ["November", "November", "December"],
            "quarter": [4, 4, 4],
        }
    )
    pd.testing.assert_frame_equal(test_output, expected_output)
