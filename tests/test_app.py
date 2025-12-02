import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Test signup
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200 or signup_resp.status_code == 400  # 400 if already signed up
    # Test unregister
    unregister_resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    # Unregister again should fail
    unregister_resp2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp2.status_code == 400

def test_signup_duplicate():
    email = "duplicate@mergington.edu"
    activity = "Programming Class"
    # First signup
    resp1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp1.status_code == 200
    # Duplicate signup
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400
    # Cleanup
    client.post(f"/activities/{activity}/unregister?email={email}")
