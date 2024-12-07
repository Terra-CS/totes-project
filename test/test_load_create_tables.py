import pandas as pd
from load_create_tables import create_tables
from moto import mock_aws
import os
import pytest
import boto3


@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    os.environ["S3_LANDING_BUCKET_NAME"] = "test"


@mock_aws
def test_create_tables_returns_list(aws_credentials):
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="test", CreateBucketConfiguration={"LocationConstraint":
                                                  "eu-west-2"}
    )
    s3.put_object(Bucket="test", Key="test", Body="test")
    test_keys = []
    assert isinstance(create_tables(s3, "test", test_keys), list)


@mock_aws
def test_create_tables_returns_list_of_df(aws_credentials):
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="test", CreateBucketConfiguration={"LocationConstraint":
                                                  "eu-west-2"}
    )
    test_input = pd.DataFrame({"test_data": ["test", "data"]})
    test_parq = test_input.to_parquet()
    s3.put_object(Bucket="test", Key="prefix/fact_table", Body=test_parq)
    s3.put_object(Bucket="test", Key="prefix/dim_table", Body=test_parq)
    test_keys = ["prefix/fact_table", "prefix/dim_table"]
    output = create_tables(s3, "test", test_keys)
    assert len(output) == 2
    for df in output:
        assert isinstance(df, pd.DataFrame)


@mock_aws
def test_create_tables_returns_correct_data(aws_credentials):
    s3 = boto3.client("s3")
    s3.create_bucket(
        Bucket="test", CreateBucketConfiguration={"LocationConstraint":
                                                  "eu-west-2"}
    )
    test_fact = pd.DataFrame({"fact_data": ["fact", "data"]})
    test_dim = pd.DataFrame({"dim_data": ["dim", "data"]})
    test_keys = ["prefix/fact_table", "prefix/dim_table"]
    test_parq = test_fact.to_parquet()
    s3.put_object(Bucket="test", Key=test_keys[0], Body=test_parq)
    test_parq = test_dim.to_parquet()
    s3.put_object(Bucket="test", Key=test_keys[1], Body=test_parq)
    output = create_tables(s3, "test", test_keys)
    assert output[0].equals(test_fact)
    assert output[1].equals(test_dim)
