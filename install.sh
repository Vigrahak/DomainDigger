#!/bin/bash

# Check if python3-pip is already installed
echo "Checking if python3-pip is already installed..."
if [ -x "$(command -v pip3)" ]; then
  echo "python3-pip is already installed. Updating..."
  sudo apt-get update
  sudo apt-get install --only-upgrade -y python3-pip
else
  echo "python3-pip is not installed. Installing..."
  sudo apt-get install -y python3-pip
fi

# Check if python3-requests is already installed
echo "Checking if python3-requests is already installed..."
if [ -x "$(command -v python3-requests)" ]; then
  echo "python3-requests is already installed. Updating..."
  sudo apt-get update
  sudo apt-get install --only-upgrade -y python3-requests
else
  echo "python3-requests is not installed. Installing..."
  sudo apt-get install -y python3-requests
fi

# Check if python3-bs4 is already installed
echo "Checking if python3-bs4 is already installed..."
if [ -x "$(command -v python3-bs4)" ]; then
  echo "python3-bs4 is already installed. Updating..."
  sudo apt-get update
  sudo apt-get install --only-upgrade -y python3-bs4
else
  echo "python3-bs4 is not installed. Installing..."
  sudo apt-get install -y python3-bs4
fi

# Check if python3-urllib3 is already installed
echo "Checking if python3-urllib3 is already installed..."
if [ -x "$(command -v python3-urllib3)" ]; then
  echo "python3-urllib3 is already installed. Updating..."
  sudo apt-get update
  sudo apt-get install --only-upgrade -y python3-urllib3
else
  echo "python3-urllib3 is not installed. Installing..."
  sudo apt-get install -y python3-urllib3
fi

# Check if python3-selenium is already installed
echo "Checking if python3-selenium is already installed..."
if [ -x "$(command -v python3-selenium)" ]; then
  echo "python3-selenium is already installed. Updating..."
  sudo apt-get update
  sudo apt-get install --only-upgrade -y python3-selenium
else
  echo "python3-selenium is not installed. Installing..."
  sudo apt-get install -y python3-selenium
fi

# Install required Python packages
echo "Installing required Python packages..."
pip3 install --upgrade -y requests beautifulsoup4 urllib3 selenium webdriver-manager

# Check if requests is already installed
echo "Checking if requests is already installed..."
if [ -x "$(pip3 show requests)" ]; then
  echo "requests is already installed. Updating..."
  pip3 install --upgrade -y requests
else
  echo "requests is not installed. Installing..."
  pip3 install -y requests
fi

# Check if beautifulsoup4 is already installed
echo "Checking if beautifulsoup4 is already installed..."
if [ -x "$(pip3 show beautifulsoup4)" ]; then
  echo "beautifulsoup4 is already installed. Updating..."
  pip3 install --upgrade -y beautifulsoup4
else
  echo "beautifulsoup4 is not installed. Installing..."
  pip3 install -y beautifulsoup4
fi

# Check if urllib3 is already installed
echo "Checking if urllib3 is already installed..."
if [ -x "$(pip3 show urllib3)" ]; then
  echo "urllib3 is already installed. Updating..."
  pip3 install --upgrade -y urllib3
else
  echo "urllib3 is not installed. Installing..."
  pip3 install -y urllib3
fi

# Check if selenium is already installed
echo "Checking if selenium is already installed..."
if [ -x "$(pip3 show selenium)" ]; then
  echo "selenium is already installed. Updating..."
  pip3 install --upgrade -y selenium
else
  echo "selenium is not installed. Installing..."
  pip3 install -y selenium
fi

# Check if webdriver-manager is already installed
echo "Checking if webdriver-manager is already installed..."
if [ -x "$(pip3 show webdriver-manager)" ]; then
  echo "webdriver-manager is already installed. Updating..."
  pip3 install --upgrade -y webdriver-manager
else
  echo "webdriver-manager is not installed. Installing..."
  pip3 install -y webdriver-manager
fi

# Run the DomainDigger script
echo "Running the DomainDigger script..."
python3 domaindigger.py
