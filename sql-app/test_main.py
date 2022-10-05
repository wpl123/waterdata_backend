# api on http://0.0.0.0:8183/
# https://fastapi.tiangolo.com/tutorial/testing
# To debug, Look in the docker container logs for the errors

import sys, os

from typing import List
from datetime import date
from fastapi import FastAPI  #TODO - package issues  https://stackoverflow.com/questions/60593604/importerror-attempted-relative-import-with-no-known-parent-package#60594917
from fastapi.testclient import TestClient

#sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])
print(sys.path)

if __name__ == '__main__' and __package__ is None:
    from .config import get_settings, Settings
    from .dependencies import get_db
    from .internal import admin
    from .routers import meters, groundwater
    from .main import app
else:
    from config import get_settings, Settings
    from dependencies import get_db
    from internal import admin
    from routers import meters, groundwater
    from main import app


#app = FastAPI(dependencies=[Depends(get_query_token)])
#app = FastAPI()

#app.include_router(meters.router)
#app.include_router(groundwater.router)
#app.include_router(admin.router)
#    admin.router,
#    prefix="/admin",
#    tags=["admin"],
#    dependencies=[Depends(get_settings)],
#    responses={418: {"description": "I'm a teapot"}},
#)

# dependencies=[Depends(get_token_header,get_settings)],

client = TestClient(app)

def test_read_meter():
    response = client.get("/meters/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }


def test_read_meter_bad_token():
    response = client.get("/meters/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent_meter():
    response = client.get("/meters/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "meter not found"}


def test_create_meter():
    response = client.post(
        "/meters/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_create_meter_bad_token():
    response = client.post(
        "/meters/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_meter():
    response = client.post(
        "/meters/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "meter already exists"}