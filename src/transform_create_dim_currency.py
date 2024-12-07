"""This module contains a function which transforms
extracted currency data into a df"""

import pandas as pd
from iso4217 import Currency


def create_dim_currency(currency_table_data):
    """finds relevant currency data
    and creates a list of dicts with the data"""
    if currency_table_data:
        dim_currency = pd.DataFrame(
            {
                "currency_id":
                [int(row["currency_id"]) for row in currency_table_data],
                "currency_code":
                [str(row["currency_code"]) for row in currency_table_data],
                "currency_name": [
                    str(Currency(row["currency_code"]).currency_name)
                    for row in currency_table_data
                ],
            }
        )
        return dim_currency
    return None
