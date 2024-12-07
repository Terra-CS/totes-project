from transform_create_dim_counterparty import create_dim_counterparty
import pandas as pd


# Does not mutate input data.
def test_create_counterparty_doesnt_mutate_data():
    test_input = (
        [
            {
                "counterparty_id": "r1",
                "counterparty_legal_name": "r1",
                "created_at": "r1",
                "last_update": "r1",
                "legal_address_id": "r1",
                "commercial_contact": "r1",
                "delivery_contact": "r1",
            },
            {
                "counterparty_id": "r2",
                "counterparty_legal_name": "r2",
                "created_at": "r2",
                "last_update": "r2",
                "legal_address_id": "r2",
                "commercial_contact": "r2",
                "delivery_contact": "r2",
            },
        ],
        [
            {
                "address_id": "r1",
                "address_line_1": "r1",
                "address_line_2": "r1",
                "district": "r1",
                "city": "r1",
                "postal_code": "r1",
                "country": "r1",
                "phone": "r1",
                "created_at": "r1",
                "last_update": "r1",
            },
            {
                "address_id": "r2",
                "address_line_1": "r2",
                "address_line_2": "r2",
                "district": "r2",
                "city": "r2",
                "postal_code": "r2",
                "country": "r2",
                "phone": "r2",
                "created_at": "r2",
                "last_update": "r2",
            },
        ],
    )
    create_dim_counterparty(*test_input)
    assert test_input == (
        [
            {
                "counterparty_id": "r1",
                "counterparty_legal_name": "r1",
                "created_at": "r1",
                "last_update": "r1",
                "legal_address_id": "r1",
                "commercial_contact": "r1",
                "delivery_contact": "r1",
            },
            {
                "counterparty_id": "r2",
                "counterparty_legal_name": "r2",
                "created_at": "r2",
                "last_update": "r2",
                "legal_address_id": "r2",
                "commercial_contact": "r2",
                "delivery_contact": "r2",
            },
        ],
        [
            {
                "address_id": "r1",
                "address_line_1": "r1",
                "address_line_2": "r1",
                "district": "r1",
                "city": "r1",
                "postal_code": "r1",
                "country": "r1",
                "phone": "r1",
                "created_at": "r1",
                "last_update": "r1",
            },
            {
                "address_id": "r2",
                "address_line_1": "r2",
                "address_line_2": "r2",
                "district": "r2",
                "city": "r2",
                "postal_code": "r2",
                "country": "r2",
                "phone": "r2",
                "created_at": "r2",
                "last_update": "r2",
            },
        ],
    )


# returns empty dataframe for empty input list
def test_create_dim_counterparty_returns_empty():
    test_input = ([], [])
    test_output = create_dim_counterparty(*test_input)
    assert test_output is None


# returns a dataframe
def test_create_dim_counterparty_returns_dataframe():
    test_input = (
        [
            {
                "counterparty_id": "r1",
                "counterparty_legal_name": "r1",
                "created_at": "r1:12345678910",
                "last_update": "r1",
                "legal_address_id": "r1",
                "commercial_contact": "r1",
                "delivery_contact": "r1",
            },
            {
                "counterparty_id": "r2",
                "counterparty_legal_name": "r2",
                "created_at": "r2:12345678910",
                "last_update": "r2",
                "legal_address_id": "r2",
                "commercial_contact": "r2",
                "delivery_contact": "r2",
            },
        ],
        [
            {
                "address_id": "r1",
                "address_line_1": "r1",
                "address_line_2": "r1",
                "district": "r1",
                "city": "r1",
                "postal_code": "r1",
                "country": "r1",
                "phone": "r1",
                "created_at": "r1",
                "last_update": "r1",
            },
            {
                "address_id": "r2",
                "address_line_1": "r2",
                "address_line_2": "r2",
                "district": "r2",
                "city": "r2",
                "postal_code": "r2",
                "country": "r2",
                "phone": "r2",
                "created_at": "r2",
                "last_update": "r2",
            },
        ],
    )
    test_output = create_dim_counterparty(*test_input)
    assert isinstance(test_output, pd.DataFrame)


