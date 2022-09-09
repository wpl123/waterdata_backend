from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base


class Meter(Base):
    __tablename__ = "meters"

    id = Column(Integer, primary_key=True, index=True)
    meter_no = Column(String, index=True)
    meter_name = Column(String)
    meter_type = Column(Integer)

    class Config:
        orm_mode = True

class Groundwater(Base):
    __tablename__ = "groundwater"

    id = Column(Integer, primary_key=True, index=True)
    meter_no = Column(String, index=True)
    read_date = Column(Date, index=True)
    bl_bmp = Column(Float)
    ql_bmp = Column(String)
    bl_ahd = Column(Float)
    ql_ahd = Column(String)
    mean_temp = Column(Float)
    ql_temp = Column(String)
    comments = Column(String)
    creation_date = Column(Date)

    class Config:
        orm_mode = True