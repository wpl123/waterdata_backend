# api on http://0.0.0.0:8183/
# https://fastapi.tiangolo.com/tutorial/bigger-applications/

#from typing import List
#from datetime import date
from fastapi import APIRouter, Depends, HTTPException
#from sqlalchemy.orm import Session

#from . import crud, models, schemas
#from ..dependencies import get_token_header, get_db
#from ..database import SessionLocal, engine
from ..config import get_settings, Settings

#models.Base.metadata.create_all(bind=engine)


router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World 2.0"}


@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing
    }    