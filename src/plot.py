import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv('temp/athletes.csv')

@st.cache_data
def clean_data(df: pd.DataFrame, sample_size: int, x_axis: str, y_axis: str, x_thresholds: tuple[int, int], y_thresholds: tuple[int, int]) -> pd.DataFrame:
    """
    args:
        df (pd.Dataframe) data to be looking
    """
    filtered_df = df.dropna(subset=[x_axis, y_axis])
    filtered_df = filtered_df[(filtered_df[x_axis] <= x_thresholds[1]) & (filtered_df[y_axis] <= y_thresholds[1])
                              & (filtered_df[x_axis] >= x_thresholds[0]) & (filtered_df[y_axis] >= y_thresholds[0])]
    return filtered_df.head(sample_size)

def generate_scatter_plot(df: pd.DataFrame, x_axis:str="weight",y_axis:str="deadlift", trendline: str="ols") -> px.scatter:
    fig = px.scatter(
        df,
        x=x_axis,
        y=y_axis,
        title=f'{x_axis} vs {y_axis}',
        trendline=trendline,
        hover_name='name',
        hover_data=['region', 'affiliate', 'team', 'gender']
    )

    fig.update_layout(
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        height=700,
        width=900
    )

    return fig

def generate_histogram(df: pd.DataFrame, column: str):
    fig = px.histogram(
        df,
        x=column,
        nbins=50,
        opacity=.7,
        title=f'Distribution of {column}'
    )

    return fig