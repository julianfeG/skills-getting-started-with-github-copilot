"""Fixtures and configuration for tests"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 3,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 3,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 3,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argument skills through competitive debate",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 3,
            "participants": ["alex@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Join the varsity soccer team and compete in regional tournaments",
            "schedule": "Tuesdays, Thursdays, Saturdays, 3:30 PM - 5:00 PM",
            "max_participants": 3,
            "participants": ["lucas@mergington.edu", "maya@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore biology, chemistry, and physics through hands-on experiments",
            "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 3,
            "participants": ["noah@mergington.edu"]
        },
        "Math Club": {
            "description": "Solve challenging math problems and prepare for competitions",
            "schedule": "Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 3,
            "participants": ["isabelle@mergington.edu", "james@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 3,
            "participants": ["grace@mergington.edu"]
        },
        "Music Band": {
            "description": "Play instruments and perform at school concerts and events",
            "schedule": "Mondays, Wednesdays, Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 3,
            "participants": ["carlo@mergington.edu", "rose@mergington.edu"]
        },
        "Art Club": {
            "description": "Create paintings, sculptures, and digital art under professional guidance",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 3,
            "participants": ["zoe@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design and build robots, participate in robotics competitions",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 3,
            "participants": ["tyler@mergington.edu", "hannah@mergington.edu"]
        },
        "Environmental Club": {
            "description": "Work on sustainability projects and environmental conservation initiatives",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 3,
            "participants": ["leo@mergington.edu"]
        },
        "Photography Club": {
            "description": "Learn photography techniques and showcase your creative vision",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 3,
            "participants": ["victoria@mergington.edu", "ryan@mergington.edu"]
        }
    }
    
    # Clear current activities
    activities.clear()
    # Restore original state
    activities.update(original_activities)
    
    yield
    
    # Cleanup after test
    activities.clear()
    activities.update(original_activities)
