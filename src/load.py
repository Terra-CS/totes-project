from load_get_new_keys import get_new_keys
from load_create_tables import create_tables
from load_conn_engine import create_conn_for_engine
from load_to_db import load_to_db
import os
import logging
import boto3

logger = logging.getLogger("lambda_logs")
logger.setLevel(logging.INFO)


def lambda_handler_load(event, context):
    try:
        secret_client = boto3.client("secretsmanager")
        engine = create_conn_for_engine(secret_client)
        s3_client = boto3.client("s3")
        bucket_name = os.environ.get("S3_TRANSFORM_BUCKET_NAME")
        table_keys = get_new_keys(s3_client, bucket_name)
        table_list = create_tables(s3_client, bucket_name, table_keys)
        if table_list:
            message = load_to_db(table_list, engine)
            logger.info({"result": "SUCCESS", "message": message})
    except Exception as e:
        logger.info({"result": "FAILURE", "error": e})
