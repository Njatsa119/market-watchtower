import os
from typing import Any, Dict

import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.services.market import get_dashboard_snapshot
from app.services.news import fetch_news

app = FastAPI(title="Market Watchtower", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "service": "market-watchtower"}


@app.get("/api/dashboard")
def dashboard() -> Dict[str, Any]:
    dashboard_data = get_dashboard_snapshot()
    news = fetch_news()

    alerts = []
    for asset in dashboard_data.get("assets", []):
        if abs(float(asset.get("change_pct", 0))) > 2.0 or float(asset.get("rumor_index", 0)) > 0.6:
            alerts.append(
                {
                    "symbol": asset["symbol"],
                    "type": "market_signal",
                    "severity": "medium" if asset.get("rumor_index", 0) > 0.75 else "low",
                    "summary": f"{asset['symbol']} is moving {asset.get('change_pct', 0):+.2f}% with rumor score {asset.get('rumor_index', 0):.2f}",
                }
            )

    dashboard_data["news"] = news
    dashboard_data["alerts"] = alerts
    return dashboard_data


@app.get("/")
def index() -> FileResponse:
    return FileResponse("../frontend/index.html")


@app.get("/favicon.ico")
def favicon() -> FileResponse:
    return FileResponse("../frontend/favicon.svg")
