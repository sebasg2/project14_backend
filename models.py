from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class ValentineAnswer(Base):
    __tablename__ = "valentine_answer"

    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String, nullable=False)
    description = Column(String, nullable=False)
    planned_year = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, default="planned")  # planned | in_progress | achieved
    created_at = Column(DateTime, default=datetime.utcnow)
