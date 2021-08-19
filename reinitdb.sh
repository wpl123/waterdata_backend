:

function reinitdb() {

# echo 'Inside reinitdb'
  docker-compose stop
  docker-compose rm -f
  docker images
  TEST=`docker images | grep waterdata | cut -c 52-63`
  docker image rm -f $TEST
  echo 'removing database subdirectory'
  sudo rm -r database
  docker-compose up -d
  exit
}

while true; do
    read -p "Do you wish to re-initialise the waterdata database?" yn
    case $yn in
        [Yy]* ) reinitdb;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

