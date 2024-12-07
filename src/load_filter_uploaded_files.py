"""This module contains a function that checks
which files have been uploaded"""

import boto3


# first listobjectv2 and get Contents list as file_keys
def filter_uploaded_files(file_keys):
    """Compares a list of s3 objects against dynamoDB record
    of uploaded objects, returning sublist of objects to upload"""
    # connect to a dynamodb table that tracks
    # which files have been uploaded
    dynamodb = boto3.client("dynamodb")

    new_files_list = []
    try:
        for file in file_keys:
            response = dynamodb.get_item(
                table_name="UploadedFiles", Key={"FileKey": {"S": file}}
            )
            if "Item" not in response:
                new_files_list.append(file)
    except Exception as e:
        raise e
    finally:
        return new_files_list
