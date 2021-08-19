:
function backupdb() {

  echo 'Backing up waterdata directory'
  docker-compose stop
  cd ..
  sudo tar cvzf waterdata.tar.gz --exclude './waterdata_frontend/venv' --exclude './waterdata_backend/venv' ./waterdata_backend ./waterdata_frontend
  scp waterdata.tar.gz root@192.168.11.10:/mnt/Storage/Phil/backups
  cd waterdata_backend
  docker-compose up -d
  exit
}

while true; do
    read -p "Do you wish to backup the waterdata directory?" yn
    case $yn in
        [Yy]* ) backupdb;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

