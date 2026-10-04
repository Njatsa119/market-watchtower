# Market Watchtower

A lightweight market intelligence dashboard for crypto and stock signals, sentiment, rumor detection and macro/market story monitoring.

## Features

- Crypto market overview (BTC, ETH, SOL, ADA)
- Stock market snapshots (AAPL, NVDA, MSFT, TSLA)
- News sentiment and rumor scoring
- Watchlist-like dashboard cards
- Alerts and signal summaries
- FastAPI backend + static frontend

## Tech stack

- Python 3.11+
- FastAPI
- Requests
- Feedparser
- Static frontend with HTML/CSS/JS

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

The app serves a frontend at the root URL and API routes under `/api/*`.

## Environment variables (optional)

```bash
export ALPHA_VANTAGE_KEY="your_key_here"
```

The app works without a key using fallback sample data and public feeds.

## Notes

This is a prototype watchtower intended for research and exploration. It should not be treated as investment advice.
