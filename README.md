# Autologin IITK :: CIPH3R

## Introduction

`autologin-iitk` is a Python script designed to automate the login process for IIT Kanpur's firewall authentication page. This script continuously checks for the captive portal, performs login, and keeps the session alive to maintain internet connectivity without manual intervention.

## Motive

- Servers and most of the computers in labs are connected via LAN and require login to the Firewall page at every boot. To automate this process, this script was created.
- Sometimes, for certain PCs, we might need to connect to **iitk** WiFi only, again for which the firewall page is necessary. Hence, `autologin-iitk`.

# Setup and Installation

### Pre Requisites:

- Python 3 with properly set environment **PATH** variable.

### Pre Installation Setup:

- Git clone the repository (or) download the zip from [here](https://codeload.github.com/cipherswami/autologin-iitk/zip/refs/heads/main), and navigate into the autologin-iitk directory:

    ```sh
    git clone https://github.com/cipherswami/autologin-iitk.git
    ```

- Now, edit the `autologin-iitk.py` file in the **src** folder to add your username and password:

    ```python
    ####### User section #########################
    username = 'FILL USERNAME'
    password = 'FILL PASSWORD'
    # NOTE: Enter webmail password, not WiFi SSO
    #############################################
    ```

### Installation

- Please refer to the following sections for Linux, Windows, and MacOS installation instructions:

## Linux

### Installation

- In autologin-iitk folder, navigate to the *linux* folder to find the installation script:
  
    ```sh
    cd linux
    ```

- Now, grant executable permissions and run the install script:

    ```sh
    chmod +x install.sh
    sudo ./install.sh
    ```

- et voilà! installation is done.

- 😁 Please give this Repo a star if you found it useful.

- And check out [Additional info](#additional-info).
  
### Uninstallation

- In autologin-iitk folder, navigate to the *linux* folder to find the uninstallation script.

- Now, grant executable permissions and run the uninstall script:

    ```sh
    chmod +x uninstall.sh
    sudo ./uninstall.sh
    ```

## Windows

### Installation

- In autologin-iitk folder, navigate to the *windows* folder to find the installation batch file.
  
- Now, right-click `install.bat` and run it as administrator.

- et voilà! installation is done.

- 😁 Please give this Repo a star if you found it useful.

- And check out [Additional info](#additional-info).

### Uninstallation

- In autologin-iitk folder, navigate to the *windows* folder to find the uninstallation batch file.
  
- Now, right-click `uninstall.bat` and run it as administrator.

## MacOS

### Installation

- 🥲 🤣 I'm not rich enough to afford Apple products. You guys, please find a way to install the below command as a service or simply put it as a startup command:

    ```sh
    python path-to-script/autologin-iitk.py
    ```

### Uninstallation

- 😜 Simply undo what you did.

# Additional Info

- The script is designed to self-terminate after 3 Hrs in the case of failures or when you are already connected to internet beyond refresh time (2 Hrs).

- There is a possibility of a maximum downtime of 15 minutes in case reboots are involved, as it doesn't store the last authentication instance. 

- In such cases, you can restart the service and check logs as follow:

  - **Linux**: 
    - In bash terminal execute - `service autologin-iitk restart`
    - For logs, execute - `journalctl -u autologin-iitk`
  
  - **Windows**: 
    - In powershell execute - `Restart-Service -Name "autologin-iitk" -Force` (or) you can do it from `services.msc`
    - For logs, execute - `Get-Content C:\Users\$envs:USERNAME\AppData\Local\auotologin-iitk\autologin-iitk.log`

# People

### Author
- Aravind Potluri \<aravindswami135@gmail.com\>

### Contributors
- Abhinav Anand (CSE IITK): Thanks for providing the inital basic script - v1.0.0.

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Feel free to contribute to this project by opening issues and submitting pull requests. Your feedback and contributions are highly appreciated!
