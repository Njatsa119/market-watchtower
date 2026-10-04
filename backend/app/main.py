from typing import Any, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.services.alerts import build_alerts
from app.services.market import get_dashboard_snapshot
from app.services.news import fetch_news
from app.services.social import fetch_social_signals

app = FastAPI(title="Market Watchtower", version="0.2.0")

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
    snapshot = get_dashboard_snapshot()
    news = fetch_news()
    social = fetch_social_signals()
    alerts = build_alerts(snapshot.get("assets", []), social, news)

    return {
        "assets": snapshot.get("assets", []),
        "history": snapshot.get("history", {}),
        "market_summary": snapshot.get("market_summary", {}),
        "news": news,
        "social": social,
        "alerts": alerts,
    }


@app.get("/")
def index() -> FileResponse:
    return FileResponse("../frontend/index.html")


@app.get("/favicon.ico")
def favicon() -> FileResponse:
    return FileResponse("../frontend/favicon.svg")
