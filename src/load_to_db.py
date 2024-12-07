"""This module contains a function which takes a list of dataframes
and uploads the data within to a data warehouse"""
from upsert_dim_tables import upsert_dim_tables


def load_to_db(df_list, engine):
    try:
        for df in df_list:
            primary_key = df.columns[0]
            if primary_key == "sales_order_id":
                # upload_fact()
                table_name = "fact_sales_order"
                df.to_sql(table_name, engine, if_exists="append", index=False)
            else:
                upsert_dim_tables(df, primary_key, engine.connect())
        return "data uploaded to the data warehouse"
    except Exception as e:
        raise e
