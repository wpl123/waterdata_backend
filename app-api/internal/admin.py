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


@router.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
            "title": "PPS Waterdata API",
            "description": "This is a API that provides select weather and water data.",
            "termsOfService": "http://192.168.11.6:8183/terms/",
            "contact": {
              "name": "API Support",
              "url": "http://www.example.com/support",
              "email": "support@example.com"
            },
            "license": {
              "name": "GNU Affero General Public License",
              "url": "https://www.gnu.org/licenses/agpl-3.0.en.html"
            },
            "version": "1.0.1"
    }
    
@router.get("/terms")
async def terms(settings: Settings = Depends(get_settings)):
    return {
            "title": "PPS Waterdata API Terms and Conditions",
            "description": "These are the PPS Waterdata API Terms and Conditions.",
            "version": "1.0.0"
    }                       