# api on http://0.0.0.0:8183/
# https://fastapi.tiangolo.com/tutorial/bigger-applications/

from typing import List
from datetime import date
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .config import get_settings, Settings

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


@app.get("/groundwater/", response_model=List[schemas.Groundwater])
def read_meters(skip: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    meters = crud.get_groundwater(db, skip=skip, limit=limit)
    return meters


@app.get("/groundwater/{meter_no}", response_model=List[schemas.Groundwater])
def read_meter_groundwater(meter_no: str, skip: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    meter_groundwater = crud.get_meter_groundwater(db, meter_no=meter_no, skip=skip, limit=limit)
    
    if meter_groundwater is None:
        raise HTTPException(status_code=404, detail="Meter not found")
    return meter_groundwater


@app.get("/groundwater/meter_no/{meter_no}/read_date/{read_date}", response_model=schemas.Groundwater)
def read_meter_date_groundwater(meter_no: str, read_date: date, db: Session = Depends(get_db)):
    meter_groundwater = crud.get_meter_date_groundwater(db, meter_no=meter_no, read_date=read_date)
    
    if meter_groundwater is None:
        raise HTTPException(status_code=404, detail="Meter not found")
    return meter_groundwater


@app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing
    }    