import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    """Provide a test client with isolated in-memory activity data."""
    # Arrange: snapshot shared in-memory state before each test.
    original_activities = copy.deepcopy(activities)

    with TestClient(app) as test_client:
        yield test_client

    # Assert/cleanup: restore shared in-memory state after each test.
    activities.clear()
    activities.update(original_activities)
