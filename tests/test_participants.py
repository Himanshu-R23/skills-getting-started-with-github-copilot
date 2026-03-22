"""Tests for participant-related endpoints."""

import pytest


def test_get_participants(client, reset_activities):
    """Test getting participants for an activity."""
    
    # Arrange
    activity_name = "Chess Club"
    expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get(f"/activities/{activity_name}/participants")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "participants" in data
    assert len(data["participants"]) == len(expected_participants)
    for email in expected_participants:
        assert email in data["participants"]


def test_get_participants_empty_activity(client, reset_activities):
    """Test getting participants for an activity with no participants."""
    
    # Arrange
    activity_name = "Programming Class"
    
    # Act
    response = client.get(f"/activities/{activity_name}/participants")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "participants" in data
    assert isinstance(data["participants"], list)


def test_get_participants_nonexistent_activity(client, reset_activities):
    """Test getting participants from a nonexistent activity."""
    
    # Arrange
    activity_name = "Fake Activity"
    
    # Act
    response = client.get(f"/activities/{activity_name}/participants")
    data = response.json()
    
    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Activity not found"


def test_get_participants_after_signup(client, reset_activities):
    """Test that participants list updates after a signup."""
    
    # Arrange
    activity_name = "Tennis Club"
    new_student = "newparticipant@mergington.edu"
    expected_total_participants = 3  # 2 original + 1 new
    
    # Act - Sign up the student
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_student}
    )
    
    # Act - Retrieve updated participants list
    response = client.get(f"/activities/{activity_name}/participants")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert new_student in data["participants"]
    assert len(data["participants"]) == expected_total_participants


def test_get_participants_after_unregister(client, reset_activities):
    """Test that participants list updates after an unregister."""
    
    # Arrange
    activity_name = "Chess Club"
    student_to_remove = "michael@mergington.edu"
    remaining_student = "daniel@mergington.edu"
    expected_remaining_count = 1
    
    # Act - Unregister the student
    client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": student_to_remove}
    )
    
    # Act - Retrieve updated participants list
    response = client.get(f"/activities/{activity_name}/participants")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert student_to_remove not in data["participants"]
    assert remaining_student in data["participants"]
    assert len(data["participants"]) == expected_remaining_count


def test_get_participants_section(client, reset_activities):
    """Test getting the participants section for an activity."""
    
    # Arrange
    activity_name = "Programming Class"
    
    # Act
    response = client.get(f"/activities/{activity_name}/participants-section")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "participants" in data


def test_get_participants_section_nonexistent_activity(client, reset_activities):
    """Test getting participants section from nonexistent activity."""
    
    # Arrange
    activity_name = "Fake Activity"
    
    # Act
    response = client.get(f"/activities/{activity_name}/participants-section")
    data = response.json()
    
    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Activity not found"
