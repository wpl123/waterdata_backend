# api on http://0.0.0.0:8183/
# https://fastapi.tiangolo.com/tutorial/bigger-applications/

from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dbmodels.meters import crud, models, schemas
from ..dependencies import get_db
from ..database import SessionLocal, engine
    
models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/meters/", response_model=List[schemas.Meter])
async def read_meters(skip: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    meters = crud.get_meters(db, skip=skip, limit=limit)
    return meters


@router.get("/meters/{meter_no}", response_model=schemas.Meter)
def read_meter(meter_no: str, db: Session = Depends(get_db)):
    db_meter = crud.get_meter(db, meter_no=meter_no)
    
    if db_meter is None:
        raise HTTPException(status_code=404, detail="Meter not found")
    return db_meter
   

@router.post("/meters/", response_model=schemas.Meter)
def create_meter(meter: schemas.MeterCreate, db: Session = Depends(get_db)):
    db_meter = crud.get_meter(db, meter=meter.meter_no)
    if db_meter:
        raise HTTPException(status_code=400, detail="Meter No already registered")
    return crud.create_meter(db=db, meter_no=meter.meter_no)