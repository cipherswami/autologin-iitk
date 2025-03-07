##############################################################
# Author        : Aravind Potluri <aravindswami135@gmail.com>
# Description   : Auto login script for IITK's firewall 
#                 authentication page, with auto logout.
##############################################################

####### User section #########################
username = 'FILL USERNAME'
password = 'FILL PASSWORD'
# NOTE: Enter webmail password, not WiFi SSO
#############################################

import os
import re
import time
import logging
import tempfile
import platform
import urllib.parse
import urllib.request

if platform.system() == 'Linux':
    format = '%(levelname)s - %(message)s'
    logout_file = "/var/tmp/iitk_logout_url.txt" 
else:
    format = '[%(asctime)s] %(levelname)s - %(message)s'
    logout_file = "C:\\Windows\\Temp\\iitk_logout_url.txt"

logging.basicConfig(level=logging.INFO, format=format, datefmt='%Y-%m-%d %H:%M:%S')

def perform_logout(opener, LOGOUT_FILE):
    if os.path.exists(LOGOUT_FILE):
        with open(LOGOUT_FILE, 'r') as f:
            logout_url = f.read().strip()
        
        if logout_url:
            logging.info(f"Attempting logout: {logout_url[-16:]}")
            timeout = 60
            while timeout > 0:
                try:
                    response_html = opener.open(logout_url).read().decode('utf-8')
                    if "<H3>You have successfully logged out</H3>" in response_html:
                        logging.info("Previous session logged out successfully")
                    if "https://gateway.iitk.ac.in:1003/login" in response_html:
                        logging.info("Previous session already expired")
                    return
                except Exception as e:
                    logging.warning(f"Logout failed, retrying: {e}")
                    time.sleep(5)
                    timeout -= 5
            logging.error("Logout attempts exhausted.")
            exit(1)
        else:
            logging.info("Logout URL file is empty.")
            os.remove(LOGOUT_FILE)
    else:
        logging.info("Logout file not found, skipping logout")

def check_creds(username, password, response):
    if "Firewall authentication failed. Please try again." in response:
        logging.critical("Please check the credentials you entered.")
    elif "keepalive" in response:
        return
    else:
        logging.critical(f"Unexpected error, Response: {response}")
    exit(1)

def perform_login(opener, gateway_url, data, timeout=60):
    login_url = gateway_url[:31]
    login_data = urllib.parse.urlencode(data).encode('utf-8')
    while timeout > 0:
        try:
            login_response_html = opener.open(login_url, login_data).read().decode('utf-8')
            check_creds(username, password, login_response_html)
            logging.info(f"Connection established with URL: {login_url}")
            return login_response_html
        except Exception as e:
            logging.error(f"Login error, retrying: {e}")
            time.sleep(5)
            timeout -= 5
        except KeyboardInterrupt:
            logging.info("Received Termination signal, exiting...")
            exit(0)
    logging.critical(f"Login failed with URL: {login_url}")
    exit(1)

def get_captive_url(opener, detector_url):
    timeout = 60
    while timeout > 0:
        try:
            captive_response_html = opener.open(detector_url).read().decode('utf-8')
            if "url=https://support.mozilla.org/kb/captive-portal" in captive_response_html:
                logging.info("Already connected to internet, will retry after 15 mins.")
                time.sleep(900)  # Sleep 15 mins
                timeout -= 5
                continue
            match = re.search(r'window\.location="(https://[^"]+)"', captive_response_html)
            if match:
                logging.info(f"Found Captive URL: {match.group(1)[-16:]}")
                return match.group(1)
        except Exception as e:
            logging.error(f"Error detecting captive portal, retrying: {e}")
            time.sleep(5)
            timeout -= 5
        except KeyboardInterrupt:
            logging.info("Received Termination signal, exiting...")
            exit(0)
    logging.error("Captive portal detection attempts exhausted.")
    return None

def keep_alive(opener, url, timeout=60):
    """Keep the authentication alive by periodically accessing the keepalive URL."""
    while timeout > 0:
        try:
            opener.open(url)
            dead_url = url.replace('keepalive', 'logout')
            logging.info(f"Authentication refreshed, logout from here: {dead_url}")
            time.sleep(7190)
        except Exception as e:
            logging.error(f"Can't refresh the authentication: {e}")
            time.sleep(5)
            timeout -= 5
        except KeyboardInterrupt:
            logging.info("Received Temination signal, exiting...")
            exit(0)
    logging.critical(f"Failed to refresh the authentication: {url}")
    exit(1)

# Main
if __name__ == "__main__":
    # URL Agent
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

    # Perform initial logout
    perform_logout(opener, logout_file)
    
    # Get gatway URL
    captive_url = get_captive_url(opener, 'http://detectportal.firefox.com/canonical.html')
    
    # Initiate the connection
    init_gateway_response = opener.open(captive_url)
    data = {"4Tredir": captive_url, "username": username, "password": password, 'magic': captive_url[-16:]}
    login_response_html = perform_login(opener, captive_url, data)

    # Closing connections
    init_gateway_response.close()

    #### Keep Alive Section ####
    # Fetch keep-alive URL
    try:
        keepalive_matches = re.findall(r'window\.location\s*=\s*"([^"]+)"', login_response_html)
        if keepalive_matches:
            keep_alive_url = keepalive_matches[0]
            logout_url = keep_alive_url.replace('keepalive', 'logout')
            with open(logout_file, 'w') as f:
                f.write(logout_url)
            logging.info(f"Received Keep alive token, logout from here: {logout_url}")
            time.sleep(7190) # wait for nearly 2 hrs
        else:
            logging.error("No Keep alive URL found, will exit after this session.")
            logging.critical(f"Login Response: {login_response_html}")
            exit(1)
    except KeyboardInterrupt:
        logging.info("Received Temination signal, exiting...")
        exit(0)
    # Keep alive refresher
    keep_alive(opener, keep_alive_url)
    #### End: Keep Alive Section ####
    exit(0)