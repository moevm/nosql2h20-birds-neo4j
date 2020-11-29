# This script updates the images for compose
sudo docker-compose up --force-recreate --build -d
sudo docker image prune -f
# sudo docker system prune -a