import streamlit as st
import pandas as pd

st.set_page_config(page_title="Crossfit Data")

@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv('temp/athletes.csv')

def main():
    df = load_data()
    st.dataframe(df)

if __name__ == '__main__':
    main()