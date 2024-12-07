"""This module contains a function which transforms
extracted design data into a df"""

import pandas as pd


def create_dim_design(design_table_data):
    """finds relevant design data
    and creates a list of dicts with the data"""
    if design_table_data:
        dim_design = pd.DataFrame(
            {
                "design_id": [int(row["design_id"])
                              for row in design_table_data],
                "design_name": [str(row["design_name"])
                                for row in design_table_data],
                "file_name": [str(row["file_name"])
                              for row in design_table_data],
                "file_location": [str(row["file_location"])
                                  for row in design_table_data],
            }
        )
        return dim_design
    return None
