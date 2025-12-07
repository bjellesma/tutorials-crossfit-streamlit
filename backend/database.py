"""Database module for athlete data management.

This module provides functions to interact with the DuckDB database
containing athlete information.
"""

from typing import Optional

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
        query = 'SELECT * FROM athletes ORDER BY athlete_id DESC LIMIT 1000;'
        result = conn.execute(query=query)
        return {'athletes': result.fetchall(), 'columns': [col[0] for col in result.description]}


def create_athlete(
    name: str,
    age: int,
    gender: Optional[str] = None,
    grace: Optional[int] = None,
    fran: Optional[int] = None,
    helen: Optional[int] = None,
    filthy50: Optional[int] = None,
    fgonebad: Optional[int] = None,
    run400: Optional[int] = None,
    run5k: Optional[int] = None,
    candj: Optional[int] = None,
    snatch: Optional[int] = None,
    deadlift: Optional[int] = None,
    backsq: Optional[int] = None,
    pullups: Optional[int] = None,
) -> dict:
    """Create a new athlete in the DuckDB database.

    Inserts a new athlete record with validated data. Generates a new athlete_id
    by incrementing the maximum existing ID.

    Args:
        name (str): Athlete's name.
        age (int): Athlete's age (must be positive).
        gender (Optional[str]): Athlete's gender ("male" or "female"), defaults to None.
        grace (Optional[int]): Grace workout score (must be >= 0 if provided), defaults to None.
        fran (Optional[int]): Fran workout score (must be >= 0 if provided), defaults to None.
        helen (Optional[int]): Helen workout score (must be >= 0 if provided), defaults to None.
        filthy50 (Optional[int]): Filthy50 workout score (must be >= 0 if provided), defaults to None.
        fgonebad (Optional[int]): Fight Gone Bad workout score (must be >= 0 if provided), defaults to None.
        run400 (Optional[int]): 400m run score (must be >= 0 if provided), defaults to None.
        run5k (Optional[int]): 5k run score (must be >= 0 if provided), defaults to None.
        candj (Optional[int]): Clean & Jerk score (must be >= 0 if provided), defaults to None.
        snatch (Optional[int]): Snatch score (must be >= 0 if provided), defaults to None.
        deadlift (Optional[int]): Deadlift score (must be >= 0 if provided), defaults to None.
        backsq (Optional[int]): Back squat score (must be >= 0 if provided), defaults to None.
        pullups (Optional[int]): Pull-ups score (must be >= 0 if provided), defaults to None.

    Returns:
        dict: Dictionary containing success status and new athlete_id.

    Raises:
        duckdb.Error: If there's an error connecting to or inserting into the database.

    """
    db_path = 'athletes.duckdb'

    with duckdb.connect(db_path) as conn:
        # Get next athlete_id
        result = conn.execute(
            'SELECT COALESCE(MAX(athlete_id), 0) + 1 as next_id FROM athletes'
        ).fetchone()
        new_athlete_id = result[0]

        # Insert new athlete
        conn.execute(
            """
            INSERT INTO athletes (
                athlete_id,
                name,
                age,
                gender,
                grace,
                fran,
                helen,
                filthy50,
                fgonebad,
                run400,
                run5k,
                candj,
                snatch,
                deadlift,
                backsq,
                pullups
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                new_athlete_id,
                name,
                age,
                gender,
                grace,
                fran,
                helen,
                filthy50,
                fgonebad,
                run400,
                run5k,
                candj,
                snatch,
                deadlift,
                backsq,
                pullups,
            ],
        )

        return {
            'status': 'success',
            'athlete_id': new_athlete_id,
            'message': f'Athlete {name} created successfully',
        }
