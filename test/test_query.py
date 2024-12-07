import pytest
from query import run_query
from conn import create_conn, close_conn
from datetime import datetime
from pg8000 import DatabaseError
import boto3
import os


@pytest.fixture(scope="class", autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    os.environ["S3_LANDING_BUCKET_NAME"] = "test"


@pytest.fixture(scope="session")
def db():
    client = boto3.client("secretsmanager")
    secret_id = "totesys_db_credentials"
    test_db = create_conn(client, secret_id)
    yield test_db
    close_conn(test_db)


def test_if_query_returns_list_of_dicts(db):
    new_db = db
    output = run_query("SELECT * FROM payment_type;", new_db)
    assert isinstance(output, list)
    for item in output:
        assert isinstance(item, dict)


def test_query_dict_has_correct_keys(db):
    test_keys = ["payment_type_id", "payment_type_name",
                 "created_at", "last_updated"]
    output = run_query("SELECT * FROM payment_type LIMIT 1;", db)
    for test, key in zip(test_keys, output[0].keys()):
        assert test == key


def test_query_data_is_correct_types(db):
    output = run_query("SELECT * FROM payment_type LIMIT 1;", db)
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    created_at = output[0]["created_at"]
    last_updated = output[0]["last_updated"]
    assert isinstance(int(output[0]["payment_type_id"]), int)
    assert isinstance(output[0]["payment_type_name"], str)
    assert isinstance(datetime.strptime(created_at, date_format), datetime)
    assert isinstance(datetime.strptime(last_updated, date_format), datetime)


def test_query_returns_exception_for_bad_query(db):
    with pytest.raises(DatabaseError):
        run_query("SELECT * FROM *", db)
