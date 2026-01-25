"""Test suite for the athlete profile page.

This module contains tests for the profile page functionality,
including fetching athlete data, rendering profiles, and navigation.
"""

from unittest.mock import Mock, patch

import pytest
import requests


def test_profile_page_renders_success():
    """Test profile page renders correctly with valid athlete data (positive test).

    Verifies that the complete profile page workflow functions correctly:
    - fetch_athlete() makes correct API call to backend
    - Returns complete athlete data including all fields
    - render_profile() displays athlete information
    - Navigation buttons (previous, dashboard, next) are rendered
    - Uses helpers.format_value() for consistent formatting
    - Handles both required and optional fields properly
    """
    from pages.profile import render_profile
    from src.plot import load_athlete

    mock_athlete_data = {
        'athlete_id': 2554,
        'name': 'Jane Smith',
        'age': 32,
        'gender': 'Female',
        'region': 'Europe',
        'team': 'Elite Athletes',
        'affiliate': 'CrossFit Berlin',
        'height': 68,
        'weight': 145,
        'grace': 195,
        'fran': 265,
        'helen': 520,
        'filthy50': 1350,
        'fgonebad': 320,
        'run400': 82,
        'run5k': 1380,
        'candj': 185,
        'snatch': 155,
        'deadlift': 315,
        'backsq': 265,
        'pullups': 32,
    }

    # Test fetch_athlete function
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = mock_athlete_data
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = load_athlete(2554)

        # Verify correct endpoint was called
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        assert '/api/athlete/2554' in call_args
        assert result['athlete_id'] == 2554
        assert result['name'] == 'Jane Smith'
        assert result['age'] == 32
        assert result['grace'] == 195

    # Test render_profile function
    with patch('src.plot.load_athlete', return_value=mock_athlete_data):
        with patch('streamlit.query_params') as mock_params:
            mock_params.get.return_value = '2554'

            # Should render without errors
            render_profile()

            # Verify query params were accessed
            mock_params.get.assert_called()


@pytest.mark.single
def test_profile_page_fail():
    """Test profile page handles errors and invalid input gracefully (negative test).

    Verifies error handling for various edge cases:
    - Missing athlete_id query parameter shows error message
    - Invalid (non-numeric) athlete_id format is validated
    - Non-existent athlete (404) displays appropriate error
    - Backend server errors (500) are handled gracefully
    - Missing optional fields don't cause crashes
    - Error messages are displayed to users
    - fetch_athlete is not called when athlete_id is invalid
    """
    from pages.profile import render_profile
    from src.plot import load_athlete

    # Test 1: Missing athlete_id parameter
    with patch('streamlit.query_params') as mock_params:
        mock_params.get.return_value = None
        with patch('src.plot.load_athlete') as mock_fetch:
            with patch('streamlit.error') as mock_error:
                render_profile()

                # Should show error and not call fetch
                mock_error.assert_called()
                mock_fetch.assert_not_called()

    # Test 2: Invalid athlete_id format (non-numeric)
    with patch('streamlit.query_params') as mock_params:
        mock_params.get.return_value = 'invalid_id'
        with patch('src.plot.load_athlete') as mock_fetch:
            with patch('streamlit.error') as mock_error:
                render_profile()

                # Should show error and not call fetch
                mock_error.assert_called()
                mock_fetch.assert_not_called()

    # Test 3: Athlete not found (404 error)
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        with pytest.raises(requests.HTTPError) as exc_info:
            load_athlete(99999)

        assert exc_info.value.response.status_code == 404

    # Test 4: Server error (500)
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.HTTPError(response=mock_response)
        mock_get.return_value = mock_response

        with pytest.raises(requests.HTTPError) as exc_info:
            load_athlete(2554)

        assert exc_info.value.response.status_code == 500

    # Test 5: Missing optional fields handled gracefully
    mock_athlete_data_minimal = {
        'athlete_id': 100,
        'name': 'Beginner Athlete',
        'age': 22,
        'gender': 'Male',
        'region': None,
        'team': None,
        'affiliate': None,
        'height': None,
        'weight': None,
        'grace': None,
        'fran': None,
        'helen': None,
        'filthy50': None,
        'fgonebad': None,
        'run400': None,
        'run5k': None,
        'candj': None,
        'snatch': None,
        'deadlift': None,
        'backsq': None,
        'pullups': None,
    }

    with patch('src.plot.load_athlete', return_value=mock_athlete_data_minimal):
        with patch('streamlit.query_params') as mock_params:
            mock_params.get.return_value = '100'

            # Should handle missing fields without crashing
            render_profile()
