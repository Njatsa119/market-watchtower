from __future__ import annotations

import os
from typing import Any, Dict

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.services.alerts import build_alerts
from app.services.market import get_dashboard_snapshot
from app.services.news import fetch_news
from app.services.notifications import send_alert_webhooks
from app.services.social import fetch_social_signals

app = FastAPI(title="Market Watchtower", version="0.3.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler(daemon=True)


def _refresh_market_data() -> Dict[str, Any]:
    snapshot = get_dashboard_snapshot()
    news = fetch_news()
    social = fetch_social_signals()
    alerts = build_alerts(snapshot.get("assets", []), social, news)
    if alerts:
        send_alert_webhooks(alerts)
    return {
        "assets": snapshot.get("assets", []),
        "history": snapshot.get("history", {}),
        "market_summary": snapshot.get("market_summary", {}),
        "news": news,
        "social": social,
        "alerts": alerts,
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "service": "market-watchtower"}


@app.get("/api/dashboard")
def dashboard() -> Dict[str, Any]:
    return _refresh_market_data()


@app.on_event("startup")
def startup_event() -> None:
    if not scheduler.running:
        scheduler.add_job(_refresh_market_data, "interval", minutes=5, id="market-refresh", replace_existing=True)
        scheduler.start()


@app.on_event("shutdown")
def shutdown_event() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)


@app.get("/")
def index() -> FileResponse:
    return FileResponse("../frontend/index.html")


@app.get("/favicon.ico")
def favicon() -> FileResponse:
    return FileResponse("../frontend/favicon.svg")
