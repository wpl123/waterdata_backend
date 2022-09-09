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

