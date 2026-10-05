from typing import Any, Dict, List


def build_alerts(assets: List[Dict[str, Any]], social: List[Dict[str, Any]], news: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    alerts: List[Dict[str, Any]] = []
    for asset in assets:
        signal = float(asset.get("signal_score", 0.0))
        rumor = float(asset.get("rumor_index", 0.0))
        change = float(asset.get("change_pct", 0.0))
        if signal >= 0.7 or rumor >= 0.8 or abs(change) >= 3.0:
            alerts.append(
                {
                    "symbol": asset.get("symbol", "UNK"),
                    "type": "market_signal",
                    "severity": "high" if signal >= 0.8 or rumor >= 0.9 else "medium",
                    "summary": f"{asset.get('symbol')} is showing elevated momentum and rumor risk. 24h move: {change:+.2f}%.",
                }
            )

    for item in social:
        if float(item.get("rumor_index", 0.0)) >= 0.65:
            alerts.append(
                {
                    "symbol": item.get("symbol", "UNK"),
                    "type": "social_signal",
                    "severity": "medium",
                    "summary": f"Social chatter is elevated for {item.get('symbol')} and contains rumor-like language.",
                }
            )

    for item in news:
        if float(item.get("rumor_index", 0.0)) >= 0.6:
            alerts.append(
                {
                    "symbol": "NEWS",
                    "type": "news_signal",
                    "severity": "low",
                    "summary": f"Rumor-sensitive market headline: {item.get('title', 'Market update')[:90]}",
                }
            )

    unique = {}
    for alert in alerts:
        key = (alert["type"], alert["symbol"], alert["summary"])
        unique[key] = alert
    return list(unique.values())[:20]


__all__ = ["build_alerts"]

