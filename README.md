# Autologin IITK :: CIPH3R

## Introduction

`autologin-iitk` is a Python script designed to automate the login process for IIT Kanpur's firewall authentication page. This script continuously checks for the firewall authentication portal, performs login, and keeps the session alive to maintain internet connectivity without manual intervention.

## Motive

- Servers and most of the computers in labs are connected via LAN and require login to the firewall authentication page at every boot. To automate this process, this script was made.

- We might need to connect exclusively to the '**iitk**' WiFi SSID in some cases, which again requires logging in to the firewall authentication page. Hence, `autologin-iitk`.

# Installation

### Pre Installation:

- Git clone the repository using below command (or) Download the latest ZIP file from [here](https://codeload.github.com/cipherswami/autologin-iitk/zip/refs/heads/main), and extract it:

    ```sh
    git clone https://github.com/cipherswami/autologin-iitk.git
    ```

- Now, go to the cloned or extracted repository and edit the `autologin-iitk.py` file in the **src** folder to add your username & password:

    ```python
    ####### User section #########################
    username = 'FILL USERNAME'
    password = 'FILL PASSWORD'
    # NOTE: Enter webmail password, not WiFi SSO
    #############################################
    ```

### Main Installation

- Please refer to the corresponding sections below for installation instructions:

  -  [Linux](#linux)
  -  [Windows](#windows)
  -  [MacOS](#macos)

## Linux 

### Installation

- Ensure **Python 3** is installed by verifying the version. If not, install it and then verify the version using below commands:
    ```sh
    python3 --version # To check the version of python
    ```
    ```sh
    sudo apt install python3  # To install for Debian-based systems
    ```

- Open a terminal in the root of the repository and install the script by running the following:
    ```sh
    chmod +x linux/install.sh && sudo ./linux/install.sh
    ```

- et voilà! installation is done. Now, you can safly delete the repository.
  
    ```sh
    cd .. && rm -rf autologin-iitk
    ```

- Please give this repo a star if you found it useful. 😁

- And check out [Additional info](#additional-info).
  
### Uninstallation

- Download or [clone](#pre-installation) the repository again. And open a terminal in the root of the repository. Then run the following to uninstall:

    ```sh
    chmod +x linux/uninstall.sh && sudo linux/uninstall.sh
    ```

## Windows 

### Installation

- Ensure **Python 3** is installed* by verifying the version. If not, install it from [python.org](https://www.python.org/downloads/), and don't forget to **check "Add Python to PATH"** during installation. And then, verify the version:  
  ```bash
  python --version
  ```

- Inside repository, navigate to the ***windows*** folder** to find the installation batch file.
  
- Now, right-click on the `install.bat` and run it as **Administrator**.

- If you encounter **Windows protected your PC** popup, click on `More info` and then choose `Run anyway` (or) If you see any **Unknown publisher** popup, simply choose `Run`.

  - NOTE: This is a simple installer script; there is no need to worry about any viruses. The entire code is open source, so you can review it if you wish.

- et voilà! installation is done. Now, you can safly delete the repository.

- Sometimes the service may exit unexpectedly. Then, you can restart/start it by opening `services.msc` (or) by running the following command:
    ```powershell
    # Open Powershell as Administrator
    Restart-Service -Name "autologin-iitk" -Force   # Restarting the service
    Start-Service -Name "autologin-iitk"            # Starting the service
    ```

- Please give this repo a star if you found it useful. 😁

- And check out [Additional info](#additional-info).

**NOTE:**  

  \* Dont use the Microsoft Store's python.
  
  ** In the Windows folder, you will find nssm.exe (Non-Sucking Service Manager), which is used to install and manage the Python script as a service. At the time of writing, the NSSM version is 2.24. If you want, you may get the most recent version from [here](https://nssm.cc/download) and replace the old one with the new 64-bit version under the same name (nssm.exe), then do the installation.

### Uninstallation

- Download or [clone](#pre-installation) the repository again and navigate to the *windows* folder to find the uninstallation batch file.
  
- Now, right-click on the `uninstall.bat` and run it as administrator.

- If you encounter **Windows protected your PC** popup, click on `More info` and then choose `Run anyway` (or) If you see any **Unknown publisher** popup, simply choose `Run`.

  - NOTE: This is a simple uninstaller script; there is no need to worry about any viruses.

## MacOS

### Installation

- I'm not rich enough to afford Apple products 🥲. You guys, please find a way to install the below command as a service or simply put it as a startup command:

    ```sh
    python path-to-script/autologin-iitk.py
    ```
- And give this repo a star mate. 😁

### Uninstallation

- Simply undo what you did. 😜

# Additional Info

- The script is designed to self-terminate after 3 Hrs in the case of failures or when you are already connected to internet way beyond refresh time.

- There is a possibility of a maximum downtime of 15 minutes in case reboots are involved, as it doesn't store the last authentication time. 

- In such cases, you can simply restart the service with the below command (former). And for checking logs, you can use the below command (latter):

  - **Windows** (In powershell): 
  
    - For restarting (powershell must be runas **Administrator**), execute below command (or) you can do it from `services.msc`: 

        ```powershell
        Restart-Service -Name "autologin-iitk" -Force
        ```

    - For logs, execute:

        ```powershell
        Get-Content $env:USERPROFILE\AppData\Local\autologin-iitk\autologin-iitk.log
        ```

  - **Linux** (In bash shell): 
  
    - For restarting (need **sudo** privileges), execute: 

        ```sh
        sudo service autologin-iitk restart
        ```

    - For logs, execute:

        ```sh
        journalctl -u autologin-iitk.service -b
        ```

# People

### Author
- Aravind Potluri \<aravindswami135@gmail.com\>

### Contributors
- Abhinav Anand (CSE IITK): Thanks for providing the inital basic script - v1.0.0.

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Feel free to contribute to this project by opening issues and submitting pull requests. Your feedback and contributions are highly appreciated!
