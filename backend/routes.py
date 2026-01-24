"""FastAPI routes for athlete data API.

This module defines the API endpoints for accessing athlete information.
"""

import traceback

import database
from fastapi import FastAPI, HTTPException
from models import Athlete, AthleteResponse

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


@app.post('/api/athletes', status_code=201)
def create_athlete(athlete: Athlete):
    """Create a new athlete in the database.

    Validates and inserts a new athlete record with their information.

    Args:
        athlete (Athlete): Athlete data including name, age, gender, and optional scores.

    Returns:
        dict: Success message with created athlete information.

    Raises:
        HTTPException: 500 error if database insertion fails.

    """
    try:
        return database.create_athlete(
            name=athlete.name,
            age=athlete.age,
            gender=athlete.gender,
            grace=athlete.grace,
            fran=athlete.fran,
            helen=athlete.helen,
            filthy50=athlete.filthy50,
            fgonebad=athlete.fgonebad,
            run400=athlete.run400,
            run5k=athlete.run5k,
            candj=athlete.candj,
            snatch=athlete.snatch,
            deadlift=athlete.deadlift,
            backsq=athlete.backsq,
            pullups=athlete.pullups,
        )
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(500, detail=str(ex))


@app.get('/api/athlete/{athlete_id}', response_model=AthleteResponse)
def get_athlete_by_id(athlete_id: int):
    """Get a single athlete by ID.

    Retrieves a specific athlete's complete information from the database
    using their unique athlete_id.

    Args:
        athlete_id (int): The unique identifier of the athlete to retrieve.

    Returns:
        AthleteResponse: Complete athlete information including all fields.

    Raises:
        HTTPException: 404 error if athlete not found, 500 error if database query fails.

    """
    try:
        athlete = database.get_athlete(athlete_id)
        if athlete is None:
            raise HTTPException(404, detail=f'Athlete with ID {athlete_id} not found')
        return athlete
    except HTTPException:
        raise
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(500, detail=str(ex))
