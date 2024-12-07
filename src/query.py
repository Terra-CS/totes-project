"""Module contains a function for extracting a table of data from a db"""


def run_query(query, db):
    """runs a SQL query to extract named tables from a db"""
    try:
        query_db = db.run(query)
        columns = [col["name"] for col in db.columns]
        return [
            {heading: str(row[index]) for index, heading in enumerate(columns)}
            for row in query_db
        ]
    except Exception as e:
        raise e
