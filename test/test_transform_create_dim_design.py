from transform_create_dim_design import create_dim_design
import pandas as pd


# Does not mutate input data.
def test_create_design_doesnt_mutate_data():
    test_input = [
        {
            "design_id": "r1",
            "created_at": "r1",
            "last_updated": "r1",
            "design_name": "r1",
            "file_location": "r1",
            "file_name": "r1",
        },
        {
            "design_id": "r2",
            "created_at": "r2",
            "last_updated": "r2",
            "design_name": "r2",
            "file_location": "r2",
            "file_name": "r2",
        },
    ]
    create_dim_design(test_input)
    assert test_input == [
        {
            "design_id": "r1",
            "created_at": "r1",
            "last_updated": "r1",
            "design_name": "r1",
            "file_location": "r1",
            "file_name": "r1",
        },
        {
            "design_id": "r2",
            "created_at": "r2",
            "last_updated": "r2",
            "design_name": "r2",
            "file_location": "r2",
            "file_name": "r2",
        },
    ]


# returns empty dataframe for empty input list
def test_create_dim_design_returns_empty():
    test_input = []
    test_output = create_dim_design(test_input)
    assert test_output is None


# returns a dataframe
def test_create_dim_design_returns_dataframe():
    test_input = [
        {
            "design_id": "r1",
            "created_at": "r1",
            "last_updated": "r1",
            "design_name": "r1",
            "file_location": "r1",
            "file_name": "r1",
        },
        {
            "design_id": "r2",
            "created_at": "r2",
            "last_updated": "r2",
            "design_name": "r2",
            "file_location": "r2",
            "file_name": "r2",
        },
    ]
    test_output = create_dim_design(test_input)
    assert isinstance(test_output, pd.DataFrame)


# returns a dataframe with correct columns
def test_create_dim_design_returns_dataframe_with_cols():
    test_input = [
        {
            "design_id": "r1",
            "created_at": "r1",
            "last_updated": "r1",
            "design_name": "r1",
            "file_location": "r1",
            "file_name": "r1",
        },
        {
            "design_id": "r2",
            "created_at": "r2",
            "last_updated": "r2",
            "design_name": "r2",
            "file_location": "r2",
            "file_name": "r2",
        },
    ]
    test_output = create_dim_design(test_input)
    assert test_output.columns.to_list() == [
        "design_id",
        "design_name",
        "file_name",
        "file_location",
    ]


# returns a dataframe with multiple rows
def test_create_dim_design_returns_dataframe_with_rows():
    test_input = [
        {
            "design_id": "r1",
            "created_at": "r1",
            "last_updated": "r1",
            "design_name": "r1",
            "file_location": "r1",
            "file_name": "r1",
        },
        {
            "design_id": "r2",
            "created_at": "r2",
            "last_updated": "r2",
            "design_name": "r2",
            "file_location": "r2",
            "file_name": "r2",
        },
    ]
    test_output = create_dim_design(test_input)
    expected_output = pd.DataFrame(
        {
            "design_id": ["r1", "r2"],
            "design_name": ["r1", "r2"],
            "file_name": ["r1", "r2"],
            "file_location": ["r1", "r2"],
        }
    )
    pd.testing.assert_frame_equal(test_output, expected_output)
