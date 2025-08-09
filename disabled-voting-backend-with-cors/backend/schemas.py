from pydantic import BaseModel

class VoterCreate(BaseModel):
    voter_id: str
    name: str
    phone: str

class VoteCreate(BaseModel):
    voter_id: str
    choice: str