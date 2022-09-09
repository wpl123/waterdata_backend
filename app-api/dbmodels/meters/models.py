from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from ...database import Base


class Meter(Base):
    __tablename__ = "meters"

    id = Column(Integer, primary_key=True, index=True)
    meter_no = Column(String, index=True)
    meter_name = Column(String)
    meter_type = Column(Integer)

    class Config:
        orm_mode = True

