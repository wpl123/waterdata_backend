# https://fastapi.tiangolo.com/deployment/docker/

FROM tiangolo/uvicorn-gunicorn-fastapi:latest

# install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt