import joblib

model = joblib.load('run5k_predictor.model')


def predict_run5k(
    age: int,
    gender: str,
    backsq: int,
    deadlift: int,
    snatch: int,
    candj: int,
    pullups: int,
    weight: float,
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

    Returns:
        float: Predicted 5K run time in seconds.

    """
    features = [
        [
            age,
            1 if gender.lower() == 'male' else 0,
            backsq,
            deadlift,
            snatch,
            candj,
            pullups,
            weight,
        ]
    ]
    return model.predict(features)[0]
