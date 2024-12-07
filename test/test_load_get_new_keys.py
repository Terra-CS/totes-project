import os
import boto3
import pytest
from moto import mock_aws
from freezegun import freeze_time
from load_get_new_keys import get_new_keys


@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    os.environ["S3_LANDING_BUCKET_NAME"] = "test"


@mock_aws
@freeze_time("2024-11-10")
def make_old_bucket(aws_credentials):
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="test",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
    )
    s3.put_object(
        Bucket="test",
        Key="2024/11/10/123456789123456789123456789/test_key1",
        Body="test",
    )
    s3.put_object(
        Bucket="test",
        Key="2024/11/09/123456789123456789123456789/test_key2",
        Body="test",
    )
    return s3


# test returns empty list for no objects in last 15 minutes
@mock_aws
@freeze_time("2024-11-11")
def test_get_new_keys_returns_empty_list_for_no_objects_in_last_15_mins():
    client = make_old_bucket(aws_credentials)
    output = get_new_keys(client, "test")
    assert output == []


# test returns list of correct key for one object in last 15 minutes
@mock_aws
@freeze_time("2024-11-10")
def test_get_new_keys_returns_list_for_one_object_in_last_15_mins():
    client = make_old_bucket(aws_credentials)
    output = get_new_keys(client, "test")
    assert output == ["2024/11/10/123456789123456789123456789/test_key1"]


# test returns list of correct keys for multiple objects in last 15 minutes
@mock_aws
@freeze_time("2024-11-10")
def test_get_new_keys_returns_list_for_multiple_objects_in_last_15_minutes(
    aws_credentials,
):
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="test",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
    )
    s3.put_object(
        Bucket="test",
        Key="2024/11/10/123456789123456789123456789/test_key1",
        Body="test",
    )
    s3.put_object(
        Bucket="test",
        Key="2024/11/10/123456789123456789123456789/test_key2",
        Body="test",
    )
    s3.put_object(
        Bucket="test",
        Key="2023/11/10/123456789123456789123456789/test_key3",
        Body="test",
    )
    s3.put_object(
        Bucket="test",
        Key="2024/11/10/123456789123456789123456789/test_key4",
        Body="test",
    )
    output = get_new_keys(s3, "test")
    assert output == [
        "2024/11/10/123456789123456789123456789/test_key1",
        "2024/11/10/123456789123456789123456789/test_key2",
        "2024/11/10/123456789123456789123456789/test_key4",
    ]
