from transform_read_file import read_file
from moto import mock_aws
from datetime import datetime, timedelta
import boto3
import json
import pytest


# Test returns list of dicts.
@mock_aws
def test_read_file_returns_list_of_dicts():
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="test",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
    )
    expected_output = [
        {"table_name": [{"test": "test_value"}, {"test": "test_value2"}]},
        {"table_name": [{"test": "test_value"}, {"test": "test_value2"}]},
    ]
    body = json.dumps(expected_output)
    now = datetime.now()
    key = f"{now.year}/{now.month}/{now.day}/{now.isoformat()}.json"
    s3.put_object(Bucket="test", Key=key, Body=body)
    output = read_file(s3, "test")
    assert isinstance(output, list)
    for item in output:
        assert isinstance(item, dict)


# Test read file doesn't change the data
@mock_aws
def test_read_file_does_not_change_data():
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="test",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
    )
    expected_output = [
        {"table_name": [{"test": "test_value"}, {"test": "test_value2"}]},
        {"table_name": [{"test": "test_value"}, {"test": "test_value2"}]},
    ]
    body = json.dumps(expected_output)
    now = datetime.now()
    key = f"{now.year}/{now.month}/{now.day}/{now.isoformat()}.json"
    s3.put_object(Bucket="test", Key=key, Body=body)
    output = read_file(s3, "test")
    assert output == expected_output


# Test gets most recent file.
@mock_aws
def test_read_file_gets_most_recent_file():
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="test",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
    )

    body_1 = json.dumps("really_wrong_object")
    body_2 = json.dumps("wrong_object")
    body_3 = json.dumps("right_object")

    now = datetime.now() - timedelta(days=2)
    key = f"{now.year}/{now.month}/{now.day}/{now.isoformat()}.json"
    s3.put_object(Bucket="test", Key=key, Body=body_1)
    now = datetime.now() - timedelta(days=1)
    key = f"{now.year}/{now.month}/{now.day}/{now.isoformat()}.json"
    s3.put_object(Bucket="test", Key=key, Body=body_2)
    now = datetime.now()
    key = f"{now.year}/{now.month}/{now.day}/{now.isoformat()}.json"
    s3.put_object(Bucket="test", Key=key, Body=body_3)
    expected_output = "right_object"
    output = read_file(s3, "test")
    assert output == expected_output


# Test raises error
@mock_aws
def test_read_file_raises_error_when_empty_file():
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="test",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
    )
    body = json.dumps([])
    now = datetime.now()
    key = f"{now.year}/{now.month}/{now.day}/{now.isoformat()}.json"
    s3.put_object(Bucket="test", Key=key, Body=body)
    with pytest.raises(Exception) as e:
        read_file(s3, "test")
        print(e)
    assert str(e.value) == "no data found in json"
