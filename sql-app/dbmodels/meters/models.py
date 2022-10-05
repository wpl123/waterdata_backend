from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from ...database import Base

class Meter(Base):
    __tablename__ = "meters"

    id = Column(Integer, primary_key=True, index=True)
    meter_no   = Column(String, ForeignKey("groundwater.meter_no"), unique=True, index=True)
    meter_name = Column(String)
    meter_type = Column(Integer)
    meter_lat  = Column(Float)
    meter_long  = Column(Float)
    meter_elev = Column(Float)
    meter_screen_depth = Column(Float)
    comments   = Column(String)
    get_data   = Column(Integer) 
    download_url = Column(String)
    params     = Column(String)
    last_download = Column(Date)
    creation_date = Column(Date)
    
    #groundwater = relationship("Groundwater", back_populates="owner")
    
    
    class Config:
        orm_mode = True

