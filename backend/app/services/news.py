from __future__ import annotations

import os
import re
from typing import Any, Dict, List

import feedparser
import requests

NEWS_URLS = [
    "https://news.google.com/rss/search?q=bitcoin+crypto",
    "https://news.google.com/rss/search?q=stock+market",
    "https://news.google.com/rss/search?q=crypto+rumor",
]

POSITIVE_WORDS = [
    "surge", "rally", "breakout", "bullish", "support", "momentum", "uptrend", "strong", "gain",
    "boost", "rebound", "approval", "adoption", "inflow", "bulls", "upgrade"
]
NEGATIVE_WORDS = [
    "drop", "selloff", "bearish", "panic", "liquidity", "crash", "risk", "weak", "decline", "down", "pressure",
    "dump", "fraud", "hack", "warning", "concern", "outflow", "slump"
]
RUMOR_WORDS = [
    "rumor", "allegedly", "whistleblower", "leak", "speculation", "insider", "possible", "unconfirmed",
    "secret", "mystery", "frenzy", "pump", "manipulation", "meme", "suspicious"
]


def _score_headline(title: str) -> Dict[str, float]:
    text = title.lower()
    pos = sum(1 for word in POSITIVE_WORDS if word in text)
    neg = sum(1 for word in NEGATIVE_WORDS if word in text)
    rumor = sum(1 for word in RUMOR_WORDS if word in text)

    sentiment = (pos - neg) / max(1, pos + neg + 1)
    rumor_score = min(1.0, rumor / 5.0)
    return {"sentiment": round(sentiment, 2), "rumor_index": round(rumor_score, 2)}


def _safe_text(value: Any) -> str:
    return str(value or "")


def fetch_news(limit: int = 12) -> List[Dict[str, Any]]:
    all_entries: List[Dict[str, Any]] = []
    for url in NEWS_URLS:
        try:
            response = requests.get(url, timeout=12, headers={"User-Agent": "MarketWatchtower/0.2"})
            response.raise_for_status()
            feed = feedparser.parse(response.text)
            for entry in feed.entries[:5]:
                title = _safe_text(entry.get("title", "News update"))
                summary = _safe_text(entry.get("summary", title))
                score = _score_headline(title)
                all_entries.append(
                    {
                        "title": title,
                        "summary": summary[:180],
                        "url": _safe_text(entry.get("link", "#")),
                        "published": _safe_text(entry.get("published", "recent")),
                        "sentiment": score["sentiment"],
                        "rumor_index": score["rumor_index"],
                        "category": "markets",
                    }
                )
        except Exception:
            continue

    seen = set()
    unique = []
    for item in all_entries:
        key = item["title"]
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)

    return unique[:limit]


__all__ = ["fetch_news"]
