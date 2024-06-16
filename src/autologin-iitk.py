##############################################################
# Author        : Aravind Potluri <aravindswami135@gmail.com>
# Description   : Auto login script for IITK's firewall 
#                 authentication page.
##############################################################

####### User section #########################
username = 'FILL USERNAME'
password = 'FILL PASSWORD'
# NOTE: Enter webmail password, not WiFi SSO
#############################################

# Required imports
import re
import time
import logging
import platform
import urllib.parse
import urllib.request

# Assessing the platfrom
if platform.system() == 'Linux':
    format='%(levelname)s - %(message)s'
else:
    format='[%(asctime)s] %(levelname)s - %(message)s'

# Configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format=format,
    datefmt='%Y-%m-%d %H:%M:%S')

#### Function declarations ####
def check_creds(username, password, response):
    """Check if the provided credentials are valid."""
    if "Firewall authentication failed. Please try again." in response:
        logging.critical("Please check the credentials you entered.")
    elif "keepalive" in response:
        return
    else:
        logging.critical("Unexpected error, Response: {response}")
    exit(1)

def get_captive_url(opener, detector_url, timeout=60):
    """Detect the captive portal URL."""
    while timeout > 0:
        try:
            response = opener.open(detector_url)
            html = response.read().decode('utf-8')
            match = re.compile(r'window\.location="(https://[^"]+)"').search(html)
            if match:
                captive_url = match.group(1)
                logging.info(f"Found Captive URL with magic token: {captive_url[-16:]}")
                return captive_url
            if "url=https://support.mozilla.org/kb/captive-portal" in html:
                logging.info("Already connected to internet, will retry after 15 mins.")
                time.sleep(900) # sleep 15 mins
                timeout -= 5 # 60/5 = 12 -> 12*900 = 10800 sec (3 Hrs)
            else:
                logging.error("No Captive URL found, exiting.")
                logging.critical(f"Detector Response: {html}")
                break
        except Exception as e:
            logging.error(f"Can't connect to firewall page: {e}")
            time.sleep(5)
            timeout -= 5
        except KeyboardInterrupt:
            logging.info("Received Temination signal, exiting...")
            exit(0)
    logging.critical(f"Detector URL: {detector_url}")
    exit(1)

def perform_login(opener, gateway_url, data, timeout=60):
    """Perform the login to the captive portal."""
    login_url = gateway_url[:31]
    login_data = urllib.parse.urlencode(data).encode('utf-8')
    while timeout > 0:
        try:
            login_response = opener.open(login_url, login_data)
            login_response_html = login_response.read().decode('utf-8')
            check_creds(username, password, login_response_html)
            logging.info(f"Connection established with URL: {login_url}")
            logout_url = gateway_url.replace('fgtauth', 'logout')
            logging.info(f"Generating logout link: {logout_url}")
            return login_response_html
        except Exception as e:
            logging.error(f"Login error, retrying: {e}")
            time.sleep(5)
            timeout -= 5
        except KeyboardInterrupt:
            logging.info("Received Temination signal, exiting...")
            exit(0)
    logging.critical(f"Login failed with URL: {login_url}")
    exit(1)

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
#### End: Function declarations ####

# Entry Point
def main():
    # Create an opener object with custom User-Agent
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', user_agent)]

    # Get the captive portal URL
    gateway_url = get_captive_url(opener, 'http://detectportal.firefox.com/canonical.html')

    # Open connection with Gateway
    init_gateway_response = opener.open(gateway_url)

    # Payload for login
    data = {
        "4Tredir": gateway_url,
        "username": username,
        "password": password,
        'magic': gateway_url[-16:]
    }

    # Log in to Gateway
    login_response_html = perform_login(opener, gateway_url, data)

    # Closing connections
    init_gateway_response.close()

    #### Keep Alive Section ####
    # Fetch keep-alive URL
    try:
        keepalive_matches = re.findall(r'window\.location\s*=\s*"([^"]+)"', login_response_html)
        if keepalive_matches:
            keep_alive_url = keepalive_matches[0]
            logging.info(f"Received Keep alive token: {keep_alive_url[-16:]}")
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

if __name__ == "__main__":
    # Execute the script
    main()
