# Autologin IITK :: CIPH3R

## Introduction

`autologin-iitk` is a Python script designed to automate the login process for IIT Kanpur's firewall authentication page. This script continuously checks for the firewall authentication portal, performs login, and keeps the session alive to maintain internet connectivity without manual intervention.

## Motive

- Servers and most of the computers in labs are connected via LAN and require login to the firewall authentication page at every boot. To automate this process, this script was made.

- We might need to connect exclusively to the '**iitk**' WiFi SSID in some cases, which again requires logging in to the firewall authentication page. Hence, `autologin-iitk`.

# Installation

### Pre Requisites:

- (Python 3) - If executing the following command in terminal ouputs python version; then you are good to go:

    - Windows

        ```sh
        python --version
        ```
    - Linux & Mac

        ```sh
        python3 --version
        ```

- Else, download latest version of python from [here](https://www.python.org/downloads). And don't forget to add python to environment PATH variable.

### Pre Installation:

- Download the latest ZIP file from [here](https://codeload.github.com/cipherswami/autologin-iitk/zip/refs/heads/main), and extract it (or) Git clone the repository:

    ```sh
    git clone https://github.com/cipherswami/autologin-iitk.git
    ```

- Now, go to the extracted or cloned directory. Edit the `autologin-iitk.py` file in the **src** folder to add your username and password:

    ```python
    ####### User section #########################
    username = 'FILL USERNAME'
    password = 'FILL PASSWORD'
    # NOTE: Enter webmail password, not WiFi SSO
    #############################################
    ```

### Main Installation

- Please refer to the corresponding sections below for installation instructions:

  -  [Windows](#windows)
  -  [Linux](#linux)
  -  [MacOS](#macos)

## Windows 

### Installation

- Inside the downloaded or cloned repository, navigate to the ***windows*** folder to find the installation batch file.
  
- Now, right-click on the `install.bat` and run it as **Administrator**.

- If you encounter **Windows protected your PC** popup, click on `More info` and then choose `Run anyway` (or) If you see any **Unknown publisher** popup, simply choose `Run`.

  - NOTE: This is a simple installer script; there is no need to worry about any viruses. The entire code is open source, so you can review it if you wish.

- Now, open powersehll as **Administrator** and execute below command (or) use `services.msc` to start the service.
  
    ```powershell
    Start-Service -Name "autologin-iitk"
    ```

- et voilà! installation is done.

- Please give this repo a star if you found it useful. 😁

- And check out [Additional info](#additional-info).

**NOTE**: In the Windows folder, you will find nssm.exe (Non-Sucking Service Manager), which is used to install and manage the Python script as a service. At the time of writing, the NSSM version is 2.24. If you want, you may get the most recent version from [here](https://nssm.cc/download) and replace the old one with the new 64-bit version under the same name (nssm.exe), then do the installation.

### Uninstallation

- Inside the downloaded or cloned repository, navigate to the *windows* folder to find the uninstallation batch file.
  
- Now, right-click on the `uninstall.bat` and run it as administrator.

- If you encounter **Windows protected your PC** popup, click on `More info` and then choose `Run anyway` (or) If you see any **Unknown publisher** popup, simply choose `Run`.

  - NOTE: This is a simple uninstaller script; there is no need to worry about any viruses.

## Linux 

### Installation

- Inside the downloaded or cloned repository, open a terminal and navigate to the linux folder to find the installation script:
  
    ```sh
    cd linux
    ```

- Now, grant executable permissions and run the installer script:

    ```sh
    chmod +x install.sh
    sudo ./install.sh
    ```

- et voilà! installation is done.

- Please give this repo a star if you found it useful. 😁

- And check out [Additional info](#additional-info).
  
### Uninstallation

- In autologin-iitk folder, navigate to the *linux* folder to find the uninstallation script.

- Now, grant executable permissions and run the uninstaller script:

    ```sh
    chmod +x uninstall.sh
    sudo ./uninstall.sh
    ```

## MacOS

### Installation

- I'm not rich enough to afford Apple products 🥲🤣. You guys, please find a way to install the below command as a service or simply put it as a startup command:

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
