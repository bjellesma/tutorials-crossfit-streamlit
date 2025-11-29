"""Data processing and visualization functions for CrossFit athlete data.

This module provides functions for loading, cleaning, and visualizing
athlete performance data using Plotly and Pandas.
"""

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from utils import constants, helpers


def calculate_stats(df, column):
    """Calculate mean and standard deviation for a column.

    Args:
        df (pd.DataFrame): The dataframe containing the data.
        column (str): The column name to calculate statistics for.

    Returns:
        tuple: A tuple containing (mean, std) values.

    """
    mean = df[column].mean()
    std = df[column].std()
    return mean, std


def load_data() -> pd.DataFrame:
    """Load athlete data from the backend API.

    Fetches athlete data from the backend service and converts it to a DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing athlete data with all columns.

    Raises:
        requests.RequestException: If the API request fails.

    """
    res = requests.get('http://backend:5000/api/athletes')
    data = res.json()
    df = pd.DataFrame(data=data['athletes'], columns=data['columns'])
    return df


@st.cache_data
def clean_data(
    df: pd.DataFrame,
    sample_size: int,
    x_axis: str,
    y_axis: str,
    x_thresholds: tuple[int, int],
    y_thresholds: tuple[int, int],
    standard_deviations: tuple[int, int],
) -> pd.DataFrame:
    """Clean and filter athlete data based on thresholds and outliers.

    Filters the dataframe by removing null values, applying threshold bounds,
    limiting sample size, and optionally removing statistical outliers.

    Args:
        df (pd.DataFrame): The dataframe containing athlete data.
        sample_size (int): Maximum number of samples to include.
        x_axis (str): Column name for x-axis metric.
        y_axis (str): Column name for y-axis metric.
        x_thresholds (tuple[int, int]): Lower and upper bounds for x-axis values.
        y_thresholds (tuple[int, int]): Lower and upper bounds for y-axis values.
        standard_deviations (tuple[int, int]): Standard deviation multipliers for outlier removal (0 to disable).

    Returns:
        tuple: A tuple containing:
            - filtered_df (pd.DataFrame): The cleaned and filtered dataframe
            - (x_mean, x_std): Mean and standard deviation for x-axis
            - (y_mean, y_std): Mean and standard deviation for y-axis
            - (x_lower, x_upper): Applied lower and upper bounds for x-axis
            - (y_lower, y_upper): Applied lower and upper bounds for y-axis

    """
    filtered_df = df.dropna(subset=[x_axis, y_axis])
    filtered_df = filtered_df[
        (filtered_df[x_axis] <= x_thresholds[1])
        & (filtered_df[y_axis] <= y_thresholds[1])
        & (filtered_df[x_axis] >= x_thresholds[0])
        & (filtered_df[y_axis] >= y_thresholds[0])
    ]
    filtered_df = filtered_df.head(sample_size)

    x_mean, x_std = calculate_stats(filtered_df, x_axis)
    y_mean, y_std = calculate_stats(filtered_df, y_axis)
    x_deviation_option, y_deviation_option = standard_deviations

    if x_deviation_option:
        x_lower = x_mean - x_std * x_deviation_option
        x_upper = x_mean + x_std * x_deviation_option
        filtered_df = filtered_df[
            (filtered_df[x_axis] >= x_lower) & (filtered_df[x_axis] <= x_upper)
        ]
    else:
        x_lower, x_upper = x_thresholds[0], x_thresholds[1]

    if y_deviation_option:
        y_lower = y_mean - y_std * y_deviation_option
        y_upper = y_mean + y_std * y_deviation_option
        filtered_df = filtered_df[
            (filtered_df[y_axis] >= y_lower) & (filtered_df[y_axis] <= y_upper)
        ]
    else:
        y_lower, y_upper = y_thresholds[0], y_thresholds[1]

    return (filtered_df, (x_mean, x_std), (y_mean, y_std), (x_lower, x_upper), (y_lower, y_upper))


def generate_scatter_plot(
    df: pd.DataFrame, x_axis: str = 'weight', y_axis: str = 'deadlift', trendline: str = 'ols'
) -> px.scatter:
    """Generate a scatter plot comparing two athlete performance metrics.

    Creates an interactive Plotly scatter plot with trendline showing the relationship
    between two performance metrics. Includes hover data for athlete details.

    Args:
        df (pd.DataFrame): DataFrame containing athlete data.
        x_axis (str): Column name for x-axis metric. Defaults to 'weight'.
        y_axis (str): Column name for y-axis metric. Defaults to 'deadlift'.
        trendline (str): Type of trendline to display ('ols', 'lowess', 'expanding'). Defaults to 'ols'.

    Returns:
        px.scatter: Plotly scatter plot figure object.

    """
    x_axis_display = helpers.get_event_info(x_axis)
    y_axis_display = helpers.get_event_info(y_axis)
    fig = px.scatter(
        df,
        x=x_axis,
        y=y_axis,
        title=f'{x_axis_display} vs {y_axis_display}',
        trendline=trendline,
        hover_name='name',
        hover_data=['region', 'affiliate', 'team', 'gender'],
    )

    fig.update_layout(
        xaxis_title=f'{x_axis_display} ({helpers.get_event_info(x_axis, "unit")})',
        yaxis_title=f'{y_axis_display} ({helpers.get_event_info(y_axis, "unit")})',
        height=700,
        width=900,
        font=dict(family=constants.FONT_FAMILY),
        title_font=dict(family=constants.FONT_FAMILY),
    )

    return fig


def generate_histogram(df: pd.DataFrame, column: str, mean, std, num_std=5):
    """Generate a histogram with mean and standard deviation lines.

    Creates a histogram showing the distribution of a metric with visual indicators
    for mean and standard deviation boundaries.

    Args:
        df (pd.DataFrame): DataFrame containing athlete data.
        column (str): Column name for the metric to plot.
        mean (float): Mean value of the metric.
        std (float): Standard deviation of the metric.
        num_std (int): Number of standard deviations to display. Defaults to 5.

    Returns:
        px.histogram: Plotly histogram figure object with mean and std deviation lines.

    """
    fig = px.histogram(
        df,
        x=column,
        nbins=50,
        opacity=0.7,
        title=f'Distribution of {helpers.get_event_info(column)}',
    )

    fig.add_vline(
        x=mean,
        line_dash='solid',
        line_color='green',
        annotation_text='Mean',
        annotation_position='top right',
    )

    for i in range(1, num_std + 1):
        fig.add_vline(
            x=mean + std * i,
            line_dash='dash',
            line_color='red',
            annotation_text=f'+{i}σ',
            annotation_position='top right',
        )
        fig.add_vline(
            x=mean - std * i,
            line_dash='dash',
            line_color='red',
            annotation_text=f'-{i}σ',
            annotation_position='top right',
        )

    fig.update_layout(
        xaxis_title=helpers.get_event_info(column),
        yaxis_title='Distribution',
        height=700,
        width=900,
        font=dict(family=constants.FONT_FAMILY),
        title_font=dict(family=constants.FONT_FAMILY),
    )

    return fig
