from secret import get_secret
from moto import mock_aws
import boto3
import os
import pytest
import json


@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    os.environ["S3_LANDING_BUCKET_NAME"] = "test"


@mock_aws
def test_get_secret_retrieves_secret():
    client = boto3.client("secretsmanager")
    secret_id = "totesys_db_credentials"
    test_dict = {"test": "test"}
    formated_dict = json.dumps(test_dict)
    client.create_secret(Name="totesys_db_credentials",
                         SecretString=formated_dict)
    assert get_secret(client, secret_id) == test_dict
