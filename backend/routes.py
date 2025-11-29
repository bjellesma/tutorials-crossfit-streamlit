"""FastAPI routes for athlete data API.

This module defines the API endpoints for accessing athlete information.
"""
from fastapi import FastAPI, HTTPException
import traceback
import database

app = FastAPI()


@app.get('/api/athletes')
def get_athletes():
    """Get all athletes from the database.

    Retrieves athlete data from the database and returns it as a JSON response.
    This endpoint fetches up to 1000 athlete records with their associated columns.

    Returns:
        dict: A dictionary containing athlete data and column names.

    Raises:
        HTTPException: 500 error if database query fails.

    """
    try:
        return database.get_athletes()
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(500, detail=str(ex))
