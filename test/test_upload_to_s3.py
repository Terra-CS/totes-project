import os
import boto3
import pytest
from moto import mock_aws
from upload_to_s3 import upload_to_s3


@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    os.environ["S3_LANDING_BUCKET_NAME"] = "test"


@mock_aws
def test_upload_to_s3_returns_str(aws_credentials):
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="test",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
    )
    result = upload_to_s3(s3, "test_data", "test", "test_name")
    assert isinstance(result, str)
    assert result == "uploaded to test"


@mock_aws
def test_upload_to_s3_uploads_to_the_bucket(aws_credentials):
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="test",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
    )
    upload_to_s3(s3, "test_data", "test", "test_name")
    object_list = s3.list_objects(Bucket="test")
    assert len(object_list["Contents"]) == 1


@mock_aws
def test_upload_to_s3_returns_error_message(aws_credentials):
    s3 = boto3.client("s3")
    with pytest.raises(Exception):
        upload_to_s3(s3, "test_data", "test", "test_name")
