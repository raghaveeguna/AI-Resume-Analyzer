
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Keyword(BaseModel):
    type: str  # e.g., 'skill', 'tech', 'degree', 'rule_based', 'tfidf'
    value: str
    score: Optional[float] = None

class Resume(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    filename: str
    content_type: str
    raw_text: str
    processed_text: str
    extracted_keywords: List[Keyword] = []
    ner_entities: dict = {}
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    candidate_score: Optional[float] = None
    sector_suitability: Optional[str] = None

class JobDescription(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    title: str
    raw_text: str
    processed_text: str
    extracted_keywords: List[Keyword] = []
    ner_entities: dict = {}
    creation_date: datetime = Field(default_factory=datetime.utcnow)

class User(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    email: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
