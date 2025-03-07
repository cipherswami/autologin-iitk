#!/bin/bash

##############################################################
# Author        : Aravind Potluri <aravindswami135@gmail.com>
# Description   : Uninstallation script for autologin-iitk.
# Distribution  : All systemd enabled Linux OS.
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

echo ""

# Stop the systemd service
echo "[-] Stopping the $SERVICE_NAME"
if systemctl stop "$SERVICE_NAME"; then
    rm -rf /var/tmp/iitk_logout_url.txt
    echo "[+] Successfully stopped $SERVICE_NAME"
else
    echo "[!] Failed to stop $SERVICE_NAME or it may not be running" 1>&2
    exit 1
fi

echo ""

# Disable the systemd service
echo "[-] Disabling the $SERVICE_NAME"
if systemctl disable "$SERVICE_NAME"; then
    echo "[+] Successfully disabled $SERVICE_NAME"
else
    echo "[!] Failed to disable $SERVICE_NAME" 1>&2
    exit 1
fi

echo ""

# Remove the systemd service file
if [ -f "$SERVICE_PATH" ]; then
    echo "[-] Removing systemd service file at $SERVICE_PATH"
    if rm "$SERVICE_PATH"; then
        echo "[+] Successfully removed $SERVICE_PATH"
    else
        echo "[!] Failed to remove $SERVICE_PATH" 1>&2
        exit 1
    fi
else
    echo "[!] Service file $SERVICE_PATH does not exist"
fi

echo ""

# Reload systemd daemon
echo "[+] Reloading systemd daemon"
if systemctl daemon-reload; then
    echo "[+] Successfully reloaded systemd daemon"
else
    echo "[!] Failed to reload systemd daemon" 1>&2
fi

echo ""

# Remove the Python script from /usr/local/bin
if [ -f "$SCRIPT_PATH" ]; then
    echo "[-] Removing script at $SCRIPT_PATH"
    if rm "$SCRIPT_PATH"; then
        echo "[+] Successfully removed $SCRIPT_PATH"
    else
        echo "[!] Failed to remove $SCRIPT_PATH" 1>&2
        exit 1
    fi
else
    echo "[!] Script file $SCRIPT_PATH does not exist"
fi

echo ""

echo "[#] Uninstallation complete"
echo ""
