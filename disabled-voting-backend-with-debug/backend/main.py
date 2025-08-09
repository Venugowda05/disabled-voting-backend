from fastapi import FastAPI, HTTPException, Depends
from backend import database, models, schemas
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    database.Base.metadata.create_all(bind=database.engine)

@app.post("/register")
def register_voter(voter: schemas.VoterCreate, db: Session = Depends(get_db)):
    if db.query(models.Voter).filter(models.Voter.voter_id == voter.voter_id).first():
        raise HTTPException(status_code=400, detail="Voter ID already registered")
    new_voter = models.Voter(**voter.dict(), has_voted=False)
    db.add(new_voter)
    db.commit()
    db.refresh(new_voter)
    return {"message": "Voter registered successfully"}

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

@app.get("/results")
def get_results(db: Session = Depends(get_db)):
    results = db.query(models.Voter.vote_choice).all()
    return {"total_votes": len(results)}