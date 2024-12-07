from datetime import datetime, timedelta
from dateutil.tz import tzutc


def get_new_keys(client, bucket_name):
    try:
        # lists objects from today and yesterday and lists by last modified
        yesterday = datetime.today() - timedelta(days=1)
        today = datetime.today()
        yesterday_objects = client.list_objects_v2(
            Bucket=bucket_name, Prefix=yesterday.strftime("%Y/%m/%d")
        )
        today_objects = client.list_objects_v2(
            Bucket=bucket_name, Prefix=today.strftime("%Y/%m/%d")
        )
        if (
            "Contents" in yesterday_objects.keys()
            and "Contents" in today_objects.keys()
        ):
            recent_objects = (
                yesterday_objects["Contents"] + today_objects["Contents"])
            recent_objects = (
                yesterday_objects["Contents"]
                + today_objects["Contents"]
                )
        elif "Contents" not in yesterday_objects.keys():
            recent_objects = today_objects["Contents"]
        else:
            recent_objects = yesterday_objects["Contents"]
        latest_modified = recent_objects[-1]["LastModified"]
        fifteen_minutes_ago = datetime.now(tzutc()) - timedelta(minutes=15)
        # if recent object newer than 15 mins, list all keys from this cycle
        if latest_modified > fifteen_minutes_ago:
            most_recent_key = recent_objects[-1]["Key"]
            most_recent_prefix = most_recent_key[:38]
            most_recent_objects = client.list_objects_v2(
                Bucket=bucket_name, Prefix=most_recent_prefix
            )
            keys_list = [object["Key"]
                         for object in most_recent_objects["Contents"]]
        else:
            keys_list = []
        return keys_list
    except Exception as e:
        raise e
