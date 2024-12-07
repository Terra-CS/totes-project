"""Contains a function to write data as an object to an S3 bucket"""

from datetime import datetime


def upload_to_s3(s3_client, data, bucket_name, file_name):
    """writes data as an object in an S3 bucket"""
    try:
        now = datetime.now()
        folder_name = f"{now.year}/{now.month}/{now.day}"
        s3_client.put_object(
            Bucket=bucket_name, Key=f"{folder_name}/{file_name}", Body=data
        )
        return f"uploaded to {bucket_name}"
    except Exception as e:
        print(f"error: {e}")
        raise e
