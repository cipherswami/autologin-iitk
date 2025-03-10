##############################################################
# Author        : Aravind Potluri <aravindswami135@gmail.com>
# Description   : Auto login script for IITK's firewall 
#                 authentication page, with auto logout.
##############################################################

################ User section ################
# NOTE: Enter webmail password, not WiFi SSO #
USERNAME = 'FILL_USERNAME'
PASSWORD = 'FILL_PASSWORD'
##############################################

# Imports
import os
import re
import time
import logging
import platform
import urllib.parse
import urllib.request

# Platform-Specific Settings
if platform.system() == 'Linux':
    LOGOUT_FILE = "/var/tmp/iitk_logout_url.txt"
    LOG_FORMAT = '%(levelname)s - %(message)s'
else:
    LOGOUT_FILE = "C:\\Windows\\Temp\\iitk_logout_url.txt"
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# Global Settings
DATE_FORMAT = '%b %d %H:%M:%S'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

# Function: Perform Prelogout
def perform_prelogout(opener):
    """Attempts to log out from a previous session if a logout URL exists."""
    if os.path.exists(LOGOUT_FILE):
        with open(LOGOUT_FILE, 'r') as f:
            logout_url = f.read().strip()
        if logout_url:
            logging.info(f"Attempting logout: {logout_url[-16:]}")
            for _ in range(12):  # Retry for 60 seconds
                try:
                    response_html = opener.open(logout_url).read().decode('utf-8')
                    if "successfully logged out" in response_html:
                        logging.info("Previous session logged out successfully")
                        return
                    elif "1003/login" in response_html:
                        logging.info("Previous session already expired")
                        return
                except Exception as e:
                    logging.warning(f"Logout failed, retrying: {e}")
                    time.sleep(5)
            logging.error("Logout attempts exhausted.")
            exit(1)
        else:
            os.remove(LOGOUT_FILE)
            logging.info("Logout URL file is empty.")
    else:
        logging.info("Logout file not found, skipping logout")


# Function: Perform Login
def perform_login(opener, captive_url):
    """Attempts to log in to the IITK firewall authentication page."""
    login_url = captive_url[:31]
    login_data = urllib.parse.urlencode({
        "4Tredir": captive_url,
        "username": USERNAME,
        "password": PASSWORD,
        'magic': captive_url[-16:]
    }).encode('utf-8')
    
    for _ in range(12):  # Retry for 60 seconds
        try:
            init_gateway_response = opener.open(captive_url)  # Open captive portal
            response_html = opener.open(login_url, login_data).read().decode('utf-8')  # Submit login form
            if "authentication failed" in response_html:
                logging.error("Invalid credentials. Please check your login details.")
                exit(1)
            logging.info(f"Login successful at {login_url}")
            init_gateway_response.close()
            return response_html 
        except Exception as e:
            logging.error(f"Login error, retrying: {e}")
            time.sleep(5)
    logging.error("Login failed.")
    exit(1)


# Function: Get Captive Portal URL
def get_captive_url(opener):
    """Detects the captive portal URL required for authentication."""
    for _ in range(12):  # Retry for 60 seconds
        try:
            response_html = opener.open('http://detectportal.firefox.com/canonical.html').read().decode('utf-8')
            
            # Check if already connected to the internet
            if "url=https://support.mozilla.org/kb/captive-portal" in response_html:
                logging.info("Already connected to internet, will retry after 15 mins.")
                time.sleep(900)  # Sleep 15 minutes before retrying
                continue
            
            # Extract captive portal URL
            match = re.search(r'window\.location="(https://[^"]+)"', response_html)
            if match:
                logging.info(f"Captive URL found: {match.group(1)[-16:]}")  # Log last 16 characters
                return match.group(1)
        except Exception as e:
            logging.error(f"Captive portal detection failed, retrying: {e}")
            time.sleep(5)
    logging.error("Failed to detect captive portal.")
    exit(1)


# Function: Keep-Alive Session
def keep_alive(opener, response_html):
    """Extracts keep-alive URL and keeps the authentication session active."""
    keepalive_match = re.search(r'window\.location\s*=\s*"([^"]+)"', response_html)
    
    if keepalive_match:
        keepalive_url = keepalive_match.group(1)  # Extract keep-alive URL
        logout_url = keepalive_url.replace('keepalive', 'logout')  # Generate logout URL

        # Store logout URL for future logouts
        with open(LOGOUT_FILE, 'w') as f:
            f.write(logout_url)
        
        logging.info(f"Keep-Alive received. Logout URL: {logout_url}")

        # Keep refreshing session
        while True:
            try:
                time.sleep(7190)  # Sleep ~2 hours before refreshing session
                opener.open(keepalive_url)  # Refresh session
                logging.info(f"Session replenished. Logout URL: {logout_url}")
            except Exception as e:
                logging.error(f"Keep-alive failed: {e}")
                time.sleep(5)  # Retry after 5 seconds
    else:
        logging.error("No keep-alive URL found. Session will not persist.")
        exit(1)

# Main Execution Flow
def main():
    """Main execution flow for the auto-login script."""
    # Initialize browser agent
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

    # Perform prelogout and login
    perform_prelogout(opener)
    captive_url = get_captive_url(opener)
    response_html = perform_login(opener, captive_url)

    # Start keep-alive mechanism
    keep_alive(opener, response_html)


# Entry Point
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Script terminated by user.")
        exit(0)