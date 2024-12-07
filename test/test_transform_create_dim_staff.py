from transform_create_dim_staff import create_dim_staff
import pandas as pd


# Does not mutate input data.
def test_create_staff_doesnt_mutate_data():
    test_input = (
        [
            {
                "staff_id": "r1",
                "created_at": "r1",
                "last_updated": "r1",
                "first_name": "r1",
                "last_name": "r1",
                "department_id": "r1",
                "email_address": "r1",
            },
            {
                "staff_id": "r2",
                "created_at": "r2",
                "last_updated": "r2",
                "first_name": "r2",
                "last_name": "r2",
                "department_id": "r2",
                "email_address": "r2",
            },
        ],
        [
            {
                "department_id": "r1",
                "created_at": "r1",
                "last_updated": "r1",
                "department_name": "r1",
                "location": "r1",
                "manager": "r1",
            },
            {
                "department_id": "r2",
                "created_at": "r2",
                "last_updated": "r2",
                "department_name": "r2",
                "location": "r2",
                "manager": "r2",
            },
        ],
    )
    create_dim_staff(*test_input)
    assert test_input == (
        [
            {
                "staff_id": "r1",
                "created_at": "r1",
                "last_updated": "r1",
                "first_name": "r1",
                "last_name": "r1",
                "department_id": "r1",
                "email_address": "r1",
            },
            {
                "staff_id": "r2",
                "created_at": "r2",
                "last_updated": "r2",
                "first_name": "r2",
                "last_name": "r2",
                "department_id": "r2",
                "email_address": "r2",
            },
        ],
        [
            {
                "department_id": "r1",
                "created_at": "r1",
                "last_updated": "r1",
                "department_name": "r1",
                "location": "r1",
                "manager": "r1",
            },
            {
                "department_id": "r2",
                "created_at": "r2",
                "last_updated": "r2",
                "department_name": "r2",
                "location": "r2",
                "manager": "r2",
            },
        ],
    )


# returns empty dataframe for empty input list
def test_create_dim_staff_returns_empty():
    test_input = ([], [])
    test_output = create_dim_staff(*test_input)
    assert test_output is None


# returns a dataframe
def test_create_dim_staff_returns_dataframe():
    test_input = (
        [
            {
                "staff_id": "r1",
                "created_at": "r1",
                "last_updated": "r1",
                "first_name": "r1",
                "last_name": "r1",
                "department_id": "r1",
                "email_address": "r1",
            },
            {
                "staff_id": "r2",
                "created_at": "r2",
                "last_updated": "r2",
                "first_name": "r2",
                "last_name": "r2",
                "department_id": "r2",
                "email_address": "r2",
            },
        ],
        [
            {
                "department_id": "r1",
                "created_at": "r1",
                "last_updated": "r1",
                "department_name": "r1",
                "location": "r1",
                "manager": "r1",
            },
            {
                "department_id": "r2",
                "created_at": "r2",
                "last_updated": "r2",
                "department_name": "r2",
                "location": "r2",
                "manager": "r2",
            },
        ],
    )
    test_output = create_dim_staff(*test_input)
    assert isinstance(test_output, pd.DataFrame)


# returns a dataframe with correct columns
def test_create_dim_staff_returns_dataframe_with_cols():
    test_input = (
        [
            {
                "staff_id": "r1",
                "created_at": "r1",
                "last_updated": "r1",
                "first_name": "r1",
                "last_name": "r1",
                "department_id": "r1",
                "email_address": "r1",
            },
            {
                "staff_id": "r2",
                "created_at": "r2",
                "last_updated": "r2",
                "first_name": "r2",
                "last_name": "r2",
                "department_id": "r2",
                "email_address": "r2",
            },
        ],
        [
            {
                "department_id": "r1",
                "created_at": "r1",
                "last_updated": "r1",
                "department_name": "r1",
                "location": "r1",
                "manager": "r1",
            },
            {
                "department_id": "r2",
                "created_at": "r2",
                "last_updated": "r2",
                "department_name": "r2",
                "location": "r2",
                "manager": "r2",
            },
        ],
    )
    test_output = create_dim_staff(*test_input)
    assert test_output.columns.to_list() == [
        "staff_id",
        "first_name",
        "last_name",
        "department_name",
        "location",
        "email_address",
    ]


# returns a dataframe with multiple rows
def test_create_dim_staff_returns_dataframe_with_rows():
    test_input = (
        [
            {
                "staff_id": "r1",
                "created_at": "r1",
                "last_updated": "r1",
                "first_name": "r1",
                "last_name": "r1",
                "department_id": "r1",
                "email_address": "r1",
            },
            {
                "staff_id": "r2",
                "created_at": "r2",
                "last_updated": "r2",
                "first_name": "r2",
                "last_name": "r2",
                "department_id": "r2",
                "email_address": "r2",
            },
        ],
        [
            {
                "department_id": "r1",
                "created_at": "r1",
                "last_updated": "r1",
                "department_name": "r1",
                "location": "r1",
                "manager": "r1",
            },
            {
                "department_id": "r2",
                "created_at": "r2",
                "last_updated": "r2",
                "department_name": "r2",
                "location": "r2",
                "manager": "r2",
            },
        ],
    )
    test_output = create_dim_staff(*test_input)
    expected_output = pd.DataFrame(
        {
            "staff_id": ["r1", "r2"],
            "first_name": ["r1", "r2"],
            "last_name": ["r1", "r2"],
            "department_name": ["r1", "r2"],
            "location": ["r1", "r2"],
            "email_address": ["r1", "r2"],
        }
    )
    pd.testing.assert_frame_equal(test_output, expected_output)
