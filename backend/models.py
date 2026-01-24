"""Module contains Pydantic models for athlete data validation."""

from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class Athlete(BaseModel):
    r"""Pydantic model for creating a new athlete.

    Validates athlete data from POST requests.


    Attributes:
        name (str): Athlete's name.
        age (int): Athlete's age (must be greater than 0).
        gender (Optional[Literal["Male", "Female"]]): Athlete's gender (stored as uppercase).
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
    gender: Optional[Literal['Male', 'Female']] = None

    @field_validator('gender', 'grace', mode='before')
    @classmethod
    def normalize_gender(cls, v):
        """Normalize gender to uppercase format.

        Accepts case-insensitive input (male, Male, MALE, female, Female, FEMALE)
        and converts to capitalized format (Male, Female) for database storage.

        Args:
            v: The gender value to normalize.

        Returns:
            Optional[str]: Normalized gender string or None.

        """
        if v is None:
            return None
        if isinstance(v, str):
            v_lower = v.lower()
            if v_lower == 'male':
                return 'Male'
            elif v_lower == 'female':
                return 'Female'
        return v

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


class AthleteResponse(Athlete):
    """Pydantic model for athlete GET responses.

    Extends Athlete model with athlete_id field for database retrieval responses.

    Attributes:
        athlete_id (int): Unique identifier for the athlete in the database.
        All other attributes inherited from Athlete model.

    """

    athlete_id: int
