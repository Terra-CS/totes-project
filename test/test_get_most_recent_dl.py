import os
import boto3
import pytest
from moto import mock_aws
from freezegun import freeze_time
from get_most_recent_dl import get_most_recent_dl


@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    os.environ["S3_LANDING_BUCKET_NAME"] = "test"


@mock_aws
@freeze_time("2024-11-18")
def test_upload_to_s3_returns_str(aws_credentials):
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="test", CreateBucketConfiguration={"LocationConstraint":
                                                  "eu-west-2"}
    )
    s3.put_object(Bucket="test", Key="test", Body="test")
    result = get_most_recent_dl(s3, "test")

    assert result[:32] == "WHERE last_updated > '2024-11-18"
