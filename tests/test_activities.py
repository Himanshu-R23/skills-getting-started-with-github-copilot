"""Tests for activity-related endpoints."""

import pytest


def test_get_activities(client, reset_activities):
    """Test getting all activities."""
    
    # Arrange
    # Activities fixture provides initial state
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Robotics Club" in data


def test_get_activities_chess_club_details(client, reset_activities):
    """Test that activities have correct structure and details."""
    
    # Arrange
    activity_name = "Chess Club"
    expected_description = "Learn strategies and compete in chess tournaments"
    expected_schedule = "Fridays, 3:30 PM - 5:00 PM"
    expected_max_participants = 12
    expected_initial_participants = 2
    
    # Act
    response = client.get("/activities")
    data = response.json()
    chess_club = data[activity_name]
    
    # Assert
    assert response.status_code == 200
    assert chess_club["description"] == expected_description
    assert chess_club["schedule"] == expected_schedule
    assert chess_club["max_participants"] == expected_max_participants
    assert len(chess_club["participants"]) == expected_initial_participants
    assert "michael@mergington.edu" in chess_club["participants"]


def test_get_activities_all_have_required_fields(client, reset_activities):
    """Test that all activities have required fields."""
    
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in data.items():
        assert required_fields.issubset(activity_data.keys()), \
            f"Activity {activity_name} missing required fields"
        assert isinstance(activity_data["participants"], list), \
            f"Participants for {activity_name} should be a list"
