#!/bin/bash

# Start the run once job.
echo "Docker container has been started"

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

# Setup a cron schedule
echo "SHELL=/bin/bash
BASH_ENV=/container.env


# Setup a cron schedule
echo "43 15 * * * root /home/admin/dockers/waterdata-backend/cronfiles/run.sh >> /var/log/cron.log 2>&1"
# This extra line makes it a valid cron" > /home/admin/dockers/waterdata-backend/cronfiles/scheduler.txt

crontab /home/admin/dockers/waterdata-backend/cronfiles/scheduler.txt
cron -f
