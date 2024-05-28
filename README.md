# Introduction

`autologin-iitk` is a Python script designed to automate the login process for IIT Kanpur's firewall authentication page. This script continuously checks for the captive portal, performs login, and keeps the session alive to maintain internet connectivity without manual intervention.

# Features

- Automatic detection and login to the firewall authentication page.
- Periodic keep-alive requests to maintain the session.
- Self-termination in extreme cases.

# Prerequisites

- Python 3 with properly set environment path.

# Setup and Installation

- **Edit the `autologin-iitk.py` file** to add your username and password:

    ```python
    ####### User section #########################
    username = 'FILL USERNAME'
    password = 'FILL PASSWORD'
    # NOTE: Enter webmail password, not WiFi SSO
    #############################################
    ```

## Linux
### Installation

1. **Clone the repository or [download](https://codeload.github.com/cipherswami/autologin-iitk/zip/refs/heads/main) the zip directly, and navigate to the directory**:

    ```sh
    git clone https://github.com/cipherswami/autologin-iitk.git
    ```

2. **Run the install script** as root:

    ```sh
    chmod +x install_linux.sh
    sudo ./install_linux.sh
    ```

    The install script will:
    - Copy `autologin-iitk.py` to `/usr/local/bin/`.
    - Create a systemd service file, enable it to run at boot, and start the service.

### Uninstallation

1. **Run the uninstall script** as root:

    ```sh
    sudo ./uninstall.sh
    ```

    The uninstall script will:
    - Stop and disable the systemd service.
    - Remove the systemd service file.
    - Remove `autologin-iitk.py` from `/usr/local/bin/`.

## Windows and MacOS

- As of now, just add the following command as a startup script:

    ```sh
    python path-to-script/autologin-iitk.py
    ```

# People

### Author
- Aravind Potluri \<aravindswami135@gmail.com\>

### Contributors
- Abhinav Anand (CSE IITK)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Feel free to contribute to this project by opening issues and submitting pull requests. Your feedback and contributions are highly appreciated!
