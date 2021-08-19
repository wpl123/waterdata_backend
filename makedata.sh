:
function create_csv() {

  BACKDIR=/home/admin/dockers/waterdata_backend/data/waterdata
  FRONTDIR=/home/admin/dockers/waterdata_frontend/work/training_data
  echo 'Setting python interpreter'
  source /home/admin/dockers/waterdata_backend/venv/bin/activate
  echo 'Downloading latest waterdata'
  /home/admin/dockers/waterdata_backend/venv/bin/python /home/admin/dockers/waterdata_backend/app/wrapper_download.py
  echo 'Uploading latest waterdata to the database'
  /home/admin/dockers/waterdata_backend/venv/bin/python /home/admin/dockers/waterdata_backend/app/wrapper_upload.py
  echo 'Recreating all_training_data.csv in current directory'
  /home/admin/dockers/waterdata_backend/venv/bin/python /home/admin/dockers/waterdata_backend/app/create_csv.py
  echo 'Moving all_training_data.csv to the frontend directory $FRONTDIR ..\c'
  mv $BACKDIR/all_training_data.csv $FRONTDIR
  echo 'done'

  exit
}

while true; do
    read -p "Do you wish to create the waterdata csv file with the latest data?" yn
    case $yn in
        [Yy]* ) create_csv;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

