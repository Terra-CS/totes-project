from transform_create_dim_location import create_dim_location
import pandas as pd


# Does not mutate input data.
def test_create_location_doesnt_mutate_data():
    test_input = (
        [
            {
                "address_id": "1",
                "address_line_1": "6826 Herzog Via",
                "address_line_2": "None",
                "district": "Avon",
                "city": "New Patienceburgh",
                "postal_code": "28441",
                "country": "Turkey",
                "phone": "1803 637401",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            }
        ],
        [{"agreed_delivery_location_id": "1"}],
    )
    create_dim_location(*test_input)
    assert test_input == (
        [
            {
                "address_id": "1",
                "address_line_1": "6826 Herzog Via",
                "address_line_2": "None",
                "district": "Avon",
                "city": "New Patienceburgh",
                "postal_code": "28441",
                "country": "Turkey",
                "phone": "1803 637401",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            }
        ],
        [{"agreed_delivery_location_id": "1"}],
    )


# returns empty dataframe for empty input list
def test_create_dim_location_returns_empty_for_no_data():
    test_input = ([], [])
    test_output = create_dim_location(*test_input)
    assert test_output is None


# returns a dataframe
def test_create_dim_location_returns_dataframe():
    test_input = (
        [
            {
                "address_id": "1",
                "address_line_1": "6826 Herzog Via",
                "address_line_2": "None",
                "district": "Avon",
                "city": "New Patienceburgh",
                "postal_code": "28441",
                "country": "Turkey",
                "phone": "1803 637401",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            }
        ],
        [{"agreed_delivery_location_id": "1"}],
    )
    test_output = create_dim_location(*test_input)
    assert isinstance(test_output, pd.DataFrame)


# returns a dataframe with correct columns
def test_create_dim_location_returns_dataframe_with_cols():
    test_input = (
        [
            {
                "address_id": "1",
                "address_line_1": "6826 Herzog Via",
                "address_line_2": "None",
                "district": "Avon",
                "city": "New Patienceburgh",
                "postal_code": "28441",
                "country": "Turkey",
                "phone": "1803 637401",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            }
        ],
        [{"agreed_delivery_location_id": "1"}],
    )
    test_output = create_dim_location(*test_input)
    assert test_output.columns.to_list() == [
        "location_id",
        "address_line_1",
        "address_line_2",
        "district",
        "city",
        "postal_code",
        "country",
        "phone",
    ]


# returns a dataframe with multiple rows
def test_create_dim_location_returns_dataframe_with_rows():
    test_input = (
        [
            {
                "address_id": "1",
                "address_line_1": "6826 Herzog Via",
                "address_line_2": "None",
                "district": "Avon",
                "city": "New Patienceburgh",
                "postal_code": "28441",
                "country": "Turkey",
                "phone": "1803 637401",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            },
            {
                "address_id": "2",
                "address_line_1": "179 Alexie Cliffs",
                "address_line_2": "None",
                "district": "None",
                "city": "Aliso Viejo",
                "postal_code": "99305-7380",
                "country": "San Marino",
                "phone": "9621 880720",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            },
        ],
        [{"agreed_delivery_location_id": "1"},
         {"agreed_delivery_location_id": "2"}],
    )
    test_output = create_dim_location(*test_input)
    expected_output = pd.DataFrame(
        {
            "location_id": ["1", "2"],
            "address_line_1": ["6826 Herzog Via", "179 Alexie Cliffs"],
            "address_line_2": ["None", "None"],
            "district": ["Avon", "None"],
            "city": ["New Patienceburgh", "Aliso Viejo"],
            "postal_code": ["28441", "99305-7380"],
            "country": ["Turkey", "San Marino"],
            "phone": ["1803 637401", "9621 880720"],
        }
    )
    pd.testing.assert_frame_equal(test_output, expected_output)


# returns a dataframe with one row despite two given
def test_create_dim_location_doesnt_include_ids_not_in_sales():
    test_input = (
        [
            {
                "address_id": "1",
                "address_line_1": "6826 Herzog Via",
                "address_line_2": "None",
                "district": "Avon",
                "city": "New Patienceburgh",
                "postal_code": "28441",
                "country": "Turkey",
                "phone": "1803 637401",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            },
            {
                "address_id": "2",
                "address_line_1": "179 Alexie Cliffs",
                "address_line_2": "None",
                "district": "None",
                "city": "Aliso Viejo",
                "postal_code": "99305-7380",
                "country": "San Marino",
                "phone": "9621 880720",
                "created_at": "2022-11-03 14:20:49.962000",
                "last_updated": "2022-11-03 14:20:49.962000",
            },
        ],
        [{"agreed_delivery_location_id": "1"}],
    )
    test_output = create_dim_location(*test_input)
    expected_output = pd.DataFrame(
        {
            "location_id": ["1"],
            "address_line_1": ["6826 Herzog Via"],
            "address_line_2": ["None"],
            "district": ["Avon"],
            "city": ["New Patienceburgh"],
            "postal_code": ["28441"],
            "country": ["Turkey"],
            "phone": ["1803 637401"],
        }
    )
    pd.testing.assert_frame_equal(test_output, expected_output)
