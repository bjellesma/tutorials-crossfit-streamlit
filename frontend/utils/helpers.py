from utils import constants
import streamlit as st


def _get_event(axis_name: str):
    return constants.EVENT_MAPPING.get(
        axis_name, {'display_name': axis_name, 'better': 'neither', 'unit': '', 'description': ''}
    )


def get_event_info(axis_name: str, key: str = 'display_name'):
    event_info = _get_event(axis_name)
    return event_info[key]


def format_value(value: float, axis_name: str):
    unit = get_event_info(axis_name, 'unit')
    if unit == 'seconds':
        minute = int(value // 60)
        second = round(value % 60)

        return f'{minute}:{second:02d}'
    elif unit == 'inches':
        return f'{value:.2f}"'
    else:
        return f'{value:.2f} {unit}'


def generate_css():
    return f"""
    :root {{
        --font-family: {constants.FONT_FAMILY}
    }}
    """


def get_url_param(key, default=None):
    return st.query_params.get(key, default)
