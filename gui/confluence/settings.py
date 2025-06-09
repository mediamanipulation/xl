# gui/confluence/settings.py
import os
import json
from cryptography.fernet import Fernet

SETTINGS_FILE = "app_settings.json"
KEY_FILE = "key.key"


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


def save_confluence_settings(base_url: str, token: str):
    settings = load_settings()
    settings["confluence"] = {
        "base_url": base_url,
        "token": encrypt_token(token)
    }
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
