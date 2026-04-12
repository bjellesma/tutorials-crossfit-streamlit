"""FastAPI routes for athlete data API.

This module defines the API endpoints for accessing athlete information.
"""

import traceback

import database
from fastapi import FastAPI, HTTPException
from models import Athlete, AthleteResponse
from predict import predict_run5k

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


@app.get('/api/predict/run5k')
def get_run5k_prediction(
    age: int,
    gender: str,
    backsq: int,
    deadlift: int,
    snatch: int,
    candj: int,
    pullups: int,
    weight: float,
    height: float,
    run400: float | int,
    fran: float | int,
    helen: float | int,
    grace: float | int,
):
    """Predict 5K run time based on athlete metrics using a pre-trained model.

    Args:
        age (int): Athlete's age.
        gender (str): Athlete's gender ('male' or 'female).
        backsq (int): Back squat weight.
        deadlift (int): Deadlift weight.
        snatch (int): Snatch weight.
        candj (int): Clean and jerk weight.
        pullups (int): Number of pull-ups.
        weight (int): Athlete's body weight.
        height (float|int): Athlete's height in inches.
        run400 (float|int): 400m run time in seconds.
        fran (float|int): Fran workout time in seconds.
        helen (float|int): Helen workout time in seconds.
        grace (float|int): Grace workout time in seconds.

    Returns:
        dict: Predicted 5K run time in seconds.

    """
    try:
        predicted_time = predict_run5k(
            age=age,
            gender=gender,
            backsq=backsq,
            deadlift=deadlift,
            snatch=snatch,
            candj=candj,
            pullups=pullups,
            weight=weight,
            height=height,
            run400=run400,
            fran=fran,
            helen=helen,
            grace=grace,
        )
        return {'predicted_run5k_time': predicted_time}
    except Exception as ex:
        traceback.print_exc()
        raise HTTPException(500, detail=str(ex))
