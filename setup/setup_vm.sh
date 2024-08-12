#!/bin/bash

# Run using the below command
# bash setup_vm.sh

echo "Downloading anaconda..."
mkdir -p ../soft && cd ~/soft && \
wget https://repo.anaconda.com/archive/Anaconda3-2023.07-1-Linux-x86_64.sh

echo "Running anaconda script..."
bash ~/soft/Anaconda3-2023.07-1-Linux-x86_64.sh

echo "Removing anaconda script..."
rm ~/soft/Anaconda3-2023.07-1-Linux-x86_64.sh

echo "Running sudo apt-get update..."
sudo apt-get update

echo "Installing Docker..."
sudo apt-get -y install docker.io

echo "Docker without sudo setup..."
sudo groupadd docker
sudo gpasswd -a ${USER} docker
sudo service docker restart

echo "Installing docker-compose..."
cd ~/soft && wget https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-linux-x86_64 -O docker-compose && \
sudo chmod +x docker-compose

echo "Setup .bashrc..."
echo '' >> ~/.bashrc
echo 'export PATH=${HOME}/soft:${PATH}' >> ~/.bashrc
eval "$(cat ~/.bashrc | tail -n +10)"

echo "docker-compose version..."
docker-compose --version

echo "Installing AWS CLI..."
sudo apt install unzip
cd ~/soft && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && sudo ./aws/install

echo "aws cli version..."
aws --version

echo "Installing Terraform..."
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

echo "Installing necessary packages..."

pip install pipenv nltk mlflow prefect boto3 evidently pyarrow psycopg psycopg_binary pytest isort black pylint deepdiff