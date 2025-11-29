"""Streamlit application for CrossFit data visualization.

This module provides the main Streamlit app for visualizing and analyzing
CrossFit athlete performance data.
"""


def main():
    """Run the Streamlit application.

    Sets up the Streamlit page configuration, loads athlete data, and renders
    the interactive data visualization dashboard. The dashboard includes:
    - Scatter plots comparing different performance metrics
    - Statistical analysis and histograms
    - Data filtering and outlier removal options
    - Downloadable data exports

    Raises:
        Exception: Displays error message if the application fails to load.

    """
    import io
    import traceback
    import zipfile
    from datetime import datetime

    import pandas as pd
    import streamlit as st
    from src.plot import clean_data, generate_histogram, generate_scatter_plot, load_data
    from st_aggrid import AgGrid, GridOptionsBuilder
    from utils import helpers

    try:
        st.markdown(
            """
                    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Libertinus+Sans:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
                    """,
            unsafe_allow_html=True,
        )
        with open('style.css') as f:
            css_content = f.read()
        with open('script.js') as f:
            js_content = f.read()
        css_vars = helpers.generate_css()
        st.markdown(f'<style>{css_vars}{css_content}</style>', unsafe_allow_html=True)
        st.set_page_config(page_title='Crossfit Data')
        df = load_data()

        @st.fragment
        def download_data(df: pd.DataFrame, x_axis, y_axis, fig):
            """Download data as a zip file containing the filtered data and the scatter plot.

            Args:
                df (pd.DataFrame): The dataframe to download
                x_axis (str): The x axis column name
                y_axis (str): The y axis column name
                fig: the plotly figure



            .. code-block:: python


                fig = download_data(
                    df,
                    x_axis,
                    y_axis,
                    fig,
                )

            """
            cols_to_include = ['name', 'affiliate', 'region', 'team', 'gender', x_axis, y_axis]
            filtered_df = df[cols_to_include].copy()

            # captilize
            filtered_df.columns = [col.capitalize() for col in filtered_df.columns]

            # convert to int
            for col in filtered_df.columns:
                if filtered_df[col].dtype == 'float64':
                    filtered_df[col] = filtered_df[col].astype(int)

            zip_buffer = io.BytesIO()

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # image
            img_buffer = io.BytesIO()
            fig.write_image(img_buffer, format='png', width=1000, height=800)

            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                csv = filtered_df.to_csv(index=False)
                zip_file.writestr('crossfit_data.csv', csv)

                metadata = f"""
    Generated at: {timestamp}
    X Axis: {x_axis}
    Y Axis: {y_axis}
    Trendline: {trendline_options.get(trendline)}
    Records: {len(filtered_df)}
    Columns: {', '.join(filtered_df.columns)}
    """

                zip_file.writestr('metadata.txt', metadata)
                zip_file.writestr('scatter.png', img_buffer.getvalue())

            st.download_button(
                label='Download Data',
                data=zip_buffer.getvalue(),
                file_name=f'crossfit_data_{timestamp}.zip',
                mime='application/zip',
            )

        with st.sidebar:
            st.subheader('Options')

            numeric_columns = (
                df.select_dtypes(include=['number'])
                .drop(['athlete_id'], axis='columns')
                .columns.tolist()
            )

            x_default = numeric_columns[0]

            x_selection = helpers.get_url_param(key='x_axis', default=x_default)
            if x_selection not in numeric_columns:
                x_selection = x_default
                st.query_params.update({'x_axis': x_selection})

            x_axis = st.selectbox(
                label='X axis',
                options=numeric_columns,
                format_func=helpers.get_event_info,
                key='x_axis',
                index=numeric_columns.index(x_selection),
                on_change=lambda: st.query_params.update({'x_axis': st.session_state.x_axis}),
            )
            x_axis_display = helpers.get_event_info(x_axis)

            # we dont want x axis and y axis to be the same
            y_values = [col for col in numeric_columns if col != x_axis]
            y_default = y_values[0]
            y_selection = helpers.get_url_param(key='y_axis', default=y_default)
            if y_selection == x_selection or y_selection not in y_values:
                y_selection = y_default
                st.query_params.update({'y_axis': y_selection})
            y_axis = st.selectbox(
                label='Y axis',
                options=y_values,
                format_func=helpers.get_event_info,
                key='y_axis',
                index=y_values.index(y_selection),
                on_change=lambda: st.query_params.update({'y_axis': st.session_state.y_axis}),
            )
            y_axis_display = helpers.get_event_info(y_axis)

            with st.sidebar.container():
                st.subheader(f'{x_axis_display} ({helpers.get_event_info(x_axis, "unit")})')
                x_threshold_lower = st.number_input(
                    f'Select lower bound for {x_axis_display}', value=0, min_value=0
                )
                x_threshold_upper = st.number_input(
                    f'Select upper bound for {x_axis_display}', value=1000, min_value=0
                )
                x_std_slider = (
                    st.slider(
                        'Remove outliers beyond deviation:',
                        min_value=0.0,
                        max_value=5.0,
                        value=3.0,
                        step=0.1,
                        key='x_slider',
                    )
                    if st.checkbox('Remove Outliers', key='x_outliers')
                    else 0
                )
            with st.sidebar.container():
                st.subheader(f'{y_axis_display} ({helpers.get_event_info(y_axis, "unit")})')
                y_threshold_lower = st.number_input(
                    f'Select lower bound for {y_axis_display}', value=0, min_value=0
                )
                y_threshold_upper = st.number_input(
                    f'Select lower bound for {y_axis_display}', value=1000, min_value=0
                )
                y_std_slider = (
                    st.slider(
                        'Remove outliers beyond deviation:',
                        min_value=0.0,
                        max_value=5.0,
                        value=3.0,
                        step=0.1,
                        key='y_slider',
                    )
                    if st.checkbox('Remove Outliers', key='y_outliers')
                    else 0
                )
            x_threshold = (x_threshold_lower, x_threshold_upper)
            y_threshold = (y_threshold_lower, y_threshold_upper)
            trendline_options = {
                'ols': 'Ordinary Least Squares',
                'expanding': 'Expanding',
                'lowess': 'Locally Weighted Scatterplot Smoothing',
            }
            trendline = st.selectbox(
                label='Trendline',
                options=trendline_options.keys(),
                format_func=lambda func: trendline_options.get(func, func),
                key='trendline',
            )
            sample_size = st.radio('Select a sample size', options=[1000, 10000, 100000])
            (df, (x_mean, x_std), (y_mean, y_std), (x_lower, x_upper), (y_lower, y_upper)) = (
                clean_data(
                    df=df,
                    sample_size=sample_size,
                    x_axis=x_axis,
                    y_axis=y_axis,
                    x_thresholds=x_threshold,
                    y_thresholds=y_threshold,
                    standard_deviations=(x_std_slider, y_std_slider),
                )
            )

        scatter_tab, stabs_tab = st.tabs(['Scatter', 'Stats'])
        with scatter_tab:
            fig = generate_scatter_plot(df=df, x_axis=x_axis, y_axis=y_axis, trendline=trendline)
            download_data(df=df, x_axis=x_axis, y_axis=y_axis, fig=fig)

            st.plotly_chart(fig)
            if st.checkbox('Show Statistics'):
                st.subheader('Averages')
                st.markdown(
                    f'**{x_axis_display}**: {helpers.format_value(value=df[x_axis].mean(), axis_name=x_axis)}'
                )
                st.markdown(
                    f'**{y_axis_display}**: {helpers.format_value(value=df[y_axis].mean(), axis_name=y_axis)}'
                )

            if helpers.get_event_info(x_axis, 'better') == 'lower':
                top_athletes = df.nsmallest(5, x_axis)[['name', x_axis, y_axis]].to_dict('records')
            else:
                top_athletes = df.nlargest(5, x_axis)[['name', x_axis, y_axis]].to_dict('records')

            athlete_html = f"""
            <style>
            {css_vars}
            {css_content}
            </style>
            <script>
            const x_axis = '{x_axis}';
            const y_axis = '{y_axis}';
            {js_content}
            </script>
            <div>
                <div class='athletes-section'>
                    <h3>Top 5 athletes by {x_axis_display}
                </div>
                <div>
                {
                ''.join(
                    [
                        f'''
                    <div class='athlete-card' onclick="toggleCard(this)" data-{x_axis}="{athlete[x_axis]}" data-{y_axis}="{athlete[y_axis]}">
                        <h4 class='athlete-name'>{athlete['name']}</h4>
                        <p>
                            <span class='stat-label'>{x_axis_display}:</span>{helpers.format_value(athlete[x_axis], x_axis)}<br>
                            <span class='stat-label'>{y_axis_display}:</span>{helpers.format_value(athlete[y_axis], y_axis)}
                        </p>
                    </div>

                    
                    '''
                        for athlete in top_athletes
                    ]
                )
            }
                    <div class="stats-summary" id="statsSummary">
                        <h4 class="stats-title">Selected total</h4>
                        <p>
                            <span class='stat-label'>{
                x_axis_display
            } Total:</span><span class="stats-value" id="xAxisTotal">0</span><br>
                            <span class='stat-label'>{
                y_axis_display
            } Total:</span><span class="stats-value" id="yAxisTotal">0</span><br>
                            <span class='stat-label'>Total Athletes:</span><span class="stats-value" id="athleteCount">0</span>
                        </p>
                    </div>

                    
                </div>
            </div>
    """

            st.components.v1.html(athlete_html, height=1200)

            st.subheader('Events')

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    f"""
                            <div class='event-card'>
                                <div class='event-title'>{x_axis_display}</div>
                                <div class='event-description'>{helpers.get_event_info(x_axis, 'description')}</div>
                                <div class='event-meta'>
                                    <div class='event-unit'>{helpers.get_event_info(x_axis, 'unit')}</div>
                                </div>
                            </div>
                            """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                            <div class='event-card'>
                                <div class='event-title'>{y_axis_display}</div>
                                <div class='event-description'>{helpers.get_event_info(y_axis, 'description')}</div>
                                <div class='event-meta'>
                                    <div class='event-unit'>{helpers.get_event_info(y_axis, 'unit')}</div>
                                </div>
                            </div>
                            """,
                    unsafe_allow_html=True,
                )

            if st.toggle('Raw Data'):
                gender_options = df['gender'].unique().tolist()
                selected_genders = st.multiselect('Gender', options=gender_options)
                df = df[df['gender'].isin(selected_genders)] if selected_genders else df
                gb = GridOptionsBuilder.from_dataframe(df)
                for col in df.select_dtypes(include=['object']).columns:
                    gb.configure_column(
                        col, type=['textColumn', 'textColumnFilter'], filter='agTextColumnFilter'
                    )
                grid_options = gb.build()

                # pagination
                grid_options['pagination'] = True
                grid_options['paginationAutoPageSize'] = False
                grid_options['paginationPageSizeSelector'] = [5, 10, 20, 50, 100]
                AgGrid(df, gridOptions=grid_options, key='raw_data')
        with stabs_tab:
            x_histogram = generate_histogram(df, x_axis, x_mean, x_std)
            st.plotly_chart(x_histogram, use_container_width=True, theme=None)
            col = st.columns(2)
            with col[0]:
                st.markdown(f'**{x_axis_display} mean**: {x_mean:.2f}')
            with col[1]:
                st.markdown(f'**{x_axis_display} std**: {x_std:.2f}')
                st.markdown(f'**{x_axis_display} lower**: {x_lower:.2f}')
                st.markdown(f'**{x_axis_display} upper**: {x_upper:.2f}')
            y_histogram = generate_histogram(df, y_axis, y_mean, y_std)
            st.plotly_chart(y_histogram, use_container_width=False, theme='streamlit')
            col = st.columns(2)
            with col[0]:
                st.markdown(f'**{y_axis_display} mean**: {y_mean:.2f}')
            with col[1]:
                st.markdown(f'**{y_axis_display} std**: {y_std:.2f}')
                st.markdown(f'**{y_axis_display} lower**: {y_lower:.2f}')
                st.markdown(f'**{y_axis_display} upper**: {y_upper:.2f}')
    except Exception:
        st.error('an error has occured. please contact admin')
        print(traceback.format_exc())


if __name__ == '__main__':
    main()
