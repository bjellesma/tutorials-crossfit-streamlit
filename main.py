

def main():
    import streamlit as st
    from st_aggrid import AgGrid, GridOptionsBuilder
    from src.plot import load_data, clean_data, generate_scatter_plot, generate_histogram
    from utils import helpers
    st.set_page_config(page_title="Crossfit Data")
    df = load_data()
    
    

    with st.sidebar:
        st.subheader('Options')
        numeric_columns = df.select_dtypes(include=['number']).drop(['athlete_id'], axis='columns').columns.tolist()
        x_axis = st.selectbox(
            label='X axis',
            options=numeric_columns,
            format_func=helpers.display_axis_label,
            key='x_axis'
        )
        x_axis_display = helpers.display_axis_label(x_axis)
        y_axis = st.selectbox(
            label='Y axis',
            options=[col for col in numeric_columns if col != x_axis],
            format_func=helpers.display_axis_label,
            key='y_axis'
        )
        y_axis_display = helpers.display_axis_label(y_axis)
        with st.sidebar.container():
            st.subheader(x_axis_display)
            x_threshold_lower = st.number_input(f'Select lower bound for {x_axis_display}',value=0, min_value=0)
            x_threshold_upper = st.number_input(f'Select upper bound for {x_axis_display}',value=1000, min_value=0)
            x_std_slider = st.slider(
                "Remove outliers beyond deviation:",
                min_value=0.0,
                max_value=5.0,
                value=3.0,
                step=0.1,
                key="x_slider"
            ) if st.checkbox("Remove Outliers", key="x_outliers") else 0
        with st.sidebar.container():
            st.subheader(y_axis_display)
            y_threshold_lower = st.number_input(f'Select lower bound for {y_axis_display}',value=0, min_value=0)
            y_threshold_upper = st.number_input(f'Select lower bound for {y_axis_display}',value=1000, min_value=0)
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
            'ols': 'Ordinary Least Squares',
            'expanding': 'Expanding',
            'lowess': 'Locally Weighted Scatterplot Smoothing'
        }
        trendline = st.selectbox(
            label='Trendline',
            options=trendline_options.keys(),
            format_func=lambda func: trendline_options.get(func, func),
            key='trendline'
        )
        sample_size = st.radio("Select a sample size", options=[1000, 10000, 100000])
        df, (x_mean, x_std), (y_mean, y_std), (x_lower, x_upper), (y_lower, y_upper) = clean_data(df=df, sample_size=sample_size, x_axis=x_axis, y_axis=y_axis, x_thresholds=x_threshold, y_thresholds=y_threshold, standard_deviations=(x_std_slider, y_std_slider))



    
    scatter_tab, stabs_tab = st.tabs(['Scatter', 'Stats'])
    with scatter_tab:
        
        st.plotly_chart(generate_scatter_plot(df=df, x_axis=x_axis, y_axis=y_axis, trendline=trendline))
        if st.checkbox("Show Statistics"):
            st.subheader("Averages")
            st.markdown(f"**{x_axis_display}**: {df[x_axis].mean():.2f}")
            st.markdown(f"**{y_axis_display}**: {df[y_axis].mean():.2f}")
        if st.toggle('Raw Data'):
            gender_options = df['gender'].unique().tolist()
            selected_genders = st.multiselect("Gender", options=gender_options)
            df = df[df['gender'].isin(selected_genders)] if selected_genders else df
            gb = GridOptionsBuilder.from_dataframe(df)
            for col in df.select_dtypes(include=["object"]).columns:
                gb.configure_column(col,
                        type=["textColumn", "textColumnFilter"],
                        filter="agTextColumnFilter")
            grid_options = gb.build()
            
            # pagination
            grid_options['pagination'] = True
            grid_options['paginationAutoPageSize'] = False
            grid_options['paginationPageSizeSelector'] = [5, 10, 20, 50, 100]
            AgGrid(df, gridOptions=grid_options, key="raw_data")
    with stabs_tab:
        x_histogram=generate_histogram(df, x_axis, x_mean, x_std)
        st.plotly_chart(x_histogram, use_container_width=True, theme=None)
        col = st.columns(2)
        with col[0]:
            st.markdown(f"**{x_axis_display} mean**: {x_mean:.2f}")
        with col[1]:
            st.markdown(f"**{x_axis_display} std**: {x_std:.2f}")
            st.markdown(f"**{x_axis_display} lower**: {x_lower:.2f}")
            st.markdown(f"**{x_axis_display} upper**: {x_upper:.2f}")
        y_histogram=generate_histogram(df, y_axis, y_mean, y_std)
        st.plotly_chart(y_histogram, use_container_width=False, theme="streamlit")
        col = st.columns(2)
        with col[0]:
            st.markdown(f"**{y_axis_display} mean**: {y_mean:.2f}")
        with col[1]:
            st.markdown(f"**{y_axis_display} std**: {y_std:.2f}")
            st.markdown(f"**{y_axis_display} lower**: {y_lower:.2f}")
            st.markdown(f"**{y_axis_display} upper**: {y_upper:.2f}")

if __name__ == '__main__':
    main()