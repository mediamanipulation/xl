# confluence_manager.py
import os
import json
import requests
from cryptography.fernet import Fernet

SETTINGS_FILE = "app_settings.json"
KEY_FILE = "key.key"

# --- Encryption Helpers ---
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_token(token: str) -> str:
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(token_enc: str) -> str:
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(token_enc.encode()).decode()

# --- Settings Management ---
def save_confluence_settings(base_url: str, token: str):
    settings = load_settings()
    settings["confluence"] = {
        "base_url": base_url,
        "token": encrypt_token(token)
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

def forget_confluence_settings():
    settings = load_settings()
    settings.pop("confluence", None)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

def load_confluence_settings():
    settings = load_settings()
    if "confluence" in settings:
        conf = settings["confluence"]
        return {
            "base_url": conf["base_url"],
            "token": decrypt_token(conf["token"])
        }
    return None

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

# --- File Upload ---
def upload_excel_to_confluence(file_path: str, page_id: str):
    settings = load_confluence_settings()
    if not settings:
        raise ValueError("No Confluence settings configured")

    url = f"{settings['base_url']}/rest/api/content/{page_id}/child/attachment"
    headers = {
        "Authorization": f"Bearer {settings['token']}",
    }

    files = {
        'file': (os.path.basename(file_path), open(file_path, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    }

    response = requests.post(url, headers=headers, files=files)
    if not response.ok:
        raise Exception(f"Upload failed: {response.status_code} - {response.text}")
    return response.json()
