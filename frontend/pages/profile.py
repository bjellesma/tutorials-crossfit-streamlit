"""Streamlit page for individual athlete profile view.

This module provides a detailed view of a single athlete's performance data,
including personal information and all workout metrics.
"""


def render_profile():
    """Display athlete profile page.

    Provides interface to search for and view detailed athlete information,
    including all workout scores and personal details. The page includes:
    - Athlete selection by ID
    - Personal information display (name, age, gender)
    - All workout metrics with proper formatting
    - Error handling for invalid or missing athletes

    Raises:
        requests.HTTPError: Displays error if athlete not found or request fails.

    """
    import traceback

    import requests
    import streamlit as st
    from src import api
    from src.plot import load_athlete, load_data
    from utils import helpers

    # Load custom CSS (same as main page)
    with open('style.css') as f:
        css_content = f.read()
    css_vars = helpers.generate_css()
    st.markdown(f'<style>{css_vars}{css_content}</style>', unsafe_allow_html=True)

    st.title('🏋️ Athlete Profile')

    # Load all athlete IDs for navigation
    try:
        df = load_data()
        athlete_ids = sorted(df['athlete_id'].dropna().astype(int).tolist())
    except Exception as e:
        traceback.print_exc()
        st.error(f'❌ Unable to load athlete IDs: {str(e)}')
        return

    # Check URL parameter
    athlete_id_param = helpers.get_url_param('athlete_id', None)
    if athlete_id_param:
        try:
            athlete_id_param = int(athlete_id_param)
        except ValueError:
            st.error('❌ Invalid athlete_id parameter in URL. Must be an integer.')
            return

        if athlete_id_param not in athlete_ids:
            st.error(f'❌ Athlete ID {athlete_id_param} not found in dataset.')
            return

    # Initialize or update session state for current index
    if 'athlete_index' not in st.session_state:
        # First load - initialize from URL param or default to 0
        if athlete_id_param and athlete_id_param in athlete_ids:
            st.session_state.athlete_index = athlete_ids.index(athlete_id_param)
        else:
            st.session_state.athlete_index = 0
    elif athlete_id_param and athlete_id_param in athlete_ids:
        # URL param exists and differs from current - sync session state
        current_id = athlete_ids[st.session_state.athlete_index]
        if current_id != athlete_id_param:
            st.session_state.athlete_index = athlete_ids.index(athlete_id_param)

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button(
            '⬅️ Previous', use_container_width=True, disabled=st.session_state.athlete_index == 0
        ):
            st.session_state.athlete_index -= 1
            st.query_params.update({'athlete_id': athlete_ids[st.session_state.athlete_index]})
            st.rerun()

    with col2:
        current_athlete_id = athlete_ids[st.session_state.athlete_index]
        st.markdown(
            f"<div style='text-align: center; padding: 8px;'>"
            f'<strong>Athlete {st.session_state.athlete_index + 1} of {len(athlete_ids)}</strong>'
            f'<br/>ID: {current_athlete_id}'
            f'</div>',
            unsafe_allow_html=True,
        )

    with col3:
        if st.button(
            'Next ➡️',
            use_container_width=True,
            disabled=st.session_state.athlete_index >= len(athlete_ids) - 1,
        ):
            st.session_state.athlete_index += 1
            st.query_params.update({'athlete_id': athlete_ids[st.session_state.athlete_index]})
            st.rerun()

    athlete_id = current_athlete_id

    # Load and display athlete data
    try:
        with st.spinner('Loading athlete data...'):
            athlete = load_athlete(athlete_id)

        # Personal Information Section
        st.markdown('---')
        st.subheader(f'{athlete["name"]}')

        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.metric('Athlete ID', athlete['athlete_id'])
        with info_col2:
            st.metric('Age', athlete['age'])
        with info_col3:
            gender_display = athlete.get('gender', 'N/A')
            if gender_display:
                gender_display = gender_display.capitalize()
            else:
                gender_display = 'N/A'
            st.metric('Gender', gender_display)

        # Workout Metrics Section
        st.markdown('---')
        st.subheader('📊 Workout Metrics')

        # Get all workout fields (exclude personal info)
        workout_fields = [
            'grace',
            'fran',
            'helen',
            'filthy50',
            'fgonebad',
            'run400',
            'run5k',
            'candj',
            'snatch',
            'deadlift',
            'backsq',
            'pullups',
        ]

        # Display in grid format (3 columns)
        rows = [workout_fields[i : i + 3] for i in range(0, len(workout_fields), 3)]

        for row in rows:
            cols = st.columns(3)
            for idx, field in enumerate(row):
                with cols[idx]:
                    value = athlete.get(field)
                    if value is not None:
                        display_name = helpers.get_event_info(field, 'display_name')
                        formatted_value = helpers.format_value(value, field)
                        description = helpers.get_event_info(field, 'description')

                        # Use custom card styling
                        st.markdown(
                            f"""
                                <div class='event-card'>
                                    <div class='event-title'>{display_name}</div>
                                    <div class='event-meta'>
                                        <div class='event-unit' style='font-size: 1.5rem; font-weight: bold;'>
                                            {formatted_value}
                                        </div>
                                    </div>
                                    <div class='event-description'>{description}</div>
                                </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        display_name = helpers.get_event_info(field, 'display_name')
                        st.info(f'{display_name}: No data')

        with st.form('prediction_form'):
            DEFAULT_VALUES = {
                'age': 25,
                'weight': 170.0,
                'pullups': 20,
                'backsq': 225,
                'deadlift': 315,
                'snatch': 135,
                'candj': 185,
            }
            col1, col2 = st.columns(2)

            with col1:
                form_age = st.number_input(
                    'Age',
                    min_value=1,
                    max_value=120,
                    value=int(athlete.get('age') or DEFAULT_VALUES['age']),
                    help='Athlete age in years',
                )
                form_gender = st.selectbox(
                    'Gender',
                    options=['male', 'female'],
                    index=0
                    if not athlete.get('gender') or athlete.get('gender', '').lower() == 'male'
                    else 1,
                    help='Athlete gender',
                )

                form_weight = st.number_input(
                    'Body Weight (lbs)',
                    min_value=1.0,
                    max_value=500.0,
                    value=float(athlete.get('weight') or DEFAULT_VALUES['weight']),
                    step=0.5,
                    help='Athlete body weight in pounds',
                )

                form_pullups = st.number_input(
                    'Pull-ups',
                    min_value=0,
                    max_value=200,
                    value=int(athlete.get('pullups') or DEFAULT_VALUES['pullups']),
                    help='Number of pull-ups',
                )

            with col2:
                form_backsq = st.number_input(
                    'Back Squat (lbs)',
                    min_value=0,
                    max_value=1000,
                    value=int(athlete.get('backsq') or DEFAULT_VALUES['backsq']),
                    help='Back squat weight in pounds',
                )

                form_deadlift = st.number_input(
                    'Deadlift (lbs)',
                    min_value=0,
                    max_value=1500,
                    value=int(athlete.get('deadlift') or DEFAULT_VALUES['deadlift']),
                    help='Deadlift weight in pounds',
                )

                form_snatch = st.number_input(
                    'Snatch (lbs)',
                    min_value=0,
                    max_value=800,
                    value=int(athlete.get('snatch') or DEFAULT_VALUES['snatch']),
                    help='Snatch weight in pounds',
                )

                form_candj = st.number_input(
                    'Clean & Jerk (lbs)',
                    min_value=0,
                    max_value=800,
                    value=int(athlete.get('candj') or DEFAULT_VALUES['candj']),
                    help='Clean and jerk weight in pounds',
                )

            submit_button = st.form_submit_button(
                '🔮 Get Prediction', width='stretch', shortcut='Enter'
            )
            if submit_button:
                try:
                    with st.spinner('Calculating prediction...'):
                        predicted_time = api.predict_run5k(
                            age=form_age,
                            gender=form_gender,
                            backsq=form_backsq,
                            deadlift=form_deadlift,
                            snatch=form_snatch,
                            candj=form_candj,
                            pullups=form_pullups,
                            weight=form_weight,
                        )
                    prediction = helpers.format_value(predicted_time, 'run5k')
                    st.success(f'**Predicted 5K Time:** {prediction}')

                    # If athlete has actual 5K time, show comparison
                    actual_run5k = athlete.get('run5k')
                    if actual_run5k:
                        formatted_actual = helpers.format_value(actual_run5k, 'run5k')
                        difference = actual_run5k - predicted_time

                        col_actual, col_diff = st.columns(2)

                        with col_actual:
                            st.metric('Actual Time', formatted_actual)

                        with col_diff:
                            # Positive difference means actual is slower (worse)
                            formatted_diff = helpers.format_value(abs(difference), 'run5k')
                            if difference > 0:
                                st.metric(
                                    'Difference',
                                    formatted_diff,
                                    delta='Slower than predicted',
                                    delta_color='inverse',
                                )
                            elif difference < 0:
                                st.metric(
                                    'Difference',
                                    formatted_diff,
                                    delta='Faster than predicted',
                                    delta_color='normal',
                                )
                            else:
                                st.metric('Difference', formatted_diff)
                except requests.HTTPError as e:
                    # check for a response object and status code to provide more specific error messages
                    if hasattr(e, 'response') and e.response is not None:
                        if e.response.status_code == 422:
                            st.error(helpers.generate_error_message(422, e))
                        elif e.response.status_code == 500:
                            st.error(helpers.generate_error_message(500, e))
                        else:
                            st.error(helpers.generate_error_message('prediction', e))
                    else:
                        st.error(helpers.generate_error_message('prediction', e))
                except requests.ConnectionError as e:
                    st.error(helpers.generate_error_message('connection', e))
                except Exception as e:
                    st.error(helpers.generate_error_message('unexpected', e))

    except requests.HTTPError as e:
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code == 404:
                st.error(f'❌ Athlete with ID {athlete_id} not found.')
            elif e.response.status_code == 422:
                st.error('❌ Invalid athlete ID format.')
            else:
                st.error(f'❌ Error loading athlete: {str(e)}')
        else:
            st.error(f'❌ Error loading athlete: {str(e)}')
    except requests.ConnectionError:
        st.error(
            '❌ Unable to connect to the backend server. Please ensure the backend is running.'
        )
    except Exception as e:
        st.error(f'❌ An unexpected error occurred: {str(e)}')


if __name__ == '__main__':
    render_profile()
