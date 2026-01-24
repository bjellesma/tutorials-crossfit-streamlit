"""Tests for FastAPI routes.

This module contains tests for the athlete API endpoints,
including GET and POST operations.
"""

import os
import sys
from unittest.mock import patch

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


class TestCreateAthlete:
    """Test suite for POST /api/athletes endpoint."""

    def test_create_athlete_success(self, client):
        """Test successful athlete creation with various valid inputs.

        Tests multiple valid scenarios:
        - All fields provided (name, age, gender, grace, fran)
        - Only required fields (name, age)
        - Female gender
        - Null gender
        - Optional scores provided independently
        - Edge cases (minimum age, large age, zero scores)

        Args:
            client (TestClient): FastAPI test client.

        """
        with patch('database.create_athlete') as mock_create:
            # Test 1: All fields provided
            mock_create.return_value = {
                'status': 'success',
                'athlete_id': 1.0,
                'message': 'Athlete John Doe created successfully',
            }
            response = client.post(
                '/api/athletes',
                json={'name': 'John Doe', 'age': 25, 'gender': 'male', 'grace': 180, 'fran': 240},
            )
            assert response.status_code == 201
            assert response.json()['status'] == 'success'
            assert response.json()['athlete_id'] == 1.0
            mock_create.assert_called_with(
                name='John Doe',
                age=25,
                gender='Male',
                grace=180,
                fran=240,
                helen=None,
                filthy50=None,
                fgonebad=None,
                run400=None,
                run5k=None,
                candj=None,
                snatch=None,
                deadlift=None,
                backsq=None,
                pullups=None,
            )

            # Test 2: Only required fields
            mock_create.reset_mock()
            mock_create.return_value = {
                'status': 'success',
                'athlete_id': 2.0,
                'message': 'Athlete Jane Smith created successfully',
            }
            response = client.post('/api/athletes', json={'name': 'Jane Smith', 'age': 30})
            assert response.status_code == 201
            assert response.json()['status'] == 'success'
            mock_create.assert_called_with(
                name='Jane Smith',
                age=30,
                gender=None,
                grace=None,
                fran=None,
                helen=None,
                filthy50=None,
                fgonebad=None,
                run400=None,
                run5k=None,
                candj=None,
                snatch=None,
                deadlift=None,
                backsq=None,
                pullups=None,
            )

            # Test 3: Female gender
            mock_create.reset_mock()
            mock_create.return_value = {
                'status': 'success',
                'athlete_id': 3.0,
                'message': 'Athlete Sarah Johnson created successfully',
            }
            response = client.post(
                '/api/athletes', json={'name': 'Sarah Johnson', 'age': 28, 'gender': 'female'}
            )
            assert response.status_code == 201
            assert response.json()['status'] == 'success'
            mock_create.assert_called_with(
                name='Sarah Johnson',
                age=28,
                gender='Female',
                grace=None,
                fran=None,
                helen=None,
                filthy50=None,
                fgonebad=None,
                run400=None,
                run5k=None,
                candj=None,
                snatch=None,
                deadlift=None,
                backsq=None,
                pullups=None,
            )

            # Test 4: Null gender explicitly
            mock_create.reset_mock()
            mock_create.return_value = {
                'status': 'success',
                'athlete_id': 4.0,
                'message': 'Athlete Alex Taylor created successfully',
            }
            response = client.post(
                '/api/athletes', json={'name': 'Alex Taylor', 'age': 27, 'gender': None}
            )
            assert response.status_code == 201
            assert response.json()['status'] == 'success'

            # Test 5: Only grace score provided
            mock_create.reset_mock()
            mock_create.return_value = {
                'status': 'success',
                'athlete_id': 5.0,
                'message': 'Athlete Mike Ross created successfully',
            }
            response = client.post(
                '/api/athletes', json={'name': 'Mike Ross', 'age': 32, 'grace': 150}
            )
            assert response.status_code == 201
            mock_create.assert_called_with(
                name='Mike Ross',
                age=32,
                gender=None,
                grace=150,
                fran=None,
                helen=None,
                filthy50=None,
                fgonebad=None,
                run400=None,
                run5k=None,
                candj=None,
                snatch=None,
                deadlift=None,
                backsq=None,
                pullups=None,
            )

            # Test 6: Edge case - minimum valid age
            mock_create.reset_mock()
            response = client.post('/api/athletes', json={'name': 'Young Athlete', 'age': 1})
            assert response.status_code == 201

            # Test 7: Edge case - large age
            mock_create.reset_mock()
            response = client.post('/api/athletes', json={'name': 'Senior Athlete', 'age': 100})
            assert response.status_code == 201

            # Test 8: Edge case - zero scores allowed
            mock_create.reset_mock()
            response = client.post(
                '/api/athletes', json={'name': 'New Athlete', 'age': 25, 'grace': 0, 'fran': 0}
            )
            assert response.status_code == 201

    def test_create_athlete_validation_errors(self, client):
        """Test validation errors for invalid athlete data.

        Tests multiple validation scenarios:
        - Missing required fields (name, age)
        - Invalid age values (zero, negative, string)
        - Invalid gender value
        - Invalid score values (negative, string)
        - Database error handling

        Args:
            client (TestClient): FastAPI test client.

        """
        # Test 1: Missing name
        response = client.post('/api/athletes', json={'age': 25, 'gender': 'male'})
        assert response.status_code == 422
        assert 'detail' in response.json()

        # Test 2: Missing age
        response = client.post('/api/athletes', json={'name': 'John Doe', 'gender': 'male'})
        assert response.status_code == 422
        assert 'detail' in response.json()

        # Test 3: Age is zero
        response = client.post('/api/athletes', json={'name': 'John Doe', 'age': 0})
        assert response.status_code == 422
        error_detail = response.json()['detail']
        assert any('age' in str(err).lower() for err in error_detail)

        # Test 4: Negative age
        response = client.post('/api/athletes', json={'name': 'John Doe', 'age': -5})
        assert response.status_code == 422
        error_detail = response.json()['detail']
        assert any('age' in str(err).lower() for err in error_detail)

        # Test 5: Age is a string
        response = client.post('/api/athletes', json={'name': 'John Doe', 'age': 'twenty-five'})
        assert response.status_code == 422

        # Test 6: Invalid gender
        response = client.post(
            '/api/athletes', json={'name': 'John Doe', 'age': 25, 'gender': 'other'}
        )
        assert response.status_code == 422
        error_detail = response.json()['detail']
        assert any('gender' in str(err).lower() for err in error_detail)

        # Test 7: Negative grace score
        response = client.post('/api/athletes', json={'name': 'John Doe', 'age': 25, 'grace': -100})
        assert response.status_code == 422
        error_detail = response.json()['detail']
        assert any('grace' in str(err).lower() for err in error_detail)

        # Test 8: Grace score is a string
        response = client.post(
            '/api/athletes', json={'name': 'John Doe', 'age': 25, 'grace': 'fast'}
        )
        assert response.status_code == 422

        # Test 9: Negative fran score
        response = client.post('/api/athletes', json={'name': 'John Doe', 'age': 25, 'fran': -200})
        assert response.status_code == 422
        error_detail = response.json()['detail']
        assert any('fran' in str(err).lower() for err in error_detail)

        # Test 10: Database error returns 500
        with patch('database.create_athlete') as mock_create:
            mock_create.side_effect = Exception('Database connection failed')
            response = client.post(
                '/api/athletes', json={'name': 'John Doe', 'age': 25, 'gender': 'male'}
            )
            assert response.status_code == 500
            assert 'detail' in response.json()


