from pydantic import BaseModel
from typing import Optional


class ValentineAnswerCreate(BaseModel):
    answer: str


class TripCreate(BaseModel):
    destination: str
    description: Optional[str] = None
    planned_year: Optional[int] = None


class GoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "planned"
