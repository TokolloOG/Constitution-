"""
Pytest configuration and fixtures for HeavenET tests.
Provides Flask test client for all test modules.
"""

import pytest
from server import app


@pytest.fixture
def client():
    """
    Create a test client for the Flask app.
    
    Yields:
        FlaskClient: Test client connected to Flask app in testing mode
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client