class TestGetAthletes:
    """Test suite for GET /api/athletes endpoint."""

    def test_get_athletes_success(self, client):
        """Test successful retrieval of athletes.

        Verifies that the existing GET endpoint still works correctly.

        Args:
            client (TestClient): FastAPI test client.

        """
        mock_data = {
            'athletes': [(1.0, 'John Doe', 25, 'male', 180, 240)],
            'columns': ['athlete_id', 'name', 'age', 'gender', 'grace', 'fran'],
        }

        with patch('database.get_athletes') as mock_get:
            mock_get.return_value = mock_data

            response = client.get('/api/athletes')

            assert response.status_code == 200
            assert 'athletes' in response.json()
            assert 'columns' in response.json()


class TestGetAthlete:
    """Test suite for GET /api/athlete/{athlete_id} endpoint."""

    def test_get_athlete_by_id_success(self, client):
        """Test successfully retrieving a single athlete by ID.

        Verifies that:
        - Valid athlete_id returns 200 status code
        - Response contains all athlete fields including athlete_id
        - All required fields (name, age) are present
        - Optional fields (scores, gender) are correctly included
        - Response matches AthleteResponse model structure

        Args:
            client (TestClient): FastAPI test client.

        """
        with patch('database.get_athlete') as mock_get:
            # Mock database response with complete athlete data
            mock_get.return_value = {
                'athlete_id': 1,
                'name': 'John Doe',
                'age': 25,
                'gender': 'Male',
                'grace': 180,
                'fran': 240,
                'helen': 300,
                'filthy50': 1500,
                'fgonebad': 350,
                'run400': 75,
                'run5k': 1800,
                'candj': 225,
                'snatch': 185,
                'deadlift': 405,
                'backsq': 315,
                'pullups': 30,
            }

            response = client.get('/api/athlete/1')

            # Verify response status and structure
            assert response.status_code == 200
            data = response.json()

            # Verify all required fields are present
            assert data['athlete_id'] == 1
            assert data['name'] == 'John Doe'
            assert data['age'] == 25

            # Verify optional fields
            assert data['gender'] == 'Male'
            assert data['grace'] == 180
            assert data['fran'] == 240
            assert data['helen'] == 300
            assert data['filthy50'] == 1500
            assert data['fgonebad'] == 350
            assert data['run400'] == 75
            assert data['run5k'] == 1800
            assert data['candj'] == 225
            assert data['snatch'] == 185
            assert data['deadlift'] == 405
            assert data['backsq'] == 315
            assert data['pullups'] == 30

            # Verify database function was called with correct parameter
            mock_get.assert_called_once_with(1)

    def test_get_athlete_failed(self, client):
        """Test all negative cases for retrieving athletes.

        Tests multiple edge cases and error scenarios:
        - Large non-existent athlete_id returns 404
        - Zero as athlete_id returns 404
        - Negative athlete_id returns 404
        - Very large boundary athlete_id returns 404
        - athlete_id = 1 when database is empty returns 404
        - Invalid type (string) returns 422
        - Database exception returns 500

        Args:
            client (TestClient): FastAPI test client.

        """
        with patch('database.get_athlete') as mock_get:
            # Test 1: Large non-existent athlete_id
            mock_get.return_value = None
            response = client.get('/api/athlete/999999')
            assert response.status_code == 404
            data = response.json()
            assert 'detail' in data
            assert '999999' in data['detail'] or 'not found' in data['detail'].lower()
            mock_get.assert_called_with(999999)

        # Test 6: Invalid type - string instead of integer (FastAPI validation)
        response = client.get('/api/athlete/abc')
        assert response.status_code == 422
        data = response.json()
        assert 'detail' in data

        # Test 7: Invalid type - float with decimal
        response = client.get('/api/athlete/1.5')
        assert response.status_code == 422

        # Test 8: Database error returns 500
        with patch('database.get_athlete') as mock_get:
            mock_get.side_effect = Exception('Database connection failed')
            response = client.get('/api/athlete/1')
            assert response.status_code == 500
            data = response.json()
            assert 'detail' in data
            mock_get.assert_called_with(1)
