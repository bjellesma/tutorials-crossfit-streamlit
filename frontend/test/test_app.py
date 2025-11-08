import pytest
from streamlit.testing.v1 import AppTest

metrics = [
    'age',
    'height',
    'weight',
    'fran',
    'helen',
    'grace',
    'filthy50',
    'fgonebad',
    'run400',
    'run5k',
    'candj',
    'snatch',
    'deadlift',
    'backsq',
    'pullups',
]

trendline_functions = [
    'Ordinary Least Squares',
    'Expanding',
    'Locally Weighted Scatterplot Smoothing',
]


@pytest.fixture(scope='module')
def app_test():
    from main import main

    return AppTest.from_function(main, default_timeout=30).run()


def test_app(app_test):
    assert not app_test.exception


@pytest.mark.parametrize('value', metrics)
def test_x_axis(value, app_test):
    selectbox = app_test.selectbox(key='x_axis')
    selectbox.set_value(value).run()

    errors = [e.value for e in app_test.error]
    assert not errors, f'Value {value} triggered errors {",".join(errors)}'


@pytest.mark.parametrize('value', metrics[:-1])
def test_y_axis(value, app_test):
    selectbox = app_test.selectbox(key='y_axis')
    selectbox.set_value(value).run()

    errors = [e.value for e in app_test.error]
    assert not errors, f'Value {value} triggered errors {",".join(errors)}'


@pytest.mark.single
@pytest.mark.parametrize('value', trendline_functions)
def test_trendline(value, app_test):
    selectbox = app_test.selectbox(key='trendline')
    selectbox.set_value(value).run()

    errors = [e.value for e in app_test.error]
    assert not errors, f'Value {value} triggered errors {",".join(errors)}'
