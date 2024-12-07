"""This module contains a function that runs
an upsert query for tables in the data warehouse"""
from sqlalchemy import text

def upsert_dim_tables(df, primary_key, conn):
    table_name = "dim_" + primary_key[:-3]

    for _, row in df.iterrows():
        # get column, values by row to use for insertion to the db
        columns = ",".join(df.columns)
        values = ",".join(
            f"'{value}'"
            if isinstance(value, str) else str(value) for value in row
        )

        # get column, value excluding primary key column, value
        # if we need to update
        columns_excl_primary_key = [
            column for column in df.columns if column != primary_key
        ]
        values_excl_primary_key = [
            value for column, value in row.items() if column != primary_key
        ]
        update_data = zip(columns_excl_primary_key, values_excl_primary_key)

        # create UPDATE SET string based on updated data
        # for existing primary_key
        update_string = ", ".join(
            [f"{column}={repr(value)}" for column, value in update_data]
        )

        # set up universal SQL query
        upsert_query = f"""
                INSERT INTO {table_name} ({columns})
                VALUES ({values})
                ON CONFLICT ({primary_key}) DO UPDATE SET
                {update_string}
                """
        conn.execute(text(upsert_query))
    conn.commit()
    return "Data uploaded to the data warehouse"
