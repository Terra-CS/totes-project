from ingest import lambda_handler_ingestion
from secret import get_secret
from moto import mock_aws
import boto3
import os
import pytest
from unittest import TestCase
import json


@pytest.fixture(scope="class", autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    os.environ["S3_LANDING_BUCKET_NAME"] = "test"


client = boto3.client("secretsmanager")
secret_id = "totesys_db_credentials"
access = get_secret(client, secret_id)


@mock_aws
class TestExtractLambdaHandler(TestCase):
    def test_lambda_handler_raises_exceptiion(self):
        # ARRANGE
        secret_client = boto3.client("secretsmanager")
        access_json = json.dumps(access)
        secret_client.create_secret(
            Name="totesys_db_credentials", SecretString=access_json
        )
        # ACT AND ASSERT
        with self.assertLogs("lambda_logs") as logger:
            lambda_handler_ingestion("", "")
            self.assertEqual(
                "INFO:lambda_logs:{'result': 'FAILURE',"
                " 'error': NoSuchBucket('An error occurred (NoSuchBucket)"
                " when calling the ListObjectsV2 operation:"
                " The specified bucket does not exist')}",
                logger.output[0],
            )

    def test_lambda_handler_uploads_to_s3(self):
        # ARRANGE
        client = boto3.client("s3")
        client.create_bucket(
            Bucket="test",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
        )
        secret_client = boto3.client("secretsmanager")
        access_json = json.dumps(access)
        secret_client.create_secret(
            Name="totesys_db_credentials", SecretString=access_json
        )
        # ACT AND ASSERT
        with self.assertLogs("lambda_logs") as logger:
            lambda_handler_ingestion("", "")
            self.assertEqual(
                "INFO:lambda_logs:{'result': 'SUCCESS',"
                " 'message': 'uploaded to test'}",
                logger.output[0],
            )
        object_list = client.list_objects_v2(Bucket="test")
        assert len(object_list["Contents"]) == 1

    def test_lambda_handler_doesnt_upload_no_changes(self):
        # ARRANGE
        s3_client = boto3.client("s3")
        s3_client.create_bucket(
            Bucket="test",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
        )
        s3_client.put_object(Bucket="test", Key="test", Body="test")
        secret_client = boto3.client("secretsmanager")
        access_json = json.dumps(access)
        secret_client.create_secret(
            Name="totesys_db_credentials", SecretString=access_json
        )
        # ACT AND ASSERT
        with self.assertLogs("lambda_logs") as logger:
            lambda_handler_ingestion("", "")
            self.assertEqual(
                "INFO:lambda_logs:{'result': 'SUCCESS',"
                " 'message': 'nothing to upload at",
                logger.output[0][:-29],
            )
        object_list = s3_client.list_objects(Bucket="test")
        assert len(object_list["Contents"]) == 1
