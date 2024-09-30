#!/bin/bash

# Install required packages using apt
sudo apt update
sudo apt install -y python3-pip
sudo apt install -y python3-beautifulsoup4
sudo apt install -y python3-requests
sudo apt install -y python3-selenium
sudo apt install -y python3-webdriver-manager
sudo apt install -y python3-urllib3

# Upgrade existing packages using apt
apt upgrade -y

# Install Python packages using pip3
pip3 install --upgrade -r requirements.txt
