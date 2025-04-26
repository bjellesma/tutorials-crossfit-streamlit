

def main():
    import streamlit as st
    from src.plot import load_data, clean_data, generate_scatter_plot
    st.set_page_config(page_title="Crossfit Data")
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