from utils import constants

def display_axis_label(axis_name: str):
    return constants.DISPLAY_MAP.get(axis_name, axis_name)