import requests
from utils import constants, helpers


def predict_run5k(
    age: int,
    gender: str,
    backsq: int,
    deadlift: int,
    snatch: int,
    candj: int,
    pullups: int,
    weight: float,
) -> float:
    """Predict 5K run time based on athlete metrics using the backend ML model.

    Makes a GET request to the backend prediction endpoint with athlete metrics
    and returns the predicted 5K run time in seconds.

    Args:
        age (int): Athlete's age.
        gender (str): Athlete's gender ('male' or 'female').
        backsq (int): Back squat weight in lbs.
        deadlift (int): Deadlift weight in lbs.
        snatch (int): Snatch weight in lbs.
        candj (int): Clean and jerk weight in lbs.
        pullups (int): Number of pull-ups.
        weight (float): Athlete's body weight in lbs.

    Returns:
        float: Predicted 5K run time in seconds.

    Raises:
        requests.HTTPError: If the API request fails (4xx, 5xx status codes).
        requests.ConnectionError: If unable to connect to the backend server.
        KeyError: If the response doesn't contain the expected 'predicted_run5k_time' key.

    """
    with helpers.timer(f'Predicting 5K run time for {gender} aged {age}'):
        params = {
            'age': age,
            'gender': gender,
            'backsq': backsq,
            'deadlift': deadlift,
            'snatch': snatch,
            'candj': candj,
            'pullups': pullups,
            'weight': weight,
        }
        res = requests.get(f'{constants.BACKEND_URL}/api/predict/run5k', params=params)
        res.raise_for_status()
        response_data = res.json()

    return response_data['predicted_run5k_time']
