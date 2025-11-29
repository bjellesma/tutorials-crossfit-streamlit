"""Database module for athlete data management.

This module provides functions to interact with the DuckDB database
containing athlete information.
"""
import duckdb


def get_athletes():
    """Get athlete data from the DuckDB database.

    Retrieves up to 1000 athlete records from the athletes table in the DuckDB database,
    including all columns and column names.

    Returns:
        dict: A dictionary containing:
            - athletes (list): List of athlete records as tuples
            - columns (list): List of column names from the query result

    Raises:
        duckdb.Error: If there's an error connecting to or querying the database.

    """
    db_path = 'athletes.duckdb'

    with duckdb.connect(db_path) as conn:
        query = 'SELECT * FROM athletes LIMIT 1000'
        result = conn.execute(query=query)
        return {'athletes': result.fetchall(), 'columns': [col[0] for col in result.description]}
