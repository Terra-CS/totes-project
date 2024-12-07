"""Module contains functions for creating and closing a db connection"""
import sqlalchemy
from secret import get_secret


# Connects to RDS - uses warehouse secret
def create_conn_for_engine(client):
    """Creates a db connection using credentials from AWS secretsmanager"""
    secret = get_secret(client, 'project_dw_credentials')
    db_user = secret["username"]
    db = secret["dbname"]
    db_pass = secret["password"]
    db_host = secret["host"]
    db_port = int(secret["port"])

    # Writes the string to use sqlalchemy
    conn_str = ("postgresql+pg8000://" +
                f"{db_user}:{db_pass}@{db_host}:{db_port}/{db}")
    engine = sqlalchemy.create_engine(conn_str)

    # Returns the engine cretaed for sqlalchemy
    return engine


def close_conn_for_engine(engine):
    """Closes an open db connection"""
    engine.dispose()
