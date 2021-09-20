# build command: cd dockers/waterdata_backend; docker build -t waterdata_dash ./dockerfiles/dash


FROM python:3.8.12-buster

RUN apt-get update
RUN apt-get install nano

# install python dependencies
#RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app-dash/app
ENV PYTHONPATH="/app-dash/app"

#CMD ["gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:8050", "app:server"]