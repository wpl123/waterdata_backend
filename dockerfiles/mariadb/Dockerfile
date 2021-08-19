# https://github.com/lindycoder/prepopulated-mysql-container-example

#FROM mariadb:latest as builder
FROM mariadb:latest

LABEL version="1.1"
LABEL vendor="Progress Programming Solutions P/L"
LABEL maintainer="Phil Laird <wplaird@bigpond.com>"
LABEL release-date="2021.08.18"
LABEL version.is-production=""

ENV MYSQL_ROOT_PASSWORD=water
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=water
ENV MYSQL_DATABASE=waterdata

RUN apt-get update && apt-get install -y vim cron

#add cronfiles

# Crontab file copied to cron.d directory.
COPY ./cronfiles/cronjob /etc/cron.d/container_cronjob

# Script file copied into container.
COPY ./cronfiles/run_load_waterdata.sh /run_load_waterdata.sh

# Give executable permission to script file.
RUN chmod +x /run_load_waterdata.sh

# Running commands for the startup of a container.
# CMD ["sh", “-c”, “/run_load_waterdata.sh && chmod 644 /etc/cron.d/container_cronjob && cron && tail -f /var/log/cron.log”]
RUN chmod 0644 /etc/cron.d/container_cronjob && \
    crontab /etc/cron.d/container_cronjob

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
# CMD cron && tail -f /var/log/cron.log    #TODO: Hashed out. Causes container to fail to start. Running cron on the server

COPY my.cnf /etc/mysql/

