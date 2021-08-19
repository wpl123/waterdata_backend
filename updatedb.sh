:

function updatedb() {

# echo 'Inside updatedb'
  mysql -u root -p -h 192.168.11.6 -P 30000 < mariadb/initialize-database.sql
  exit
}

while true; do
    read -p "Do you wish to update the waterdata database?" yn
    case $yn in
        [Yy]* ) updatedb;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

