from typing import List, Optional
from datetime import date
from pydantic import BaseModel


class MeterBase(BaseModel):
    meter_no: str
    meter_name: Optional[str] = None


class MeterCreate(MeterBase):
    pass


class Meter(MeterBase):
    id: int
    meter_no: str

    class Config:
        orm_mode = True


class GroundwaterBase(BaseModel):
    meter_no: str
    read_date: Optional[date] = None
    bl_bmp: Optional[float] = None
    ql_bmp: Optional[str] = None
    bl_ahd: Optional[float] = None
    ql_ahd: Optional[str] = None
    mean_temp: Optional[float] = None
    ql_temp: Optional[str] = None
    comments: Optional[str] = None
    creation_date: Optional[date] = None

class GroundwaterCreate(GroundwaterBase):
    pass


class Groundwater(GroundwaterBase):
    id: int
    meter_no: str
    read_date: Optional[date] = None
    bl_bmp: Optional[float] = None
    ql_bmp: Optional[str] = None
    bl_ahd: Optional[float] = None
    ql_ahd: Optional[str] = None
    mean_temp: Optional[float] = None
    ql_temp: Optional[str] = None
    comments: Optional[str] = None
    creation_date: Optional[date] = None
    
    class Config:
        orm_mode = True