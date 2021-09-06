
/home/admin/dockers/waterdata_backend/venv/bin/python -m smtpd -c DebuggingServer -n localhost:1025 >> /home/admin/dockers/waterdata_backend/data/downloads/cronlog/download_error.log 2>&1 &

#cat /home/admin/dockers/waterdata_backend/data/downloads/cronlog/download_error.log >> /home/admin/dockers/waterdata_backend/data/downloads/cronlog/test.log & 
PID=$!
echo $PID
kill -9 $PID