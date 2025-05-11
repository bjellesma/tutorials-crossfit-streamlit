

def main():
    import streamlit as st
    from src.plot import load_data, clean_data, generate_scatter_plot, generate_histogram
    st.set_page_config(page_title="Crossfit Data")
    df = load_data()
    
    

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
        x_threshold_lower = st.number_input(f'Select lower bound for {x_axis}',0,1000,0,1)
        x_threshold_upper = st.number_input(f'Select upper bound for {x_axis}',0,1000,1000,1)
        x_std_slider = st.slider(
            "Remove outliers beyond deviation:",
            min_value=0.0,
            max_value=5.0,
            value=3.0,
            step=0.1,
            key="x_slider"
        ) if st.checkbox("Remove Outliers", key="x_outliers") else 0
        y_threshold_lower = st.number_input(f'Select lower bound for {y_axis}',0,1000,0,1)
        y_threshold_upper = st.number_input(f'Select lower bound for {y_axis}',0,1000,1000,1)
        y_std_slider = st.slider(
            "Remove outliers beyond deviation:",
            min_value=0.0,
            max_value=5.0,
            value=3.0,
            step=0.1,
            key="y_slider"
        ) if st.checkbox("Remove Outliers", key="y_outliers") else 0
        x_threshold = (x_threshold_lower, x_threshold_upper)
        y_threshold = (y_threshold_lower, y_threshold_upper)
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
        sample_size = st.radio("Select a sample size", options=[1000, 10000, 100000])
        trendline = trendline_options[trendline_display]
        df, (x_mean, x_std), (y_mean, y_std), (x_lower, x_upper), (y_lower, y_upper) = clean_data(df=df, sample_size=sample_size, x_axis=x_axis, y_axis=y_axis, x_thresholds=x_threshold, y_thresholds=y_threshold, standard_deviations=(x_std_slider, y_std_slider))



    
    scatter_tab, stabs_tab = st.tabs(['Scatter', 'Stats'])
    with scatter_tab:
        st.plotly_chart(generate_scatter_plot(df=df, x_axis=x_axis, y_axis=y_axis, trendline=trendline))
        if st.checkbox("Show Statistics"):
            st.subheader("Averages")
            st.markdown(f"**{x_axis}**: {df[x_axis].mean():.2f}")
            st.markdown(f"**{y_axis}**: {df[y_axis].mean():.2f}")
        with st.expander('Raw Data'):
            st.dataframe(df)
    with stabs_tab:
        x_histogram=generate_histogram(df, x_axis, x_mean, x_std)
        st.plotly_chart(x_histogram, use_container_width=True, theme=None)
        col = st.columns(2)
        with col[0]:
            st.markdown(f"**{x_axis} mean**: {x_mean:.2f}")
        with col[1]:
            st.markdown(f"**{x_axis} std**: {x_std:.2f}")
            st.markdown(f"**{x_axis} lower**: {x_lower:.2f}")
            st.markdown(f"**{x_axis} upper**: {x_upper:.2f}")
        y_histogram=generate_histogram(df, y_axis, y_mean, y_std)
        st.plotly_chart(y_histogram, use_container_width=False, theme="streamlit")
        col = st.columns(2)
        with col[0]:
            st.markdown(f"**{y_axis} mean**: {y_mean:.2f}")
        with col[1]:
            st.markdown(f"**{y_axis} std**: {y_std:.2f}")
            st.markdown(f"**{y_axis} lower**: {y_lower:.2f}")
            st.markdown(f"**{y_axis} upper**: {y_upper:.2f}")

if __name__ == '__main__':
    main()