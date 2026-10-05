# Market Watchtower

A lightweight market intelligence dashboard for crypto and stock signals, sentiment, rumor detection, social chatter, and alerting.

## Features

- Live market snapshots for crypto and equities
- RSS news aggregation + sentiment and rumor scoring
- Social/X-style chatter feed with fallback data
- Alert generation based on market momentum, rumor risk, and social acceleration
- Scheduled refresh + webhook alert support
- FastAPI backend powering a single-page dashboard

## Tech stack

- Python 3.11+
- FastAPI
- Requests
- Feedparser
- APScheduler

## Quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

```text
http://localhost:8000
```

## Optional environment variables

```bash
export ALPHA_VANTAGE_KEY="your_key_here"
export X_BEARER_TOKEN="your_x_bearer_token_here"
export ALERT_WEBHOOK_URLS="https://example.com/alerts,https://hooks.slack.com/services/xxx"
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

Without keys, the app uses public fallback data and sample sentiment feeds so the dashboard still works.

## Notes

This is a prototype and research dashboard. It is not investment advice.
