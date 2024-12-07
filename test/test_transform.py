import os
import pytest
import boto3
import json
from moto import mock_aws
from transform import lambda_handler_transform
from unittest import TestCase
from datetime import datetime


@pytest.fixture(scope="class", autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    os.environ["S3_LANDING_BUCKET_NAME"] = "test_landing"
    os.environ["S3_TRANSFORM_BUCKET_NAME"] = "test_processed"


@mock_aws
class TestProcessLambdaHandler(TestCase):
    def test_uploads_parquet_files_to_transform_bucket(self):
        # ARRANGE: create landing and processed buckets
        client = boto3.client("s3")
        client.create_bucket(
            Bucket="test_landing",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        client.create_bucket(
            Bucket="test_processed",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # ARRANGE: upload test data file to landing bucket
        test_data = [
            {"counterparty": []},
            {"currency": []},
            {"department": []},
            {"design": []},
            {"staff": []},
            {
                "sales_order": [
                    {
                        "sales_order_id": "11224",
                        "created_at": "2024-11-19 11:18:10.223000",
                        "last_updated": "2024-11-19 11:18:10.223000",
                        "design_id": "69",
                        "staff_id": "10",
                        "counterparty_id": "3",
                        "units_sold": "91067",
                        "unit_price": "3.44",
                        "currency_id": "3",
                        "agreed_delivery_date": "2024-11-24",
                        "agreed_payment_date": "2024-11-22",
                        "agreed_delivery_location_id": "30",
                    },
                    {
                        "sales_order_id": "11225",
                        "created_at": "2024-11-19 11:20:09.854000",
                        "last_updated": "2024-11-19 11:20:09.854000",
                        "design_id": "233",
                        "staff_id": "16",
                        "counterparty_id": "6",
                        "units_sold": "72419",
                        "unit_price": "3.38",
                        "currency_id": "2",
                        "agreed_delivery_date": "2024-11-26",
                        "agreed_payment_date": "2024-11-24",
                        "agreed_delivery_location_id": "18",
                    },
                ]
            },
            {"address": []},
            {
                "payment": [
                    {
                        "payment_id": "15886",
                        "created_at": "2024-11-19 11:18:10.223000",
                        "last_updated": "2024-11-19 11:18:10.223000",
                        "transaction_id": "15886",
                        "counterparty_id": "3",
                        "payment_amount": "313270.48",
                        "currency_id": "3",
                        "payment_type_id": "1",
                        "paid": "False",
                        "payment_date": "2024-11-22",
                        "company_ac_number": "85837294",
                        "counterparty_ac_number": "78731588",
                    },
                    {
                        "payment_id": "15887",
                        "created_at": "2024-11-19 11:20:09.854000",
                        "last_updated": "2024-11-19 11:20:09.854000",
                        "transaction_id": "15887",
                        "counterparty_id": "6",
                        "payment_amount": "244776.22",
                        "currency_id": "2",
                        "payment_type_id": "1",
                        "paid": "False",
                        "payment_date": "2024-11-24",
                        "company_ac_number": "73587735",
                        "counterparty_ac_number": "35512228",
                    },
                    {
                        "payment_id": "15888",
                        "created_at": "2024-11-19 11:23:09.852000",
                        "last_updated": "2024-11-19 11:23:09.852000",
                        "transaction_id": "15888",
                        "counterparty_id": "6",
                        "payment_amount": "120963.12",
                        "currency_id": "1",
                        "payment_type_id": "3",
                        "paid": "False",
                        "payment_date": "2024-11-23",
                        "company_ac_number": "42045804",
                        "counterparty_ac_number": "60776468",
                    },
                ]
            },
            {
                "purchase_order": [
                    {
                        "purchase_order_id": "4663",
                        "created_at": "2024-11-19 11:23:09.852000",
                        "last_updated": "2024-11-19 11:23:09.852000",
                        "staff_id": "2",
                        "counterparty_id": "6",
                        "item_code": "79FJTUD",
                        "item_quantity": "984",
                        "item_unit_price": "122.93",
                        "currency_id": "1",
                        "agreed_delivery_date": "2024-11-23",
                        "agreed_payment_date": "2024-11-23",
                        "agreed_delivery_location_id": "1",
                    }
                ]
            },
            {"payment_type": []},
            {
                "transaction": [
                    {
                        "transaction_id": "15886",
                        "transaction_type": "SALE",
                        "sales_order_id": "11224",
                        "purchase_order_id": "None",
                        "created_at": "2024-11-19 11:18:10.223000",
                        "last_updated": "2024-11-19 11:18:10.223000",
                    },
                    {
                        "transaction_id": "15887",
                        "transaction_type": "SALE",
                        "sales_order_id": "11225",
                        "purchase_order_id": "None",
                        "created_at": "2024-11-19 11:20:09.854000",
                        "last_updated": "2024-11-19 11:20:09.854000",
                    },
                    {
                        "transaction_id": "15888",
                        "transaction_type": "PURCHASE",
                        "sales_order_id": "None",
                        "purchase_order_id": "4663",
                        "created_at": "2024-11-19 11:23:09.852000",
                        "last_updated": "2024-11-19 11:23:09.852000",
                    },
                ]
            },
        ]
        json_test_data = json.dumps(test_data)
        now = datetime.now()
        key = f"{now.year}/{now.month}/{now.day}/{now.isoformat()}.json"
        client.put_object(Bucket="test_landing", Key=key, Body=json_test_data)
        # ACT: run process lambda handler
        with self.assertLogs("lambda_logs") as logger:
            lambda_handler_transform("", "")
            self.assertEqual(
                "INFO:lambda_logs:{'result': 'SUCCESS',"
                " 'message': 'uploaded to test_processed'}",
                logger.output[0],
            )
        # ASSERT: files uploaded and in parquet format
        processed_files = client.list_objects_v2(Bucket="test_processed")
        assert len(processed_files["Contents"]) > 0
        for file in processed_files["Contents"]:
            assert file["Key"][-8:] == ".parquet"

    def test_nothing_uploaded_if_no_new_data(self):
        # ARRANGE: create landing and processed buckets
        client = boto3.client("s3")
        client.create_bucket(
            Bucket="test_landing",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        client.create_bucket(
            Bucket="test_processed",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # ARRANGE: upload no sales test data file to landing bucket
        test_data = [
            {"counterparty": []},
            {"currency": []},
            {"department": []},
            {"design": []},
            {"staff": []},
            {"sales_order": []},
            {"address": []},
            {
                "payment": [
                    {
                        "payment_id": "15972",
                        "created_at": "2024-11-21 13:05:09.864000",
                        "last_updated": "2024-11-21 13:05:09.864000",
                        "transaction_id": "15972",
                        "counterparty_id": "8",
                        "payment_amount": "60489.40",
                        "currency_id": "1",
                        "payment_type_id": "3",
                        "paid": "False",
                        "payment_date": "2024-11-26",
                        "company_ac_number": "73772083",
                        "counterparty_ac_number": "48426610",
                    }
                ]
            },
            {
                "purchase_order": [
                    {
                        "purchase_order_id": "4690",
                        "created_at": "2024-11-21 13:05:09.864000",
                        "last_updated": "2024-11-21 13:05:09.864000",
                        "staff_id": "14",
                        "counterparty_id": "8",
                        "item_code": "ENLQ6RX",
                        "item_quantity": "170",
                        "item_unit_price": "355.82",
                        "currency_id": "1",
                        "agreed_delivery_date": "2024-11-22",
                        "agreed_payment_date": "2024-11-26",
                        "agreed_delivery_location_id": "7",
                    }
                ]
            },
            {"payment_type": []},
            {
                "transaction": [
                    {
                        "transaction_id": "15972",
                        "transaction_type": "PURCHASE",
                        "sales_order_id": "None",
                        "purchase_order_id": "4690",
                        "created_at": "2024-11-21 13:05:09.864000",
                        "last_updated": "2024-11-21 13:05:09.864000",
                    }
                ]
            },
        ]
        json_test_data = json.dumps(test_data)
        now = datetime.now()
        key = f"{now.year}/{now.month}/{now.day}/{now.isoformat()}.json"
        client.put_object(Bucket="test_landing", Key=key, Body=json_test_data)
        # ACT: run process lambda handler
        with self.assertLogs("lambda_logs") as logger:
            lambda_handler_transform("", "")
            self.assertEqual(
                "INFO:lambda_logs:{'result': 'SUCCESS', 'message': "
                "'succesfully ran, no new data for \"Sales\" schema'}",
                logger.output[0],
            )
        # ASSERT: files uploaded and in parquet format
        processed_files = client.list_objects_v2(Bucket="test_processed")
        assert "Contents" not in processed_files.keys()

    def test_raises_errors(self):
        # ARRANGE: create landing but NOT processed buckets
        client = boto3.client("s3")
        client.create_bucket(
            Bucket="test_landing",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        test_data = [
            {"counterparty": []},
            {"currency": []},
            {"department": []},
            {"design": []},
            {"staff": []},
            {
                "sales_order": [
                    {
                        "sales_order_id": "11224",
                        "created_at": "2024-11-19 11:18:10.223000",
                        "last_updated": "2024-11-19 11:18:10.223000",
                        "design_id": "69",
                        "staff_id": "10",
                        "counterparty_id": "3",
                        "units_sold": "91067",
                        "unit_price": "3.44",
                        "currency_id": "3",
                        "agreed_delivery_date": "2024-11-24",
                        "agreed_payment_date": "2024-11-22",
                        "agreed_delivery_location_id": "30",
                    },
                    {
                        "sales_order_id": "11225",
                        "created_at": "2024-11-19 11:20:09.854000",
                        "last_updated": "2024-11-19 11:20:09.854000",
                        "design_id": "233",
                        "staff_id": "16",
                        "counterparty_id": "6",
                        "units_sold": "72419",
                        "unit_price": "3.38",
                        "currency_id": "2",
                        "agreed_delivery_date": "2024-11-26",
                        "agreed_payment_date": "2024-11-24",
                        "agreed_delivery_location_id": "18",
                    },
                ]
            },
            {"address": []},
            {
                "payment": [
                    {
                        "payment_id": "15886",
                        "created_at": "2024-11-19 11:18:10.223000",
                        "last_updated": "2024-11-19 11:18:10.223000",
                        "transaction_id": "15886",
                        "counterparty_id": "3",
                        "payment_amount": "313270.48",
                        "currency_id": "3",
                        "payment_type_id": "1",
                        "paid": "False",
                        "payment_date": "2024-11-22",
                        "company_ac_number": "85837294",
                        "counterparty_ac_number": "78731588",
                    },
                    {
                        "payment_id": "15887",
                        "created_at": "2024-11-19 11:20:09.854000",
                        "last_updated": "2024-11-19 11:20:09.854000",
                        "transaction_id": "15887",
                        "counterparty_id": "6",
                        "payment_amount": "244776.22",
                        "currency_id": "2",
                        "payment_type_id": "1",
                        "paid": "False",
                        "payment_date": "2024-11-24",
                        "company_ac_number": "73587735",
                        "counterparty_ac_number": "35512228",
                    },
                    {
                        "payment_id": "15888",
                        "created_at": "2024-11-19 11:23:09.852000",
                        "last_updated": "2024-11-19 11:23:09.852000",
                        "transaction_id": "15888",
                        "counterparty_id": "6",
                        "payment_amount": "120963.12",
                        "currency_id": "1",
                        "payment_type_id": "3",
                        "paid": "False",
                        "payment_date": "2024-11-23",
                        "company_ac_number": "42045804",
                        "counterparty_ac_number": "60776468",
                    },
                ]
            },
            {
                "purchase_order": [
                    {
                        "purchase_order_id": "4663",
                        "created_at": "2024-11-19 11:23:09.852000",
                        "last_updated": "2024-11-19 11:23:09.852000",
                        "staff_id": "2",
                        "counterparty_id": "6",
                        "item_code": "79FJTUD",
                        "item_quantity": "984",
                        "item_unit_price": "122.93",
                        "currency_id": "1",
                        "agreed_delivery_date": "2024-11-23",
                        "agreed_payment_date": "2024-11-23",
                        "agreed_delivery_location_id": "1",
                    }
                ]
            },
            {"payment_type": []},
            {
                "transaction": [
                    {
                        "transaction_id": "15886",
                        "transaction_type": "SALE",
                        "sales_order_id": "11224",
                        "purchase_order_id": "None",
                        "created_at": "2024-11-19 11:18:10.223000",
                        "last_updated": "2024-11-19 11:18:10.223000",
                    },
                    {
                        "transaction_id": "15887",
                        "transaction_type": "SALE",
                        "sales_order_id": "11225",
                        "purchase_order_id": "None",
                        "created_at": "2024-11-19 11:20:09.854000",
                        "last_updated": "2024-11-19 11:20:09.854000",
                    },
                    {
                        "transaction_id": "15888",
                        "transaction_type": "PURCHASE",
                        "sales_order_id": "None",
                        "purchase_order_id": "4663",
                        "created_at": "2024-11-19 11:23:09.852000",
                        "last_updated": "2024-11-19 11:23:09.852000",
                    },
                ]
            },
        ]
        json_test_data = json.dumps(test_data)
        now = datetime.now()
        key = f"{now.year}/{now.month}/{now.day}/{now.isoformat()}.json"
        client.put_object(Bucket="test_landing", Key=key, Body=json_test_data)

        # ACT & ASSERT: running process lambda handler raises error
        with self.assertLogs("lambda_logs") as logger:
            lambda_handler_transform("", "")
            self.assertEqual(
                "INFO:lambda_logs:{'result': 'FAILURE', 'error':"
                " NoSuchBucket('An error occurred (NoSuchBucket) "
                "when calling the PutObject operation:"
                " The specified bucket does not exist')}",
                logger.output[0],
            )
