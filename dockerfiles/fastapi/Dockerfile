# https://fastapi.tiangolo.com/deployment/docker/
# cd dockers/waterdata_backend; docker build -t waterdata_fastapi ./dockerfiles/fastapi

FROM tiangolo/uvicorn-gunicorn-fastapi:latest

# install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt