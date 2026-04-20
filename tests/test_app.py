"""Unit tests for the High School Management System API"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test"""
    original_state = {
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
    
    activities.clear()
    activities.update(original_state)
    yield
    activities.clear()
    activities.update(original_state)


class TestRoot:
    """Tests for the root endpoint"""
    
    def test_root_redirect(self, client):
        """Test that root redirects to static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


class TestGetActivities:
    """Tests for the GET /activities endpoint"""
    
    def test_get_all_activities(self, client):
        """Test retrieving all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 13
        assert "Chess Club" in data
        assert "Programming Class" in data
    
    def test_activity_structure(self, client):
        """Test that activities have the correct structure"""
        response = client.get("/activities")
        data = response.json()
        activity = data["Chess Club"]
        
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)
    
    def test_participants_list(self, client):
        """Test that participant lists are correct"""
        response = client.get("/activities")
        data = response.json()
        chess_club = data["Chess Club"]
        
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client):
        """Test successful signup"""
        response = client.post(
            "/activities/Science Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
        assert "newstudent@mergington.edu" in activities["Science Club"]["participants"]
    
    def test_signup_nonexistent_activity(self, client):
        """Test signup for non-existent activity"""
        response = client.post(
            "/activities/Non Existent Club/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_already_registered_in_another(self, client):
        """Test signup fails when email is already in another activity"""
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": "michael@mergington.edu"}  # Already in Chess Club
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_signup_activity_full(self, client):
        """Test signup fails when activity is full"""
        # Chess Club has 2 participants and max_participants is 3
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "student1@mergington.edu"}
        )
        assert response.status_code == 200
        
        # Try to add another - activity should now be full
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "student2@mergington.edu"}
        )
        assert response.status_code == 400
        assert "full" in response.json()["detail"]
    
    def test_signup_response_message(self, client):
        """Test signup response message format"""
        email = "newsignup@mergington.edu"
        response = client.post(
            "/activities/Math Club/signup",
            params={"email": email}
        )
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Math Club" in data["message"]


class TestRemoveFromActivity:
    """Tests for the POST /activities/{activity_name}/remove endpoint"""
    
    def test_remove_success(self, client):
        """Test successful removal from activity"""
        email = "michael@mergington.edu"
        response = client.post(
            "/activities/Chess Club/remove",
            params={"email": email}
        )
        assert response.status_code == 200
        assert email not in activities["Chess Club"]["participants"]
    
    def test_remove_nonexistent_activity(self, client):
        """Test removal from non-existent activity"""
        response = client.post(
            "/activities/Fake Club/remove",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_remove_email_not_in_activity(self, client):
        """Test removal of email not in activity"""
        response = client.post(
            "/activities/Chess Club/remove",
            params={"email": "notregistered@mergington.edu"}
        )
        assert response.status_code == 400
        assert "not found" in response.json()["detail"]
    
    def test_remove_response_message(self, client):
        """Test remove response message format"""
        email = "michael@mergington.edu"
        response = client.post(
            "/activities/Chess Club/remove",
            params={"email": email}
        )
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Chess Club" in data["message"]


class TestSignupAndRemoveFlow:
    """Tests for signup and removal flow together"""
    
    def test_signup_then_remove(self, client):
        """Test signing up and then removing"""
        email = "flowtest@mergington.edu"
        activity = "Science Club"
        
        # Signup
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        assert email in activities[activity]["participants"]
        
        # Remove
        response = client.post(
            f"/activities/{activity}/remove",
            params={"email": email}
        )
        assert response.status_code == 200
        assert email not in activities[activity]["participants"]
    
    def test_removed_email_can_signup_again(self, client):
        """Test that removed email can signup for the same activity"""
        email = "flowtest2@mergington.edu"
        activity = "Debate Team"
        
        # First signup
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Remove
        response = client.post(
            f"/activities/{activity}/remove",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Signup again
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        assert email in activities[activity]["participants"]
    
    def test_can_signup_after_leaving_other_activity(self, client):
        """Test that student can signup for another activity after leaving one"""
        email = "multiactivity@mergington.edu"
        
        # Signup for Science Club
        response = client.post(
            "/activities/Science Club/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Remove from Science Club
        response = client.post(
            "/activities/Science Club/remove",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Now signup for Programming Class
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        assert email in activities["Programming Class"]["participants"]
