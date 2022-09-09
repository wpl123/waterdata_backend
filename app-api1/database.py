from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:water@192.168.11.6:30000/waterdata"
#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://" + app.dbconfig.user + \
#    ':' + app.dbconfig.psw + '@' + app.dbconfig.host + ':' + app.dbconfig.port +\
#    '/' + app.dbconfig.db_name

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()