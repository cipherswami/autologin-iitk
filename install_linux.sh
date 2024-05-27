#!/bin/bash

##############################################################
# Author        : Aravind Potluri <aravindswami135@gmail.com>
# Description   : Installation script for autologin-iitk.
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
    echo "[!] This script must be run as sudo" 1>&2
    echo ""
    exit 1
fi

# Display banner
banner

echo ""

# Copy the Python script to /usr/local/bin and make it executable
echo "[+] Copying $SCRIPT_NAME to $SCRIPT_PATH"
cp "$SCRIPT_NAME" "$SCRIPT_PATH"
chmod +x "$SCRIPT_PATH"

echo ""

# Create the systemd service file
echo "[+] Creating systemd service file at $SERVICE_PATH"
cat <<EOL > "$SERVICE_PATH"
[Unit]
After=network.target

[Service]
ExecStart=$PYTHON_PATH $SCRIPT_PATH
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOL

echo ""

# Reload systemd, enable and start the service
echo "[+] Reloading systemd daemon"
systemctl daemon-reload

echo ""

echo "[+] Enabling the $SERVICE_NAME, to run at boot"
systemctl enable "$SERVICE_NAME"

echo ""

echo "[+] Starting the $SERVICE_NAME"
systemctl start "$SERVICE_NAME"

echo ""

# Check the status of the service
echo "[#] Installation done :)"

echo ""
echo "[#] Check the status using:"
echo "$ systemctl status ${SERVICE_NAME::-8}"
echo ""
