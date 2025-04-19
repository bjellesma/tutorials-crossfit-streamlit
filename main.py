import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Crossfit Data")

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

def main():
    df = load_data()
    df = clean_data(df=df)

    with st.sidebar:
        st.subheader('Options')
        numeric_columns = df.select_dtypes(include=['number']).drop(['athlete_id'], axis='columns').columns.tolist()
        x_axis = st.selectbox(
            label='X axis',
            options=numeric_columns,
            key='x_axis'
        )
        
        y_axis = st.selectbox(
            label='Y axis',
            options=[col for col in numeric_columns if col != x_axis],
            key='y_axis'
        )
        trendline_options={
            'Ordinary Least Squares': 'ols',
            'Expanding': 'expanding',
            'Locally Weighted Scatterplot Smoothing': 'lowess'
        }

        trendline_display = st.selectbox(
            label='Trendline',
            options=trendline_options.keys(),
            key='trendline'
        )
        trendline = trendline_options[trendline_display]

    st.plotly_chart(generate_scatter_plot(df=df, x_axis=x_axis, y_axis=y_axis, trendline=trendline))
    if st.checkbox("Show Statistics"):
        st.subheader("Averages")
        st.markdown(f"**{x_axis}**: {df[x_axis].mean():.2f}")
        st.markdown(f"**{y_axis}**: {df[y_axis].mean():.2f}")
    with st.expander('Raw Data'):
        st.dataframe(df)

if __name__ == '__main__':
    main()