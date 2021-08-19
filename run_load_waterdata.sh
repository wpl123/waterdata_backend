#!/bin/bash
#script to download and update the realdata from Water NSW and the BOM to the waterdata Mysql DB
#18.8.2021

DOWNLOADDIR=/home/admin/dockers/waterdata_backend/data/downloads/cronlog
UPLOADDIR=/home/admin/dockers/waterdata_backend/data/uploads/cronlog

# https://stackoverflow.com/questions/3287038/cron-and-virtualenv
#SHELL=/bin/bash
#*/10 * * * * root source /path/to/virtualenv/bin/activate && /path/to/build/manage.py some_command > /dev/null


source /home/admin/dockers/waterdata_backend/venv/bin/activate && /home/admin/dockers/waterdata_backend/venv/bin/python /home/admin/dockers/waterdata_backend/app/wrapper_download.py >> $DOWNLOADDIR/download_error.log 2>&1
source /home/admin/dockers/waterdata_backend/venv/bin/activate && /home/admin/dockers/waterdata_backend/venv/bin/python /home/admin/dockers/waterdata_backend/app/wrapper_upload.py >> $UPLOADDIR/upload_error.log 2>&1


