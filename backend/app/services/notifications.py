from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List

import requests


def _webhook_urls() -> List[str]:
    raw = os.getenv("ALERT_WEBHOOK_URLS", "")
    return [item.strip() for item in raw.split(",") if item.strip()]


def send_alert_webhooks(alerts: Iterable[Dict[str, Any]]) -> None:
    urls = _webhook_urls()
    if not urls:
        return

    payload = {"alerts": list(alerts)}
    for url in urls:
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception:
            continue


def send_telegram_message(message: str, token: str | None = None, chat_id: str | None = None) -> bool:
    token = token or os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception:
        return False


__all__ = ["send_alert_webhooks", "send_telegram_message"]
