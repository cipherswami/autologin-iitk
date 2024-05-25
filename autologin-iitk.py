##############################################################
# Author        : Aravind Potluri <aravindswami135@gmail.com>
# Description   : Auto login script for IITK's firewall 
#                 authentication page.
##############################################################

# Required imports
import urllib.request
import urllib.parse
import logging
import time
import re

# User input for Authentication
username = 'Fill username'
password = 'Fill Password'
gatway_url ='https://gateway.iitk.ac.in:1003/fgtauth?65c8d5b29dad3c97'

# Configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

#### Function declarations ####
def perform_login(opener, login_url, data, timeout=120):
    while True:
        try:
            login_data = urllib.parse.urlencode(data).encode('utf-8')
            login_response = opener.open(login_url, login_data)
            logging.info(f"Connection established: {gatway_url}")
            logout_url = gatway_url.replace('fgtauth', 'logout')
            logging.info(f"Generating logout link: {logout_url}")
            return login_response
        except Exception as e:
            if timeout <= 0: break
            logging.error(f"Retrying, Login failed: {e}")
            time.sleep(2)
            timeout -= 2
    logging.critical(f"Login failed, exiting")
    logging.critical(f"data: {data}")
    exit(1)

def keep_alive(opener, url, timeout=120):
    while True:
        try:
            opener.open(url)
            dead_url = url.replace('keepalive', 'logout')
            logging.info(f"Authentication refreshed, Logout from here: {dead_url}")
            time.sleep(2400)
        except Exception as e:
            if timeout <= 0: break
            logging.warning(f"Can't refresh the authentication: {e}")
            time.sleep(2)
            timeout -= 2
    logging.critical(f"Failed to refresh the authentication: {url}")
    exit(1)
#### End: Function declarations ####

# Entry Point
def main():
    # Create an opener object with custom User-Agent
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')]

    # Payload for login
    data = {"4Tredir": f"{gatway_url}", "username": username, "password": password, 'magic': gatway_url[-16:]}

    # Logging in
    login_response = perform_login(opener, 'https://gateway.iitk.ac.in:1003', data, 120)

    #### Keep Alive Section ####
    # Fetech keep alive url
    login_response_html = login_response.read().decode('utf-8')
    keepalive_matches = re.findall(r'window\.location\s*=\s*"([^"]+)"', login_response_html)
    if keepalive_matches:
        url = keepalive_matches[0]
        logging.info(f"Allocatd Keep Alive URL: {url}")
        time.sleep(2400)
    else:
        logging.critical("No Keep alive URL found, exiting after this")
        logging.critical(f"Login Response: {login_response_html}")
        exit(1)
    # Keep alive refresher
    keep_alive(opener, url, 120)
    #### End: Keep Alive Section ####

if __name__ == "__main__":
    # Execute the script
    main()
