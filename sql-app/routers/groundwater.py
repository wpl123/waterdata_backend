# api on http://0.0.0.0:8183/
# https://fastapi.tiangolo.com/tutorial/bigger-applications/

from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dbmodels.groundwater import crud, models, schemas
from ..dependencies import get_db
#from dependencies import get_token_header, get_db
from ..database import SessionLocal, engine

router = APIRouter()


@router.get("/groundwater/", response_model=List[schemas.Groundwater])
def read_meters(skip: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    meters = crud.get_groundwater(db, skip=skip, limit=limit)
    return meters


@router.get("/groundwater/{meter_no}", response_model=List[schemas.Groundwater])
def read_meter_groundwater(meter_no: str, skip: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    meter_groundwater = crud.get_meter_groundwater(db, meter_no=meter_no, skip=skip, limit=limit)
    
    if meter_groundwater is None:
        raise HTTPException(status_code=404, detail="Groundwater for meter " + meter_no + " not found")
    return meter_groundwater


@router.get("/groundwater/meter_no/{meter_no}/read_date/{read_date}", response_model=schemas.Groundwater)
def read_meter_date_groundwater(meter_no: str, read_date: date, db: Session = Depends(get_db)):
    meter_groundwater = crud.get_meter_date_groundwater(db, meter_no=meter_no, read_date=read_date)
    
    if meter_groundwater is None:
        raise HTTPException(status_code=404, detail="Groundwater record not found")
    return meter_groundwater
   