##############################################################
# Author        : Aravind Potluri <aravindswami135@gmail.com>
# Description   : Auto login script for IITK's firewall 
#                 authentication page, with auto logout.
##############################################################

####### User section #########################
USERNAME = 'FILL USERNAME'
PASSWORD = 'FILL PASSWORD'
# NOTE: Enter webmail password, not WiFi SSO
#############################################

import os
import re
import time
import logging
import platform
import subprocess
import urllib.parse
import urllib.request

# Platform-Specific Settings
if platform.system() == 'Linux':
    LOGOUT_FILE = "/var/tmp/iitk_logout_url.txt"
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    def log_event(message, level="INFO"):
        getattr(logging, level.lower(), logging.info)(message)
else:
    LOGOUT_FILE = "C:\\Windows\\Temp\\iitk_logout_url.txt"
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    def log_event(message, level="INFO"):
        getattr(logging, level.lower(), logging.info)(message)
        event_type_map = {"INFO": "Information", "WARNING": "Warning", "ERROR": "Error"}
        subprocess.run([
            "powershell.exe", "-Command",
            f'Write-EventLog -LogName Application -Source "autologin-iitk" -EntryType {event_type_map.get(level, "Information")} -EventId 999 -Message "{message}"'
        ], shell=True)

def perform_logout(opener):
    """Attempts to log out from a previous session if a logout URL exists."""
    if os.path.exists(LOGOUT_FILE):
        with open(LOGOUT_FILE, 'r') as f:
            logout_url = f.read().strip()
        
        if logout_url:
            log_event(f"Attempting logout: {logout_url[-16:]}", "INFO")
            for _ in range(12):  # Retry for 60 seconds
                try:
                    response_html = opener.open(logout_url).read().decode('utf-8')
                    if "successfully logged out" in response_html or "1003/login" in response_html:
                        log_event("Previous session logged out successfully", "INFO")
                        return
                except Exception as e:
                    log_event(f"Logout failed, retrying: {e}", "WARNING")
                    time.sleep(5)
            log_event("Logout attempts exhausted.", "ERROR")
            exit(1)
        else:
            os.remove(LOGOUT_FILE)
            log_event("Logout URL file is empty.", "INFO")
    else:
        log_event("Logout file not found, skipping logout", "INFO")

def check_login_response(response):
    """Validates the login response to check for authentication success."""
    if "authentication failed" in response:
        log_event("Invalid credentials. Please check your login details.", "ERROR")
        exit(1)
    elif "keepalive" not in response:
        log_event(f"Unexpected login response: {response}", "ERROR")
        exit(1)

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
            init_gateway_response = opener.open(captive_url)
            response_html = opener.open(login_url, login_data).read().decode('utf-8')
            check_login_response(response_html)
            log_event(f"Login successful at {login_url}", "INFO")
            init_gateway_response.close()
            return response_html
        except Exception as e:
            log_event(f"Login error, retrying: {e}", "ERROR")
            time.sleep(5)
    log_event("Login failed.", "ERROR")
    exit(1)

def get_captive_url(opener):
    """Detects the captive portal URL required for authentication."""
    for _ in range(12):  # Retry for 60 seconds
        try:
            response_html = opener.open('http://detectportal.firefox.com/canonical.html').read().decode('utf-8')
            if "url=https://support.mozilla.org/kb/captive-portal" in response_html:
                log_event("Already connected to internet, will retry after 15 mins.", "INFO")
                time.sleep(900)  # Sleep 15 mins
                timeout -= 5
                continue
            match = re.search(r'window\.location="(https://[^"]+)"', response_html)
            if match:
                log_event(f"Captive URL found: {match.group(1)[-16:]}", "INFO")
                return match.group(1)
        except Exception as e:
            log_event(f"Captive portal detection failed, retrying: {e}", "ERROR")
            time.sleep(5)
    log_event("Failed to detect captive portal.", "ERROR")
    exit(1)

def keep_alive(opener, keepalive_url):
    """Keeps the authentication session active by periodically refreshing it."""
    while True:
        try:
            opener.open(keepalive_url)
            log_event(f"Session replenished. Logout URL: {keepalive_url.replace('keepalive', 'logout')}", "INFO")
            time.sleep(7190)  # Keep alive for nearly 2 hours
        except Exception as e:
            log_event(f"Keep-alive failed: {e}", "ERROR")
            time.sleep(5)

def main():
    """Main execution flow for the auto-login script."""
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    
    perform_logout(opener)

    captive_url = get_captive_url(opener)
    response_html = perform_login(opener, captive_url)

    keepalive_match = re.search(r'window\.location\s*=\s*"([^"]+)"', response_html)
    if keepalive_match:
        keepalive_url = keepalive_match.group(1)
        with open(LOGOUT_FILE, 'w') as f:
            f.write(keepalive_url.replace('keepalive', 'logout'))
        log_event(f"Keep-Alive received. Logout URL: {keepalive_url.replace('keepalive', 'logout')}", "INFO")
        time.sleep(7190)  # Wait for nearly 2 hrs
        keep_alive(opener, keepalive_url)
    else:
        log_event("No keep-alive URL found. Session will not persist.", "ERROR")
        exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_event("Script terminated by user.", "INFO")
        exit(0)