# returns a dataframe with correct columns
def test_create_dim_counterparty_returns_dataframe_with_cols():
    test_input = (
        [
            {
                "counterparty_id": "r1",
                "counterparty_legal_name": "r1",
                "created_at": "r1:12345678910",
                "last_update": "r1",
                "legal_address_id": "r1",
                "commercial_contact": "r1",
                "delivery_contact": "r1",
            },
            {
                "counterparty_id": "r2",
                "counterparty_legal_name": "r2",
                "created_at": "r2:12345678910",
                "last_update": "r2",
                "legal_address_id": "r2",
                "commercial_contact": "r2",
                "delivery_contact": "r2",
            },
        ],
        [
            {
                "address_id": "r1",
                "address_line_1": "r1",
                "address_line_2": "r1",
                "district": "r1",
                "city": "r1",
                "postal_code": "r1",
                "country": "r1",
                "phone": "r1",
                "created_at": "r1",
                "last_update": "r1",
            },
            {
                "address_id": "r2",
                "address_line_1": "r2",
                "address_line_2": "r2",
                "district": "r2",
                "city": "r2",
                "postal_code": "r2",
                "country": "r2",
                "phone": "r2",
                "created_at": "r2",
                "last_update": "r2",
            },
        ],
    )
    test_output = create_dim_counterparty(*test_input)
    assert test_output.columns.to_list() == [
        "counterparty_id",
        "counterparty_legal_name",
        "counterparty_legal_address_line_1",
        "counterparty_legal_address_line_2",
        "counterparty_legal_district",
        "counterparty_legal_city",
        "counterparty_legal_postal_code",
        "counterparty_legal_country",
        "counterparty_legal_phone_number",
    ]


# returns a dataframe with multiple rows
def test_create_dim_counterparty_returns_dataframe_with_rows():
    test_input = (
        [
            {
                "counterparty_id": "r1",
                "counterparty_legal_name": "r1",
                "created_at": "r1:12345678910",
                "last_update": "r1",
                "legal_address_id": "r1",
                "commercial_contact": "r1",
                "delivery_contact": "r1",
            },
            {
                "counterparty_id": "r2",
                "counterparty_legal_name": "r2",
                "created_at": "r2:12345678910",
                "last_update": "r2",
                "legal_address_id": "r2",
                "commercial_contact": "r2",
                "delivery_contact": "r2",
            },
        ],
        [
            {
                "address_id": "r1",
                "address_line_1": "r1",
                "address_line_2": "r1",
                "district": "r1",
                "city": "r1",
                "postal_code": "r1",
                "country": "r1",
                "phone": "r1",
                "created_at": "r1",
                "last_update": "r1",
            },
            {
                "address_id": "r2",
                "address_line_1": "r2",
                "address_line_2": "r2",
                "district": "r2",
                "city": "r2",
                "postal_code": "r2",
                "country": "r2",
                "phone": "r2",
                "created_at": "r2",
                "last_update": "r2",
            },
        ],
    )
    test_output = create_dim_counterparty(*test_input)
    expected_output = pd.DataFrame(
        {
            "counterparty_id": ["r1", "r2"],
            "counterparty_legal_name": ["r1", "r2"],
            "counterparty_legal_address_line_1": ["r1", "r2"],
            "counterparty_legal_address_line_2": ["r1", "r2"],
            "counterparty_legal_district": ["r1", "r2"],
            "counterparty_legal_city": ["r1", "r2"],
            "counterparty_legal_postal_code": ["r1", "r2"],
            "counterparty_legal_country": ["r1", "r2"],
            "counterparty_legal_phone_number": ["r1", "r2"],
        }
    )
    pd.testing.assert_frame_equal(test_output, expected_output)


def test_create_dim_counterparty_with_one_table_outputs_none():
    test_input = (
        [
            {
                "counterparty_id": "r1",
                "counterparty_legal_name": "r1",
                "created_at": "r1:12345678910",
                "last_update": "r1",
                "legal_address_id": "r1",
                "commercial_contact": "r1",
                "delivery_contact": "r1",
            },
            {
                "counterparty_id": "r2",
                "counterparty_legal_name": "r2",
                "created_at": "r2:12345678910",
                "last_update": "r2",
                "legal_address_id": "r2",
                "commercial_contact": "r2",
                "delivery_contact": "r2",
            },
        ],
        [],
    )
    test_output = create_dim_counterparty(*test_input)
    assert test_output is None
