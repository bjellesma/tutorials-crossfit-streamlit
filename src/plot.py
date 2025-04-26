import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv('temp/athletes.csv')

@st.cache_data
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    args:
        df (pd.Dataframe) data to be looking
    """
    filtered_df = df.dropna(subset=['weight', 'deadlift'])
    filtered_df = filtered_df[(filtered_df['weight'] <= 500) & (filtered_df['deadlift'] <= 1000)
                              & (filtered_df['weight'] >= 100) & (filtered_df['deadlift'] >= 10)]
    return filtered_df.head(1000)

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