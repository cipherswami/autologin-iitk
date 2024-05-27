#!/bin/bash

##############################################################
# Author        : Aravind Potluri <aravindswami135@gmail.com>
# Description   : Uninstallation script for autologin-iitk.
# Distrubuiton  : All systemd enabled linux OS.
##############################################################

# Function to display banner
function banner {
    clear
    echo "##############################################################"
    echo "#------------------------------------------------------------#"
    echo "                     autologin-iitk                           "
    echo "#------------------------------------------------------------#"
    echo "################## Author: cipherswami #######################"
}

# Variables
SCRIPT_NAME="autologin-iitk.py"
SCRIPT_PATH="/usr/local/bin/$SCRIPT_NAME"
PYTHON_PATH=$(which python3)
SERVICE_NAME="${SCRIPT_NAME::-3}.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo ""
    echo "[!] This script must be run as root" 1>&2
    echo ""
    exit 1
fi

# Display banner
banner

# Stop and disable the systemd service
echo ""
echo "[-] Stopping the $SERVICE_NAME"
systemctl stop "$SERVICE_NAME"

echo ""

echo "[-] Disabling the $SERVICE_NAME"
systemctl disable "$SERVICE_NAME"

echo ""

# Remove the systemd service file
if [ -f "$SERVICE_PATH" ]; then
    echo "[-] Removing systemd service file at $SERVICE_PATH"
    rm "$SERVICE_PATH"
else
    echo "[!] Service file $SERVICE_PATH does not exist"
fi

echo ""

# Reload systemd daemon
echo "[+] Reloading systemd daemon"
systemctl daemon-reload

echo ""

# Remove the Python script from /usr/local/bin
if [ -f "$SCRIPT_PATH" ]; then
    echo "[-] Removing script at $SCRIPT_PATH"
    rm "$SCRIPT_PATH"
else
    echo "[!] Script file $SCRIPT_PATH does not exist"
fi

echo ""

echo "[#] Uninstallation complete"
echo ""
