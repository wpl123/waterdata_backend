from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

if __name__ == '__main__' and __package__ is None:
    from ...database import Base
else:
    from database import Base

class Meter(Base):
    __tablename__ = "meters"

    id = Column(Integer, primary_key=True, index=True)
    meter_no   = Column(String, unique=True, index=True)
    meter_name = Column(String)
    meter_type = Column(Integer)
    meter_lat  = Column(Float)
    meter_lon  = Column(Float)
    meter_elev = Column(Float)
    meter_screen_depth = Column(Float)
    comments   = Column(String)
    get_data   = Column(Float)    # TODO: should be int
    download_url = Column(String)
    params     = Column(String)
    last_download = Column(Date)
    creation_date = Column(Date)
    
    groundwater = relationship("Groundwater", back_populates="meter_no")
    
    
    class Config:
        orm_mode = True

