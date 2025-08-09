from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import database, models, schemas

app = FastAPI()

# DB Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Startup: Create tables
@app.on_event("startup")
def startup():
    database.Base.metadata.create_all(bind=database.engine)

# Root
@app.get("/")
def read_root():
    return {"message": "Backend is working!"}

# Voter registration
@app.post("/register")
def register_voter(voter: schemas.VoterCreate, db: Session = Depends(get_db)):
    if db.query(models.Voter).filter(models.Voter.voter_id == voter.voter_id).first():
        raise HTTPException(status_code=400, detail="Voter ID already registered")
    new_voter = models.Voter(**voter.dict(), has_voted=False)
    db.add(new_voter)
    db.commit()
    db.refresh(new_voter)
    return {"message": "Voter registered successfully"}

# Submit vote
@app.post("/vote")
def vote(vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    voter = db.query(models.Voter).filter(models.Voter.voter_id == vote.voter_id).first()
    if not voter:
        raise HTTPException(status_code=404, detail="Voter not found")
    if voter.has_voted:
        raise HTTPException(status_code=400, detail="Voter has already voted")
    voter.has_voted = True
    voter.vote_choice = vote.choice
    db.commit()
    return {"message": "Vote submitted successfully"}

# Results
@app.get("/results")
def get_results(db: Session = Depends(get_db)):
    results = db.query(models.Voter.vote_choice).all()
    return {"total_votes": len(results)}

# ✅ Create ballot
@app.post("/ballots")
def create_ballot(ballot: schemas.BallotCreate, db: Session = Depends(get_db)):
    new_ballot = models.Ballot(title=ballot.title)
    db.add(new_ballot)
    db.commit()
    db.refresh(new_ballot)
    for opt in ballot.options:
        new_option = models.Option(text=opt.text, ballot_id=new_ballot.id)
        db.add(new_option)
    db.commit()
    return {"message": "Ballot created", "ballot_id": new_ballot.id}

# ✅ Get ballots (for frontend dropdown)
@app.get("/ballots")
def get_ballots(db: Session = Depends(get_db)):
    ballots = db.query(models.Ballot).all()
    results = []
    for b in ballots:
        results.append({
            "id": b.id,
            "title": b.title,
            "options": [{"id": o.id, "text": o.text} for o in b.options]
        })
    return results
