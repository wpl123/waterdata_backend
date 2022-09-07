from sqlalchemy.orm import Session
from datetime import date
from . import models, schemas

def get_meters(db: Session, skip: int = 1, limit: int = 100):
    return db.query(models.Meter).offset(skip).limit(limit).all()

def get_meter(db: Session, meter_no: str):
    return db.query(models.Meter).filter(models.Meter.meter_no == meter_no).first()

def get_groundwater(db: Session, skip: int = 1, limit: int = 100):
    return db.query(models.Groundwater).offset(skip).limit(limit).all()
    
    
def get_meter_groundwater(db: Session, meter_no: str, skip: int = 1, limit: int = 100): 
    return db.query(models.Groundwater).filter(models.Groundwater.meter_no == meter_no).offset(skip).limit(limit).all()

def get_meter_date_groundwater(db: Session, meter_no: str, read_date: date): 
    return db.query(models.Groundwater).filter(models.Groundwater.meter_no == meter_no).filter(models.Groundwater.read_date == read_date).first()