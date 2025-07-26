import streamlit as st
import pandas as pd
import plotly.express as px
from utils import helpers

def calculate_stats(df, column):
    mean = df[column].mean()
    std = df[column].std()
    return mean, std

@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv('temp/athletes.csv')

@st.cache_data
def clean_data(df: pd.DataFrame, sample_size: int, x_axis: str, y_axis: str, x_thresholds: tuple[int, int], y_thresholds: tuple[int, int], standard_deviations: tuple[int, int]) -> pd.DataFrame:
    """
    args:
        df (pd.Dataframe) data to be looking
    """
    filtered_df = df.dropna(subset=[x_axis, y_axis])
    filtered_df = filtered_df[(filtered_df[x_axis] <= x_thresholds[1]) & (filtered_df[y_axis] <= y_thresholds[1])
                              & (filtered_df[x_axis] >= x_thresholds[0]) & (filtered_df[y_axis] >= y_thresholds[0])]
    filtered_df = filtered_df.head(sample_size)

    x_mean, x_std = calculate_stats(filtered_df, x_axis)
    y_mean, y_std = calculate_stats(filtered_df, y_axis)
    x_deviation_option, y_deviation_option = standard_deviations

    if x_deviation_option:
        x_lower = x_mean - x_std * x_deviation_option
        x_upper = x_mean + x_std * x_deviation_option
        filtered_df = filtered_df[(filtered_df[x_axis] >= x_lower) & (filtered_df[x_axis] <= x_upper)]
    else:
        x_lower, x_upper = x_thresholds[0], x_thresholds[1]

    if y_deviation_option:
        y_lower = y_mean - y_std * y_deviation_option
        y_upper = y_mean + y_std * y_deviation_option
        filtered_df = filtered_df[(filtered_df[y_axis] >= y_lower) & (filtered_df[y_axis] <= y_upper)]
    else:
        y_lower, y_upper = y_thresholds[0], y_thresholds[1]

    return filtered_df, (x_mean, x_std), (y_mean, y_std), (x_lower, x_upper), (y_lower, y_upper)

def generate_scatter_plot(df: pd.DataFrame, x_axis:str="weight",y_axis:str="deadlift", trendline: str="ols") -> px.scatter:
    x_axis_display = helpers.get_event_info(x_axis)
    y_axis_display = helpers.get_event_info(y_axis)
    fig = px.scatter(
        df,
        x=x_axis,
        y=y_axis,
        title=f'{x_axis_display} vs {y_axis_display}',
        trendline=trendline,
        hover_name='name',
        hover_data=['region', 'affiliate', 'team', 'gender']
    )

    fig.update_layout(
        xaxis_title=f'{x_axis_display} ({helpers.get_event_info(x_axis, "unit")})',
        yaxis_title=f'{y_axis_display} ({helpers.get_event_info(y_axis, "unit")})',
        height=700,
        width=900
    )

    return fig

def generate_histogram(df: pd.DataFrame, column: str, mean, std, num_std = 5):
    fig = px.histogram(
        df,
        x=column,
        nbins=50,
        opacity=.7,
        title=f'Distribution of {helpers.get_event_info(column)}'
    )

    fig.add_vline(
        x=mean,
        line_dash="solid",
        line_color="green",
        annotation_text="Mean",
        annotation_position="top right"
    )

    for i in range(1, num_std+1):
        fig.add_vline(
            x=mean+std*i,
            line_dash="dash",
            line_color="red",
            annotation_text=f"+{i}σ",
            annotation_position="top right"
        )
        fig.add_vline(
            x=mean-std*i,
            line_dash="dash",
            line_color="red",
            annotation_text=f"-{i}σ",
            annotation_position="top right"
        )

    fig.update_layout(
        xaxis_title=helpers.get_event_info(column),
        yaxis_title="Distribution",
        height=700,
        width=900
    )

    return fig