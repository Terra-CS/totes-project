"""This module contains a function which transforms
extracted counterparty data into a df"""

import pandas as pd
from copy import deepcopy


def create_dim_counterparty(counterparty_data, address_data):
    """finds relevant counterparty data
    and creates a list of dicts with the data"""
    if counterparty_data and address_data:
        counpar_copy = deepcopy(counterparty_data)
        add_copy = deepcopy(address_data)
        counpar_add_data = []
        for party in counpar_copy:
            for add in add_copy:
                if party["legal_address_id"] == add["address_id"]:
                    party.update(add)
                    counpar_add_data.append(party)

        # create df from comprehensions
        dim_counterparty = pd.DataFrame(
            {
                "counterparty_id": [
                   int(datum["counterparty_id"]) for datum in counpar_add_data
                ],
                "counterparty_legal_name": [
                    str(datum["counterparty_legal_name"]) for datum
                    in counpar_add_data
                ],
                "counterparty_legal_address_line_1": [
                    str(datum["address_line_1"]) for datum in counpar_add_data
                ],
                "counterparty_legal_address_line_2": [
                    str(datum["address_line_2"]) for datum in counpar_add_data
                ],
                "counterparty_legal_district": [
                    str(datum["district"]) for datum in counpar_add_data
                ],
                "counterparty_legal_city": [
                    str(datum["city"]) for datum in counpar_add_data
                ],
                "counterparty_legal_postal_code": [
                    str(datum["postal_code"]) for datum in counpar_add_data
                ],
                "counterparty_legal_country": [
                    str(datum["country"]) for datum in counpar_add_data
                ],
                "counterparty_legal_phone_number": [
                    str(datum["phone"]) for datum in counpar_add_data
                ],
            }
        )
        return dim_counterparty
    return None
