from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from app.config import get_settings, Settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/meters/", response_model=List[schemas.Meter])
def read_meters(skip: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    meters = crud.get_meters(db, skip=skip, limit=limit)
    return meters


@app.get("/meters/{meter_no}", response_model=schemas.Meter)
def read_meter(meter_no: str, db: Session = Depends(get_db)):
    db_meter = crud.get_meter(db, meter_no=meter_no)
    
    if db_meter is None:
        raise HTTPException(status_code=404, detail="Meter not found")
    return db_meter

@app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing
    }    