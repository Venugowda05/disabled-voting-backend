from fastapi import FastAPI

app = FastAPI()

# Temporary in-memory storage
ballots_list = []

@app.get("/")
def read_root():
    return {"message": "Backend is working!"}

# Get ballots
@app.get("/ballots")
def get_ballots():
    return ballots_list

# Add a dummy ballot
@app.post("/seed-ballot")
def seed_ballot():
    dummy_ballot = {
        "id": 1,
        "title": "Test Election",
        "options": [
            {"id": 1, "text": "Option 1"},
            {"id": 2, "text": "Option 2"}
        ]
    }
    ballots_list.append(dummy_ballot)
    return {"message": "Dummy ballot added", "ballot": dummy_ballot}
