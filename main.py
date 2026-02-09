
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from project14_backend.database import SessionLocal, engine
from models import Base, ValentineAnswer, Trip, Goal

load_dotenv()

SHARED_PASSWORD = os.get("SHARED_PASSWORD")

app = FastAPI(title="project14 backend")

# Create tables
Base.metadata.create_all(bind=engine)


# -------- DB dependency --------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------- CORS --------
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later replace with Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------- Helper: password check --------
def check_password(pw: str):
    if not pw or pw != SHARED_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta ahh")


@app.get("/")
def root():
    return {"message": "Backend is live"}


@app.post("/valentine/answer")
async def save_answer(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    answer = body.get("answer")

    if not answer:
        raise HTTPException(status_code=400, detail="respuesta")

    db.add(ValentineAnswer(answer=answer))
    db.commit()

    return {"status": "saved"}


# -------- Trips --------
@app.get("/trips")
def get_trips(db: Session = Depends(get_db)):
    return db.query(Trip).order_by(Trip.created_at.desc()).all()


@app.post("/trips")
async def add_trip(
    request: Request,
    x_shared_password: str = Header(None),
    db: Session = Depends(get_db),
):
    check_password(x_shared_password)

    body = await request.json()

    trip = Trip(
        destination=body.get("destination"),
        description=body.get("description"),
        planned_year=body.get("planned_year"),
    )

    db.add(trip)
    db.commit()

    return {"status": "Viaje added"}


# -------- Goals --------
@app.get("/goals")
def get_goals(db: Session = Depends(get_db)):
    return db.query(Goal).order_by(Goal.created_at.desc()).all()


@app.post("/goals")
async def add_goal(
    request: Request,
    x_shared_password: str = Header(None),
    db: Session = Depends(get_db),
):
    check_password(x_shared_password)

    body = await request.json()

    goal = Goal(
        title=body.get("title"),
        description=body.get("description"),
        status=body.get("status", "planned"),
    )

    db.add(goal)
    db.commit()

    return {"status": "Goal added"}
