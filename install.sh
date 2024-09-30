#!/bin/bash

# Uninstall all packages
echo "Uninstalling all packages..."
pip3 uninstall -y requests beautifulsoup4 urllib3 selenium webdriver-manager
sudo apt-get remove -y python3-pip python3-requests python3-bs4 python3-urllib3 python3-selenium chromium chromium-common chromium-sandbox chromium-driver

# Install required packages
echo "Installing required packages..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-requests python3-bs4 python3-urllib3 python3-selenium chromium chromium-common chromium-sandbox chromium-driver

# Install required Python packages
echo "Installing required Python packages..."
pip3 install requests beautifulsoup4 urllib3 selenium webdriver-manager

# Run the DomainDigger script
echo "Running the DomainDigger script..."
python3 domaindigger.py
