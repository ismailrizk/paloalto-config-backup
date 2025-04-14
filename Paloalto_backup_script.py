import requests
import urllib3
from datetime import datetime
import os
import getpass

# Suppress SSL warnings (only if necessary - not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration section (edit these variables only)
FIREWALL_IP = input("Enter firewall IP address: ").strip()
USERNAME = input("Enter admin username: ").strip()
PASSWORD = getpass.getpass("Enter admin password: ")
OUTPUT_DIR = r'C:\Backups\PaloAlto'  # Change to your desired backup directory
LOG_FILE = r'C:\Logs\palo_backup_log.txt'  # Change log path as needed


def get_api_key(ip, username, password):
    """Request API key from the firewall."""
    url = f"https://{ip}/api/?type=keygen&user={username}&password={password}"
    response = requests.get(url, verify=False)
    if "<key>" in response.text:
        return response.text.split("<key>")[1].split("</key>")[0]
    raise Exception("Failed to retrieve API key. Check credentials or firewall access.")


def export_config(ip, api_key, output_path):
    """Download the running configuration using the API key."""
    url = f"https://{ip}/api/?type=export&category=configuration&key={api_key}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download config. Status code: {response.status_code}")


def log_message(message):
    """Append a timestamped log entry."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")



try:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    api_key = get_api_key(FIREWALL_IP, USERNAME, PASSWORD)

    filename = f"palo_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    output_path = os.path.join(OUTPUT_DIR, filename)

    export_config(FIREWALL_IP, api_key, output_path)
    log_message(f"Backup successful: {filename}")
    print(f"Backup completed: {filename}")

except Exception as e:
    log_message(f"Backup failed: {e}")
    print(f"Error occurred: {e}")
