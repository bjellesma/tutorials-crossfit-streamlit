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
        height (float): Athlete's height.
        run400 (float|int): 400m run time in seconds.
        fran (float|int): Fran workout time in seconds.
        helen (float|int): Helen workout time in seconds.
        grace (float|int): Grace workout time in seconds.

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
            height,
            run400,
            fran,
            helen,
            grace,
        ]
    ]
    return model.predict(features)[0]
