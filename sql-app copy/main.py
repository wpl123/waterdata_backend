# api on http://0.0.0.0:8183/
# https://fastapi.tiangolo.com/tutorial/bigger-applications/
# To debug, Look in the docker container logs for the errors

from typing import List, Union
from datetime import date
from fastapi import Depends, FastAPI    #, HTTPException

if __name__ == '__main__' and __package__ is None:
    from config import get_settings, Settings
    #from .dependencies import get_query_token, get_token_header, get_db
    from dependencies import get_db
    from internal import admin
    from routers import meters, groundwater
else:
    from .config import get_settings, Settings
    #from dependencies import get_query_token, get_token_header, get_db
    from .dependencies import get_db
    from .internal import admin
    from .routers import meters, groundwater


#app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(meters.router)
app.include_router(groundwater.router)
app.include_router(admin.router)
#    admin.router,
#    prefix="/admin",
#    tags=["admin"],
#    dependencies=[Depends(get_settings)],
#    responses={418: {"description": "I'm a teapot"}},
#)

# dependencies=[Depends(get_token_header,get_settings)],
