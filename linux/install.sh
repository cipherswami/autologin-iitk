#!/bin/bash

##############################################################
# Author        : Aravind Potluri <aravindswami135@gmail.com>
# Description   : Installation script for autologin-iitk.
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
SCRIPT_LOCATION="src"
SCRIPT_PATH="/usr/local/bin/$SCRIPT_NAME"
PYTHON_PATH=python3
SERVICE_NAME="${SCRIPT_NAME::-3}.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo ""
    echo "[!] This script must be run as sudo" 1>&2
    echo ""
    exit 1
fi

# Check if Python3 is installed
if [ -z "$PYTHON_PATH" ]; then
    echo ""
    echo "[!] Python3 is not installed. Please install it and try again." 1>&2
    echo ""
    exit 1
fi

# Display banner
banner

echo ""

# Copy the Python script to /usr/local/bin and make it executable
echo "[+] Copying $SCRIPT_NAME to $SCRIPT_PATH"
if cp "$SCRIPT_LOCATION/$SCRIPT_NAME" "$SCRIPT_PATH"; then
    echo "[+] Successfully copied $SCRIPT_NAME"
else
    echo "[!] Failed to copy $SCRIPT_NAME" 1>&2
    exit 1
fi

if chmod +x "$SCRIPT_PATH"; then
    echo "[+] Made $SCRIPT_PATH executable"
else
    echo "[!] Failed to make $SCRIPT_PATH executable" 1>&2
    exit 1
fi

echo ""

# Create the systemd service file
echo "[+] Creating systemd service file at $SERVICE_PATH"
if cat <<EOL > "$SERVICE_PATH"
[Unit]
After=network.target

[Service]
ExecStart=$PYTHON_PATH $SCRIPT_PATH
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOL
then
    echo "[+] Successfully created $SERVICE_PATH"
else
    echo "[!] Failed to create $SERVICE_PATH" 1>&2
    exit 1
fi

echo ""

# Reload systemd, enable and start the service
echo "[+] Reloading systemd daemon"
if systemctl daemon-reload; then
    echo "[+] Successfully reloaded systemd daemon"
else
    echo "[!] Failed to reload systemd daemon" 1>&2
    exit 1
fi

echo ""

echo "[+] Enabling the $SERVICE_NAME, to run at boot"
if systemctl enable "$SERVICE_NAME"; then
    echo "[+] Successfully enabled $SERVICE_NAME"
else
    echo "[!] Failed to enable $SERVICE_NAME" 1>&2
    exit 1
fi

echo ""

echo "[+] Starting the $SERVICE_NAME"
if systemctl start "$SERVICE_NAME"; then
    echo "[+] Successfully started $SERVICE_NAME"
else
    echo "[!] Failed to start $SERVICE_NAME" 1>&2
    exit 1
fi

echo ""

# Check the status of the service
echo "[#] Installation done :)"

echo ""
echo "[#] Check the status using:"
echo "$ systemctl status ${SERVICE_NAME::-8}"
echo ""
