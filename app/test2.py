import datetime
from datetime import timedelta
from flutils import *

download_dir = "/home/admin/dockers/waterdata_backend/data/downloads/"
logs_dir = "/home/admin/dockers/waterdata_backend/data/downloads/logs/"
logfile = logs_dir + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + ".log"


del_files(logs_dir + '/screenshots/', '*.png')