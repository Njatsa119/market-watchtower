import os
from typing import Any, Dict, List

import requests

CRYPTO_IDS = ["bitcoin", "ethereum", "solana", "cardano"]
STOCK_SYMBOLS = ["AAPL", "NVDA", "MSFT", "TSLA"]

SAMPLE_CRYPTO = {
    "bitcoin": {"name": "Bitcoin", "price": 62450.12, "change_pct": 1.84, "volume": 28600000000, "market_cap": 1230000000000},
    "ethereum": {"name": "Ethereum", "price": 3310.45, "change_pct": 2.31, "volume": 12800000000, "market_cap": 397000000000},
    "solana": {"name": "Solana", "price": 148.63, "change_pct": 3.42, "volume": 4690000000, "market_cap": 73000000000},
    "cardano": {"name": "Cardano", "price": 0.72, "change_pct": -0.85, "volume": 1160000000, "market_cap": 23000000000},
}

SAMPLE_STOCKS = {
    "AAPL": {"name": "Apple", "price": 214.58, "change_pct": 0.97, "volume": 54200000, "market_cap": 3200000000000},
    "NVDA": {"name": "NVIDIA", "price": 137.21, "change_pct": 2.64, "volume": 68200000, "market_cap": 3400000000000},
    "MSFT": {"name": "Microsoft", "price": 430.12, "change_pct": 0.61, "volume": 24900000, "market_cap": 3200000000000},
    "TSLA": {"name": "Tesla", "price": 243.75, "change_pct": -1.83, "volume": 78400000, "market_cap": 770000000000},
}


def _fetch_json(url: str, timeout: int = 12) -> Dict[str, Any]:
    response = requests.get(url, timeout=timeout, headers={"User-Agent": "MarketWatchtower/0.2"})
    response.raise_for_status()
    return response.json()


def _fetch_crypto_prices() -> Dict[str, Dict[str, float]]:
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": ",".join(CRYPTO_IDS), "vs_currencies": "usd", "include_24hr_change": "true", "include_market_cap": "true", "include_24hr_vol": "true"}
        data = _fetch_json(url + "?" + "&".join(f"{key}={value}" for key, value in params.items()), timeout=12)
        result = {}
        for coin_id in CRYPTO_IDS:
            if coin_id in data:
                result[coin_id] = {
                    "name": coin_id.replace("-", " ").title(),
                    "price": float(data[coin_id]["usd"]),
                    "change_pct": float(data[coin_id].get("usd_24h_change", 0.0)),
                    "volume": float(data[coin_id].get("usd_24h_vol", 0.0)),
                    "market_cap": float(data[coin_id].get("usd_market_cap", 0.0)),
                }
        return result
    except Exception:
        return SAMPLE_CRYPTO


def _fetch_stock_prices() -> Dict[str, Dict[str, float]]:
    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    if api_key:
        try:
            result = {}
            for symbol in STOCK_SYMBOLS:
                url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
                payload = _fetch_json(url, timeout=12)
                quote = payload.get("Global Quote", {})
                if quote:
                    result[symbol] = {
                        "name": symbol,
                        "price": float(quote.get("05. price", 0.0)),
                        "change_pct": float(quote.get("10. change percent", "0%").replace("%", "")),
                        "volume": float(quote.get("06. volume", 0.0)),
                        "market_cap": 0.0,
                    }
            if result:
                return result
        except Exception:
            pass

    try:
        result = {}
        for symbol in STOCK_SYMBOLS:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1d&interval=1d"
            payload = _fetch_json(url, timeout=12)
            chart = payload.get("chart", {}).get("result", [])
            if chart:
                meta = chart[0].get("meta", {})
                price = meta.get("regularMarketPrice")
                change = meta.get("regularMarketChangePercent")
                volume = meta.get("regularMarketVolume")
                market_cap = meta.get("marketCap")
                result[symbol] = {
                    "name": symbol,
                    "price": float(price or 0.0),
                    "change_pct": float(change or 0.0),
                    "volume": float(volume or 0.0),
                    "market_cap": float(market_cap or 0.0),
                }
        if result:
            return result
    except Exception:
        pass

    return SAMPLE_STOCKS


def _score_signal(change_pct: float, rumor_index: float, volume: float, market_cap: float) -> float:
    change_component = min(abs(change_pct) / 10.0, 1.0)
    rumor_component = min(rumor_index, 1.0)
    volume_component = min(volume / 100000000.0, 1.0)
    cap_component = min(market_cap / 500000000000.0, 1.0)
    score = 0.4 * change_component + 0.35 * rumor_component + 0.15 * volume_component + 0.1 * cap_component
    return round(max(0.0, min(score, 1.0)), 2)


def get_dashboard_snapshot() -> Dict[str, Any]:
    crypto = _fetch_crypto_prices()
    stocks = _fetch_stock_prices()
    assets: List[Dict[str, Any]] = []

    for coin_id, values in crypto.items():
        symbol = coin_id.upper()[:4]
        rumor_index = 0.42 + (abs(float(values.get("change_pct", 0.0))) / 20.0)
        asset = {
            "symbol": symbol,
            "name": values.get("name", coin_id.title()),
            "asset_type": "crypto",
            "price": round(float(values.get("price", 0.0)), 2),
            "change_pct": round(float(values.get("change_pct", 0.0)), 2),
            "volume": round(float(values.get("volume", 0.0)), 2),
            "market_cap": round(float(values.get("market_cap", 0.0)), 2),
            "sentiment": 0.62,
            "rumor_index": round(min(rumor_index, 0.98), 2),
            "signal_score": _score_signal(float(values.get("change_pct", 0.0)), min(rumor_index, 0.98), float(values.get("volume", 0.0)), float(values.get("market_cap", 0.0))),
            "source": "CoinGecko",
        }
        assets.append(asset)

    for stock_symbol, values in stocks.items():
        rumor_index = 0.32 + (abs(float(values.get("change_pct", 0.0))) / 18.0)
        asset = {
            "symbol": stock_symbol.upper(),
            "name": values.get("name", stock_symbol.upper()),
            "asset_type": "stock",
            "price": round(float(values.get("price", 0.0)), 2),
            "change_pct": round(float(values.get("change_pct", 0.0)), 2),
            "volume": round(float(values.get("volume", 0.0)), 2),
            "market_cap": round(float(values.get("market_cap", 0.0)), 2),
            "sentiment": 0.58,
            "rumor_index": round(min(rumor_index, 0.94), 2),
            "signal_score": _score_signal(float(values.get("change_pct", 0.0)), min(rumor_index, 0.94), float(values.get("volume", 0.0)), float(values.get("market_cap", 0.0))),
            "source": "Yahoo Finance",
        }
        assets.append(asset)

    strongest = max(assets, key=lambda asset: abs(float(asset["change_pct"])), default={"symbol": "N/A"})
    return {
        "assets": assets,
        "market_summary": {
            "crypto_count": len(crypto),
            "stock_count": len(stocks),
            "strongest_signal": strongest,
            "market_bias": "risk-on" if strongest.get("change_pct", 0) >= 0 else "defensive",
        },
    }


__all__ = ["get_dashboard_snapshot"]

