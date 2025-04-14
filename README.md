# Palo Alto Firewall Configuration Backup Script

This Python script automates the backup of configuration files from a Palo Alto firewall using the device's API.

---

## 🔧 Features

- Secure API key generation
- Configuration export to local disk
- Timestamped logs for backup activity
- Clean, modular code with proper error handling
- Secure credential handling using `getpass`

---

## 📦 Requirements

- Python 3.6+
- Internet access to the firewall’s management interface
- Admin credentials with API access enabled on the Palo Alto firewall

---

## 🛠 Installation

1. Clone or download this repository.
2. Install dependencies:

```bash
pip install -r requirements.txt
