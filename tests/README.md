# FastAPI Backend Tests

This directory contains comprehensive tests for the Mergington High School API backend.

## Test Structure

The tests are organized into three modules:

- **`test_activities.py`** - Tests for the `/activities` endpoint
- **`test_signup_unregister.py`** - Tests for signup and unregister endpoints
- **`test_participants.py`** - Tests for participant-related endpoints

## Running Tests

### Run all tests
```bash
python -m pytest tests/ -v
```

### Run specific test file
```bash
python -m pytest tests/test_activities.py -v
```

### Run specific test function
```bash
python -m pytest tests/test_signup_unregister.py::test_signup_new_student -v
```

### Run with coverage
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## Test Fixtures

The `conftest.py` file provides two key fixtures:

- **`client`** - A FastAPI TestClient for making requests to the app
- **`reset_activities`** - Resets the in-memory activity database to its initial state before each test

## Test Pattern: AAA (Arrange-Act-Assert)

All tests follow the **AAA pattern** for clear structure and readability:

```python
def test_example(client, reset_activities):
    """Test description."""
    
    # Arrange: Set up test data and preconditions
    email = "student@mergington.edu"
    activity_name = "Chess Club"
    
    # Act: Execute the code being tested
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert: Verify the results
    assert response.status_code == 200
    assert email in response.json()["message"]
```

**Benefits of AAA:**
- ✨ Clear test intent and flow
- ✨ Easy to identify setup, execution, and verification
- ✨ Simpler to debug failing tests
- ✨ Consistent structure across all tests

## Test Coverage

- ✅ Retrieving all activities
- ✅ Activity structure validation
- ✅ Student signup (new students, duplicate prevention)
- ✅ Student unregistration
- ✅ Participant list retrieval
- ✅ Error handling (nonexistent activities, invalid operations)
- ✅ Edge cases (email whitespace normalization, multiple activity enrollment)

## Requirements

Make sure the test dependencies are installed:

```bash
pip install -r requirements.txt
```

This includes `pytest` and `pytest-asyncio` for running the tests.
