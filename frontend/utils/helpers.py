"""Helper utility functions for event information and formatting.

This module provides utility functions for retrieving event metadata,
formatting values, and managing URL parameters.
"""

import streamlit as st
from utils import constants


def _get_event(axis_name: str):
    """Get event metadata for a given axis name.

    Retrieves event information from the EVENT_MAPPING constant, returning
    a default structure if the event is not found.

    Args:
        axis_name (str): The name of the event/metric.

    Returns:
        dict: Dictionary containing event metadata with keys:
            - display_name: Human-readable name
            - better: Whether higher or lower is better ('higher', 'lower', 'neither')
            - unit: Unit of measurement
            - description: Description of the event

    """
    return constants.EVENT_MAPPING.get(
        axis_name, {'display_name': axis_name, 'better': 'neither', 'unit': '', 'description': ''}
    )


def get_event_info(axis_name: str, key: str = 'display_name'):
    """Get specific event information for a metric.

    Args:
        axis_name (str): The name of the event/metric.
        key (str): The specific information key to retrieve. Defaults to 'display_name'.

    Returns:
        str: The requested event information value.

    """
    event_info = _get_event(axis_name)
    return event_info[key]


def format_value(value: float, axis_name: str):
    """Format a numeric value based on its unit type.

    Formats values appropriately based on the metric's unit (seconds as MM:SS,
    inches with quote marks, or other units with their labels).

    Args:
        value (float): The numeric value to format.
        axis_name (str): The name of the metric to determine formatting.

    Returns:
        str: Formatted string representation of the value.

    """
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
    """Generate CSS variables for the application.

    Returns:
        str: CSS string containing root variables for styling.

    """
    return f"""
    :root {{
        --font-family: {constants.FONT_FAMILY}
    }}
    """


def get_url_param(key, default=None):
    """Get a URL query parameter value.

    Args:
        key (str): The query parameter key to retrieve.
        default: Default value to return if parameter is not found. Defaults to None.

    Returns:
        The parameter value if found, otherwise the default value.

    """
    return st.query_params.get(key, default)
