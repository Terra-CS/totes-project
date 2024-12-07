"""This module contains a function which transforms
extracted staff data into a df"""

import pandas as pd
from copy import deepcopy


def create_dim_staff(staff_data, dep_data):
    """finds relevant staff data
    and creates a list of dicts with the data"""
    if staff_data and dep_data:
        # copy data to construct merged table data
        staff_copy = deepcopy(staff_data)
        dep_copy = deepcopy(dep_data)
        dep_staff_data = []
        """find department with matching id
        and create list of dicts with all data"""
        for staff in staff_copy:
            for dep in dep_copy:
                if staff["department_id"] == dep["department_id"]:
                    staff.update(dep)
                    dep_staff_data.append(staff)
        # create df from comprehensions
        dim_staff = pd.DataFrame(
            {
                "staff_id": [int(datum["staff_id"])
                             for datum in dep_staff_data],
                "first_name": [str(datum["first_name"])
                               for datum in dep_staff_data],
                "last_name": [str(datum["last_name"])
                              for datum in dep_staff_data],
                "department_name": [
                    str(datum["department_name"])
                    for datum in dep_staff_data
                ],
                "location": [str(datum["location"])
                             for datum in dep_staff_data],
                "email_address": [str(datum["email_address"])
                                  for datum in dep_staff_data],
            }
        )
        return dim_staff
    return None
