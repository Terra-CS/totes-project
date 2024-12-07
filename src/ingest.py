"""This module contains the main ingestion lambda handler"""

import os
import json
import logging
from datetime import datetime
import boto3
from conn import create_conn, close_conn
from query import run_query
from upload_to_s3 import upload_to_s3
from get_most_recent_dl import get_most_recent_dl


logger = logging.getLogger("lambda_logs")
logger.setLevel(logging.INFO)


def lambda_handler_ingestion(event, context):
    """Extracts new totesys data and stores as json in an s3"""
    conn = False
    tables = [
        "counterparty",
        "currency",
        "department",
        "design",
        "staff",
        "sales_order",
        "address",
        "payment",
        "purchase_order",
        "payment_type",
        "transaction",
    ]
    try:
        data = []
        client = boto3.client("s3")
        secret_client = boto3.client("secretsmanager")
        conn = create_conn(secret_client, "totesys_db_credentials")
        bucket_name = os.environ.get("S3_LANDING_BUCKET_NAME")
        where_statement = get_most_recent_dl(client, bucket_name)

        for table in tables:
            query = f"SELECT * FROM {table} {where_statement};"
            table_data = run_query(query, conn)
            data.append({table: table_data})
        for data_tables in data:
            if any(data_tables.values()):
                json_data = json.dumps(data)
                file_name = f"{datetime.now().isoformat()}.json"
                response = upload_to_s3(client, json_data,
                                        bucket_name, file_name)
                logger.info({"result": "SUCCESS", "message": response})
                return
        logger.info(
            {"result": "SUCCESS",
             "message": f"nothing to upload at {datetime.now()}"}
        )
    except Exception as e:
        logger.info({"result": "FAILURE", "error": e})

    finally:
        if conn:
            close_conn(conn)
