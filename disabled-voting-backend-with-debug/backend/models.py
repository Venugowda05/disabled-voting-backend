from sqlalchemy import Column, String, Boolean
from backend.database import Base

class Voter(Base):
    __tablename__ = "voters"
    voter_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    has_voted = Column(Boolean, default=False)
    vote_choice = Column(String, nullable=True)