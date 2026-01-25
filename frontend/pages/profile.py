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
