"""This module contains a function which transforms
extracted location data into a df"""

import pandas as pd


def create_dim_location(address_data, sales_data):
    """finds relevant location data
    and creates a list of dicts with the data"""
    if address_data and sales_data:
        locations = [sale["agreed_delivery_location_id"]
                     for sale in sales_data]
        dim_location = pd.DataFrame(
            {
                "location_id": [
                    int(datum["address_id"])
                    for datum in address_data
                    if datum["address_id"] in locations
                ],
                "address_line_1": [
                    str(datum["address_line_1"])
                    for datum in address_data
                    if datum["address_id"] in locations
                ],
                "address_line_2": [
                    str(datum["address_line_2"])
                    for datum in address_data
                    if datum["address_id"] in locations
                ],
                "district": [
                    str(datum["district"])
                    for datum in address_data
                    if datum["address_id"] in locations
                ],
                "city": [
                    str(datum["city"])
                    for datum in address_data
                    if datum["address_id"] in locations
                ],
                "postal_code": [
                    str(datum["postal_code"])
                    for datum in address_data
                    if datum["address_id"] in locations
                ],
                "country": [
                    str(datum["country"])
                    for datum in address_data
                    if datum["address_id"] in locations
                ],
                "phone": [
                    str(datum["phone"])
                    for datum in address_data
                    if datum["address_id"] in locations
                ],
            }
        )
        return dim_location
    return None
