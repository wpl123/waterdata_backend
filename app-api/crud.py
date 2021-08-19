from sqlalchemy.orm import Session

from . import models, schemas

def get_meters(db: Session, skip: int = 1, limit: int = 100):
    return db.query(models.Meter).offset(skip).limit(limit).all()

def get_meter(db: Session, meter_no: str): 
    return db.query(models.Meter).filter(models.Meter.meter_no == meter_no).first()