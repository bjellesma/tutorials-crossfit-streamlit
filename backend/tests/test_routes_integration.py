"""Integration tests for FastAPI routes.

This module contains integration tests that interact with the actual database,
testing real database operations rather than mocked responses.
"""

import os
import sys

import pytest
from fastapi.testclient import TestClient

# Add the backend directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from routes import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app.

    Returns:
        TestClient: FastAPI test client instance.

    """
    return TestClient(app)


class TestGetAthleteIntegration:
    """Integration tests for GET /api/athlete/{athlete_id} endpoint."""

    def test_get_existing_athlete_from_database(self, client):
        """Test retrieving athlete ID 2554 from actual database.

        This integration test queries the real database to verify that:
        - The athlete with ID 2554 exists and can be retrieved
        - Gender field is properly normalized (uppercase Male/Female)
        - All athlete fields are returned correctly
        - Response validation passes with AthleteResponse model

        Args:
            client (TestClient): FastAPI test client.

        """
        # Query actual database for athlete ID 2554
        response = client.get('/api/athlete/2554')

        # Verify successful response
        assert response.status_code == 200
        data = response.json()

        # Verify required fields are present
        assert 'athlete_id' in data
        assert data['athlete_id'] == 2554
        assert data['name'] == 'Pj Ablang'
        assert 'age' in data

        # Verify gender is properly formatted (Male or Female, not lowercase)
        if data.get('gender') is not None:
            assert data['gender'] in ['Male', 'Female'], (
                f"Gender should be 'Male' or 'Female', got: {data['gender']}"
            )

        # Verify all expected fields are present
        expected_fields = [
            'athlete_id',
            'name',
            'age',
            'gender',
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
        for field in expected_fields:
            assert field in data, f'Missing field: {field}'
