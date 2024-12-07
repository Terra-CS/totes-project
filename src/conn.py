"""Module contains functions for creating and closing a db connection"""

from pg8000.native import Connection
from secret import get_secret


def create_conn(client, secret_id):
    """Creates a db connection using credentials from AWS secretsmanager"""
    secret = get_secret(client, secret_id)
    db_user = secret["username"]
    db = secret["dbname"]
    db_pass = secret["password"]
    db_host = secret["host"]
    db_port = int(secret["port"])
    conn = Connection(
        user=db_user, database=db, password=db_pass, host=db_host, port=db_port
    )
    return conn


def close_conn(conn):
    """Closes an open db connection"""
    conn.close()
