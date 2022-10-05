from typing import List, Optional
from datetime import date
from pydantic import BaseModel


class MeterBase(BaseModel):
    id: int
    meter_no: str
    meter_name: Optional[str] = None
    meter_type: Optional[int] = None
    meter_lat: Optional[float] = None
    meter_long: Optional[float] = None
    meter_elev: Optional[float] = None
    meter_screen_depth: Optional[float] = None
    comments: Optional[str] = None
    get_data: Optional[int] = None    # TODO: should be int
    download_url: Optional[str] = None
    params: Optional[str] = None
    last_download: Optional[date] = None
    creation_date: Optional[date] = None


class MeterCreate(MeterBase):
    pass


class Meter(MeterBase):
    id: int
    meter_no: str

    class Config:
        orm_mode = True

