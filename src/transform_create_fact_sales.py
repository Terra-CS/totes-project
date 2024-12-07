"""This module contains a function which transforms
extracted sales data into a df"""

import pandas as pd
from datetime import datetime
from datetime import date as datetype

def create_fact_sales(sales_table_data):
    """finds relevant sales data
    and creates a list of dicts with the data"""
    if sales_table_data:
        fact_sales = pd.DataFrame(
            {
                "sales_order_id": [
                    int(row["sales_order_id"]) for row in sales_table_data
                    ],
                "created_date": [
                    str(datetime.strptime(row["created_at"][:10], ("%Y-%m-%d")).strftime("%Y/%m/%d")) for row in sales_table_data
                    ],
                "created_time": [
                    str(row["created_at"][11:]) for row in sales_table_data
                    ],
                "last_updated_date": [
                    str(datetime.strptime(row["last_updated"][:10], ("%Y-%m-%d")).strftime("%Y/%m/%d")) for row in sales_table_data
                    ],
                "last_updated_time": [
                    str(row["last_updated"][11:]) for row in sales_table_data
                    ],
                "sales_staff_id": [
                    int(row["staff_id"]) for row in sales_table_data
                    ],
                "counterparty_id": [
                    int(row["counterparty_id"]) for row in sales_table_data
                    ],
                "units_sold": [
                    int(row["units_sold"]) for row in sales_table_data
                    ],
                "unit_price": [
                    round(float(row["unit_price"]),2) for row in sales_table_data
                    ],
                "currency_id": [
                    int(row["currency_id"]) for row in sales_table_data
                    ],
                "design_id": [
                    int(row["design_id"]) for row in sales_table_data
                    ],
                "agreed_payment_date": [
                    str(datetime.strptime(row["agreed_payment_date"], ("%Y-%m-%d")).strftime("%Y/%m/%d")) for row in sales_table_data
                ],
                "agreed_delivery_date": [
                    str(datetime.strptime(row["agreed_delivery_date"], ("%Y-%m-%d")).strftime("%Y/%m/%d")) for row in sales_table_data
                ],
                "agreed_delivery_location_id": [
                    int(row["agreed_delivery_location_id"])
                    for row in sales_table_data
                ],
            }
        )
        return fact_sales
    return None
