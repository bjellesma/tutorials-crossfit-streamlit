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

def generate_scatter_plot(df: pd.DataFrame) -> px.scatter:
    fig = px.scatter(
        df,
        x='weight',
        y='deadlift',
        title='Weight vs Deadlift',
        trendline="ols"
    )

    fig.update_layout(
        xaxis_title="Body Weight (lbs)",
        yaxis_title='Deadlift (lbs)',
        height=700,
        width=900
    )

    return fig

def main():
    df = load_data()
    df = clean_data(df=df)
    st.plotly_chart(generate_scatter_plot(df=df))
    if st.checkbox("Show Statistics"):
        st.subheader("Averages")
        st.markdown(f"**Deadlift**: {df['deadlift'].mean():.2f} lbs")
        st.markdown(f"**Weight**: {df['weight'].mean():.2f} lbs")
    with st.expander('Raw Data'):
        st.dataframe(df)

if __name__ == '__main__':
    main()