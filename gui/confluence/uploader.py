# gui/confluence/uploader.py
import os
import requests
from .settings import load_confluence_settings


def upload_to_page(file_path: str, page_id: str) -> dict:
    """Uploads a file to the specified Confluence page as an attachment."""
    settings = load_confluence_settings()
    if not settings:
        raise ValueError("Confluence settings not configured")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    url = f"{settings['base_url'].rstrip('/')}/rest/api/content/{page_id}/child/attachment"
    headers = {"Authorization": f"Bearer {settings['token']}"}
    files = {
        'file': (os.path.basename(file_path), open(file_path, 'rb'),
                 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    }

    response = requests.post(url, headers=headers, files=files)
    if not response.ok:
        raise Exception(f"Upload failed: {response.status_code} - {response.text}")
    return response.json()
