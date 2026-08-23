from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(100))
    resume_filename = Column(String(255), nullable=False)
    resume_text = Column(Text, nullable=False)
    skills = Column(Text, default="[]")
    education = Column(Text, default="[]")
    experience = Column(Text, default="[]")
    projects = Column(Text, default="[]")
    certifications = Column(Text, default="[]")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), default="Untitled Job")
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    score = Column(Float, nullable=False)
    strengths = Column(Text, default="[]")
    skill_gaps = Column(Text, default="[]")
    justification = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
