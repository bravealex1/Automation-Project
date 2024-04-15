#!/bin/bash

# Install ChromeDriver
# First, define the target directory where ChromeDriver will be downloaded and extracted
TARGET_DIR="/mnt/c/Users/Owner/Downloads/chromedriver-linux64"

# Create target directory if it doesn't exist
mkdir -p $TARGET_DIR

# # Download ChromeDriver zip file into the target directory
wget -N https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/linux64/chromedriver-linux64.zip -P $TARGET_DIR

# Navigate to the target directory
cd $TARGET_DIR

# Unzip the ChromeDriver in the target directory
unzip -o chromedriver-linux64.zip

# Move the ChromeDriver binary to a system-wide location in /usr/local/bin
# Check for the nested directory structure and adjust accordingly
if [ -f "$TARGET_DIR/chromedriver-linux64/chromedriver" ]; then
    # Moving from nested directory structure
    sudo mv $TARGET_DIR/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
else
    # Directly move if not nested
    sudo mv $TARGET_DIR/chromedriver /usr/local/bin/chromedriver
fi

# Set the owner and permissions to ensure it is executable
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod 0755 /usr/local/bin/chromedriver

# Clean up: Remove the downloaded zip and any extracted directories
rm -rf $TARGET_DIR/chromedriver-linux64.zip
rm -rf $TARGET_DIR/chromedriver-linux64

# Print success message
echo "ChromeDriver installation is complete."