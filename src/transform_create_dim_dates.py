"""This module contains a function which transforms
extracted dates data into a df"""

import pandas as pd
from datetime import datetime
from datetime import date as dat


def create_dim_dates(sales_data):
    """finds relevant dates data
    and creates a list of dicts with the data"""
    if sales_data:
        # remove duplicates, time from datetime strings and convert to datetime
        created_date = {
            datetime.strptime(datum["created_at"][:10], ("%Y-%m-%d"))
            for datum in sales_data
        }
        last_updated_date = {
            datetime.strptime(datum["last_updated"][:10], ("%Y-%m-%d"))
            for datum in sales_data
        }
        payment_date = {
            datetime.strptime(datum["agreed_payment_date"], ("%Y-%m-%d"))
            for datum in sales_data
        }
        delivery_date = {
            datetime.strptime(datum["agreed_delivery_date"], ("%Y-%m-%d"))
            for datum in sales_data
        }
        set_dates = (created_date | last_updated_date
                     | payment_date | delivery_date)
        # create list and create dataframe converting back to string
        date_data = list(set_dates)
        date_data.sort()
        dicts = {
            "date_id": [(date.strftime("%Y-%m-%d")) for date in date_data],
            "year": [int(date.strftime("%Y")) for date in date_data],
            "month": [int(date.strftime("%m")) for date in date_data],
            "day": [int(date.strftime("%d")) for date in date_data],
            "day_of_week": [int(date.strftime("%w")) for date in date_data],
            "day_name": [str(date.strftime("%A")) for date in date_data],
            "month_name": [str(date.strftime("%B")) for date in date_data],
            "quarter": [(int(date.strftime("%m")) - 1) // 3 + 1
                        for date in date_data],
        }
        dim_date = pd.DataFrame(dicts)
        return dim_date
    return None
