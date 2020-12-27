sudo apt-get update
sudo apt-get -y install y-pip python-dev libffi-dev openssl-dev gcc libc-dev make

sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

