"""Module contains a function to obtain a secret from AWS secrets manager"""

import json
from botocore.exceptions import ClientError


def get_secret(client, secret_id):
    """returns secret details as a dict from AWS secrets manager"""
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_id)
    except ClientError as e:
        raise e
    secret_string = get_secret_value_response["SecretString"]
    secret_dict = json.loads(secret_string)
    return secret_dict
