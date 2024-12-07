""" Contains procesing/transforming lambda handler"""

import os
import logging
import boto3
from datetime import datetime
from transform_create_dim_counterparty import create_dim_counterparty
from transform_create_dim_currency import create_dim_currency
from transform_create_dim_dates import create_dim_dates
from transform_create_dim_design import create_dim_design
from transform_create_dim_location import create_dim_location
from transform_create_dim_staff import create_dim_staff
from transform_create_fact_sales import create_fact_sales
from transform_read_file import read_file
from upload_to_s3 import upload_to_s3


logger = logging.getLogger("lambda_logs")
logger.setLevel(logging.INFO)


def lambda_handler_transform(event, context):
    """Take ingested data and processes into star schema and outputs parquet"""
    try:
        # Get newest file from bucket and read json file to a dictionary.
        client = boto3.client("s3")
        landing_bucket_name = os.environ.get("S3_LANDING_BUCKET_NAME")
        read_data = read_file(client, landing_bucket_name)

        # Feed input tables into relevent function to reformat to output table
        dataframes_dict = {
            "counterparty": create_dim_counterparty(
                read_data[0]["counterparty"], read_data[6]["address"]
            ),
            "currency": create_dim_currency(read_data[1]["currency"]),
            "date": create_dim_dates(read_data[5]["sales_order"]),
            "design": create_dim_design(read_data[3]["design"]),
            "location": create_dim_location(
                read_data[6]["address"], read_data[5]["sales_order"]
            ),
            "staff": create_dim_staff(
                read_data[4]["staff"], read_data[2]["department"]
            ),
            "fact_sales": create_fact_sales(read_data[5]["sales_order"]),
        }
        # Convert each into parquet and save to bucket
        transform_bucket_name = os.environ.get("S3_TRANSFORM_BUCKET_NAME")
        timestamp = datetime.now().isoformat()
        response = None
        for key, value in dataframes_dict.items():
            if value is not None:
                pq_data = value.to_parquet()
                file_name = f"{timestamp}/{key}.parquet"
                response = upload_to_s3(
                    client, pq_data, transform_bucket_name, file_name
                )
        if response:
            logger.info({"result": "SUCCESS", "message": response})
        else:
            logger.info(
                {
                    "result": "SUCCESS",
                    "message": 'succesfully ran, '
                    'no new data for "Sales" schema'
                }
            )
    except Exception as e:
        logger.info({"result": "FAILURE", "error": e})
