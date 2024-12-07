"""Module contains a function to check the most recently updated data"""

from datetime import datetime
from dateutil.tz import tzutc


def get_most_recent_dl(s3_client, bucket_name):
    """returns a SQL "WHERE" clause based on the most recently ingested data"""
    bucket_list = s3_client.list_objects_v2(Bucket=bucket_name)
    timestamp = datetime(2015, 1, 1, 1, 1, 1, tzinfo=tzutc())
    where_statement = ""
    if "Contents" in bucket_list.keys():
        for content in bucket_list["Contents"]:
            if content["LastModified"] > timestamp:
                timestamp = content["LastModified"]
        where_statement += (
            f"WHERE last_updated > "
            f"'{timestamp.strftime('%Y-%m-%d %H:%M:%S')}'"
        )
    return where_statement
