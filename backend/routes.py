"""FastAPI routes for athlete data API.

This module defines the API endpoints for accessing athlete information.
"""

import traceback
from typing import Literal, Optional

import database
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class AthleteCreate(BaseModel):
    r"""Pydantic model for creating a new athlete.

    Validates athlete data from POST requests.

    Attributes:
        name (str): Athlete's name.
        age (int): Athlete's age (must be greater than 0).
        gender (Optional[Literal["male", "female"]]): Athlete's gender.
        grace (Optional[int]): Grace workout score (must be >= 0 if provided).
        fran (Optional[int]): Fran workout score (must be >= 0 if provided).
        helen (Optional[int]): Helen workout score (must be >= 0 if provided).
        filthy50 (Optional[int]): Filthy50 workout score (must be >= 0 if provided).
        fgonebad (Optional[int]): Fight Gone Bad workout score (must be >= 0 if provided).
        run400 (Optional[int]): 400m run time/score (must be >= 0 if provided).
        run5k (Optional[int]): 5k run time/score (must be >= 0 if provided).
        candj (Optional[int]): Clean & Jerk score (must be >= 0 if provided).
        snatch (Optional[int]): Snatch score (must be >= 0 if provided).
        deadlift (Optional[int]): Deadlift score (must be >= 0 if provided).
        backsq (Optional[int]): Back squat score (must be >= 0 if provided).
        pullups (Optional[int]): Pull-ups count/score (must be >= 0 if provided).

    """

    name: str
    age: int = Field(gt=0)
    gender: Optional[Literal['male', 'female']] = None
    grace: Optional[int] = Field(default=None, ge=0)
    fran: Optional[int] = Field(default=None, ge=0)
    helen: Optional[int] = Field(default=None, ge=0)
    filthy50: Optional[int] = Field(default=None, ge=0)
    fgonebad: Optional[int] = Field(default=None, ge=0)
    run400: Optional[int] = Field(default=None, ge=0)
    run5k: Optional[int] = Field(default=None, ge=0)
    candj: Optional[int] = Field(default=None, ge=0)
    snatch: Optional[int] = Field(default=None, ge=0)
    deadlift: Optional[int] = Field(default=None, ge=0)
    backsq: Optional[int] = Field(default=None, ge=0)
    pullups: Optional[int] = Field(default=None, ge=0)


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
def create_athlete(athlete: AthleteCreate):
    """Create a new athlete in the database.

    Validates and inserts a new athlete record with their information.

    Args:
        athlete (AthleteCreate): Athlete data including name, age, gender, and optional scores.

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
