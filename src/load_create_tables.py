import pandas as pd
import io


def create_tables(client, bucket_name, key_list):
    table_list = []
    if key_list:
        for key in key_list:
            table_parq = client.get_object(Bucket=bucket_name, Key=key)
            file_content = io.BytesIO(table_parq["Body"].read())
            table_df = pd.read_parquet(file_content)
            table_list.append(table_df)
    return table_list
