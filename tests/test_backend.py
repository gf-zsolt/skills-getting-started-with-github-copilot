import copy
from urllib.parse import quote
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

# Snapshot original activities to restore between tests
_original_activities = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory `activities` before each test (Arrange)."""
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))
    yield
    activities.clear()
    activities.update(copy.deepcopy(_original_activities))


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


def test_get_activities_contains_chess_club(client):
    # Arrange: client fixture

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_increases_participants_and_returns_200(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    url = f"/activities/{quote(activity)}/signup"
    before = client.get("/activities").json()[activity]["participants"]
    before_count = len(before)

    # Act
    res = client.post(url, params={"email": email})

    # Assert
    assert res.status_code == 200
    after = client.get("/activities").json()[activity]["participants"]
    assert email in after
    assert len(after) == before_count + 1


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already present in fixture data
    url = f"/activities/{quote(activity)}/signup"

    # Act
    res = client.post(url, params={"email": email})

    # Assert
    assert res.status_code == 400


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"
    url = f"/activities/{quote(activity)}/signup"

    # Act
    res = client.post(url, params={"email": email})

    # Assert
    assert res.status_code == 404


def test_delete_removes_participant_and_returns_200(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # existing participant
    url = f"/activities/{quote(activity)}/signup"
    before = client.get("/activities").json()[activity]["participants"]
    assert email in before

    # Act
    res = client.delete(url, params={"email": email})

    # Assert
    assert res.status_code == 200
    after = client.get("/activities").json()[activity]["participants"]
    assert email not in after


def test_delete_unknown_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "not-a-user@mergington.edu"
    url = f"/activities/{quote(activity)}/signup"

    # Act
    res = client.delete(url, params={"email": email})

    # Assert
    assert res.status_code == 404
