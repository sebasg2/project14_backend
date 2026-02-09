from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from database import SessionLocal, engine
from models import Base, ValentineAnswer, Trip, Goal, PasswordCheck
from schemas import (
    ValentineAnswerCreate,
    TripCreate,
    GoalCreate,
)

load_dotenv()
SHARED_PASSWORD = os.getenv("SHARED_PASSWORD")

if not SHARED_PASSWORD:
    raise RuntimeError("SHARED_PASSWORD not set")

app = FastAPI(
    title="project14 backend",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def check_password(pw: str):
    if pw != SHARED_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta, no eres ana paty")
    



@app.post("/auth/password")
def verify_password(payload: PasswordCheck):
    if payload.password != SHARED_PASSWORD:
        return {"success": False}

    return {"success": True}



@app.get("/valentine/status")
def valentine_status(db: Session = Depends(get_db)):
    yes_exists = (
        db.query(ValentineAnswer)
        .filter(ValentineAnswer.answer == True)
        .first()
        is not None
    )

    return {"answeredYes": yes_exists}

@app.post("/valentine/yes")
def save_yes(db: Session = Depends(get_db)):
    db.add(ValentineAnswer(answer=True))
    db.commit()
    return {"status": "saved"}


@app.get("/")
def root():
    return {"message": "Backend is live"}


@app.post("/valentine/answer")
def save_answer(
    payload: ValentineAnswerCreate,
    db: Session = Depends(get_db),
):
    db.add(ValentineAnswer(answer=payload.answer))
    db.commit()
    return {"status": "saved"}


@app.get("/trips")
def get_trips(db: Session = Depends(get_db)):
    return db.query(Trip).order_by(Trip.created_at.desc()).all()

@app.post("/trips")
def add_trip(
    trip: TripCreate,
    x_shared_password: str = Header(...),
    db: Session = Depends(get_db),
):
    check_password(x_shared_password)

    new_trip = Trip(
        destination=trip.destination,
        description=trip.description,
        planned_year=trip.planned_year,
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return new_trip


@app.get("/goals")
def get_goals(db: Session = Depends(get_db)):
    return db.query(Goal).order_by(Goal.created_at.desc()).all()



@app.post("/goals")
def add_goal(
    goal: GoalCreate,
    x_shared_password: str = Header(...),
    db: Session = Depends(get_db),
):
    check_password(x_shared_password)

    new_goal = Goal(
        title=goal.title,
        description=goal.description,
        status=goal.status,
    )

    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return new_goal


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,  # local only
    )