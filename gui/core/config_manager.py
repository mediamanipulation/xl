# core/config_manager.py
"""Read/write config JSON files anywhere and keep a small MRU list."""

import json
import os

MAX_RECENT = 8          # how many recent files to remember
SETTINGS_FILE = "app_settings.json"


def _load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_settings(settings: dict):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)


def _touch_recent(path: str):
    settings = _load_settings()
    recent = settings.get("recent_configs", [])
    if path in recent:
        recent.remove(path)
    recent.insert(0, path)
    settings["recent_configs"] = recent[:MAX_RECENT]
    _save_settings(settings)


def save_config(config: dict, path: str):
    """Write JSON to *path* and add it to the MRU list."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    _touch_recent(path)


def load_config(path: str) -> dict:
    """Read JSON from *path* and add it to the MRU list."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    _touch_recent(path)
    return data


def list_recent() -> list[str]:
    """Return most-recent-used config paths (newest first)."""
    return _load_settings().get("recent_configs", [])
