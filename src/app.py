"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
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
        "participants": ["zoe@mergington.edu.co"]
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


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if email is already registered in another activity
    for other_activity_name, other_activity in activities.items():
        if other_activity_name != activity_name and email in other_activity["participants"]:
            raise HTTPException(status_code=400, detail=f"Email already registered in {other_activity_name}")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if email is already registered in this activity
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Email already registered in this activity")

    # Check if activity is full
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="This activity is full")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.post("/activities/{activity_name}/remove")
def remove_from_activity(activity_name: str, email: str):
    """Remove a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if email is in the activity
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Email not found in this activity")

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
