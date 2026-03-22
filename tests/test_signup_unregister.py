"""Tests for signup and unregister endpoints."""

import pytest


def test_signup_new_student(client, reset_activities):
    """Test signing up a new student to an activity."""
    
    # Arrange
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Signed up {email} for {activity_name}"
    
    # Verify student was added to activity
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_nonexistent_activity(client, reset_activities):
    """Test signing up to an activity that doesn't exist."""
    
    # Arrange
    email = "student@mergington.edu"
    activity_name = "Nonexistent Activity"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Activity not found"


def test_signup_duplicate_student(client, reset_activities):
    """Test that a student cannot sign up twice for the same activity."""
    
    # Arrange
    email = "duplicate@mergington.edu"
    activity_name = "Chess Club"
    
    # Act - First signup (should succeed)
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Try to sign up again (should fail)
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    data = response2.json()
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 400
    assert data["detail"] == "Student already signed up"


def test_signup_already_registered_student(client, reset_activities):
    """Test that already registered students can't sign up again."""
    
    # Arrange
    email = "michael@mergington.edu"  # Already registered in Chess Club
    activity_name = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 400
    assert data["detail"] == "Student already signed up"


def test_unregister_existing_participant(client, reset_activities):
    """Test unregistering an existing participant from an activity."""
    
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Unregistered {email} from {activity_name}"
    
    # Verify student was removed from activity
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_nonexistent_activity(client, reset_activities):
    """Test unregistering from a nonexistent activity."""
    
    # Arrange
    email = "student@mergington.edu"
    activity_name = "Nonexistent Activity"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Activity not found"


def test_unregister_nonexistent_participant(client, reset_activities):
    """Test unregistering a student who is not registered."""
    
    # Arrange
    email = "notregistered@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Participant not found"


def test_unregister_with_whitespace(client, reset_activities):
    """Test that unregister handles whitespace in emails."""
    
    # Arrange
    email = "student@test.edu"
    activity_name = "Programming Class"
    
    # Act - Sign up student
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Act - Unregister with whitespace around email
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": f" {email} "}
    )
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in data["message"]


def test_signup_multiple_activities(client, reset_activities):
    """Test that a student can sign up for multiple activities."""
    
    # Arrange
    student_email = "versatile@mergington.edu"
    activities_to_join = ["Chess Club", "Drama Club", "Robotics Club"]
    
    # Act - Sign up for multiple activities
    responses = []
    for activity_name in activities_to_join:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        responses.append(response)
    
    # Retrieve updated activities
    activities = client.get("/activities").json()
    
    # Assert - All signups successful
    for response in responses:
        assert response.status_code == 200
    
    # Assert - Student enrolled in all activities
    for activity_name in activities_to_join:
        assert student_email in activities[activity_name]["participants"]
