from transform_create_dim_currency import create_dim_currency
import pandas as pd


# Does not mutate input data.
def test_create_currency_doesnt_mutate_data():
    test_input = [
        {
            "currency_id": "r1",
            "currency_code": "GBP",
            "created_at": "r1:12345678910",
            "last_updated": "r1",
        },
        {
            "currency_id": "r2",
            "currency_code": "GBP",
            "created_at": "r2:12345678910",
            "last_updated": "r2",
        },
    ]
    create_dim_currency(test_input)
    assert test_input == [
        {
            "currency_id": "r1",
            "currency_code": "GBP",
            "created_at": "r1:12345678910",
            "last_updated": "r1",
        },
        {
            "currency_id": "r2",
            "currency_code": "GBP",
            "created_at": "r2:12345678910",
            "last_updated": "r2",
        },
    ]


# returns empty dataframe for empty input list
def test_create_dim_currency_returns_empty():
    test_input = []
    test_output = create_dim_currency(test_input)
    assert test_output is None


# returns a dataframe
def test_create_dim_currency_returns_dataframe():
    test_input = [
        {
            "currency_id": "r1",
            "currency_code": "GBP",
            "created_at": "r1:12345678910",
            "last_updated": "r1",
        },
        {
            "currency_id": "r2",
            "currency_code": "GBP",
            "created_at": "r2:12345678910",
            "last_updated": "r2",
        },
    ]
    test_output = create_dim_currency(test_input)
    assert isinstance(test_output, pd.DataFrame)


# returns a dataframe with correct columns
def test_create_dim_currency_returns_dataframe_with_cols():
    test_input = [
        {
            "currency_id": "r1",
            "currency_code": "GBP",
            "created_at": "r1:12345678910",
            "last_updated": "r1",
        },
        {
            "currency_id": "r2",
            "currency_code": "GBP",
            "created_at": "r2:12345678910",
            "last_updated": "r2",
        },
    ]
    test_output = create_dim_currency(test_input)
    assert test_output.columns.to_list() == [
        "currency_id",
        "currency_code",
        "currency_name",
    ]


# returns a dataframe with multiple rows
def test_create_dim_currency_returns_dataframe_with_rows():
    test_input = [
        {
            "currency_id": "r1",
            "currency_code": "GBP",
            "created_at": "r1:12345678910",
            "last_updated": "r1",
        },
        {
            "currency_id": "r2",
            "currency_code": "GBP",
            "created_at": "r2:12345678910",
            "last_updated": "r2",
        },
    ]
    test_output = create_dim_currency(test_input)
    expected_output = pd.DataFrame(
        {
            "currency_id": ["r1", "r2"],
            "currency_code": ["GBP", "GBP"],
            "currency_name": ["Pound Sterling", "Pound Sterling"],
        }
    )
    pd.testing.assert_frame_equal(test_output, expected_output)
