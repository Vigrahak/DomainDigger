#!/bin/bash

# Install required packages using apt
sudo apt update
sudo apt install --upgrade -y python3-pip
sudo apt install --upgrade -y python3-requests
sudo apt install --upgrade -y python3-bs4
sudo apt install --upgrade -y python3-urllib3
sudo apt install --upgrade -y python3-selenium

# Upgrade existing packages using apt
apt upgrade -y

# Install Python packages using pip3
pip3 install -r requirements.txt
