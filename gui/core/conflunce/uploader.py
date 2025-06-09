# gui/core/confluence/uploader.py

import os
import requests
from gui.core.confluence.config import load_confluence_settings
from gui.core.confluence.metadata import generate_summary


def upload_to_confluence(file_path: str, page_id: str) -> dict:
    """
    Uploads an Excel file to a Confluence page as an attachment.
    Includes a summary comment.
    Returns Confluence response JSON.
    """
    settings = load_confluence_settings()
    if not settings:
        raise ValueError("Confluence settings not configured")

    url = f"{settings['base_url']}/rest/api/content/{page_id}/child/attachment"
    headers = {"Authorization": f"Bearer {settings['token']}", "X-Atlassian-Token": "no-check"}

    with open(file_path, "rb") as f:
        files = {
            "file": (os.path.basename(file_path), f,
                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        }
        response = requests.post(url, headers=headers, files=files)

    if not response.ok:
        raise Exception(f"Upload failed: {response.status_code} - {response.text}")

    summary_text = generate_summary(file_path)
    add_comment_to_page(settings, page_id, summary_text)
    return response.json()


def add_comment_to_page(settings, page_id: str, comment_text: str):
    """
    Posts a comment under a Confluence page.
    """
    url = f"{settings['base_url']}/rest/api/content/{page_id}/child/comment"
    headers = {
        "Authorization": f"Bearer {settings['token']}",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "comment",
        "container": {"type": "page", "id": page_id},
        "body": {
            "storage": {
                "value": comment_text,
                "representation": "storage"
            }
        }
    }
    requests.post(url, headers=headers, json=payload)


