"""Contains a function that finds the most
recently created object in an S3 bucket"""

import json
from datetime import datetime, timedelta


def read_file(client, bucket_name):
    """Finds most recent object and returns its content"""
    try:
        yesterday = datetime.today() - timedelta(days=1)
        today = datetime.today()
        yesterday_objects = client.list_objects_v2(
            Bucket=bucket_name, Prefix=yesterday.strftime("%Y/%m/%d")
        )
        today_objects = client.list_objects_v2(
            Bucket=bucket_name, Prefix=today.strftime("%Y/%m/%d")
        )
        if "Contents" in yesterday_objects.keys():
            recent_objects = (yesterday_objects["Contents"]
                              + today_objects["Contents"])
        else:
            recent_objects = today_objects["Contents"]
        most_recent_key = recent_objects[-1]["Key"]
        most_recent_object = client.get_object(Bucket=bucket_name,
                                               Key=most_recent_key)
        file_content = most_recent_object["Body"].read().decode("utf-8")
        json_file_content = json.loads(file_content)
        if json_file_content:
            return json_file_content
        else:
            raise Exception("no data found in json")
    except Exception as e:
        raise e
