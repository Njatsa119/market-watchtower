from typing import Any, Dict, List


def _fallback_social() -> List[Dict[str, Any]]:
    return [
        {
            "symbol": "BTC",
            "author": "MarketPulse",
            "content": "BTC sees renewed social heat as traders debate whether the recent breakout is real or another liquidity trap.",
            "engagement": 18400,
            "sentiment": 0.58,
            "rumor_index": 0.71,
            "source": "X-like chatter",
            "link": "https://x.com/search?q=BTC+breakout",
        },
        {
            "symbol": "NVDA",
            "author": "AlphaFlow",
            "content": "AI chip demand narrative still dominating the tape as large volume and chatter accelerate on the back of the latest guidance.",
            "engagement": 9600,
            "sentiment": 0.66,
            "rumor_index": 0.52,
            "source": "X-like chatter",
            "link": "https://x.com/search?q=NVDA+AI+chip",
        },
        {
            "symbol": "TSLA",
            "author": "StreetTalk",
            "content": "Tesla social chatter remains mixed; some traders are framing the move as a short squeeze while others call it a macro-driven fade.",
            "engagement": 13200,
            "sentiment": -0.08,
            "rumor_index": 0.64,
            "source": "X-like chatter",
            "link": "https://x.com/search?q=TSLA+squeeze",
        },
    ]


def fetch_social_signals() -> List[Dict[str, Any]]:
    return _fallback_social()


__all__ = ["fetch_social_signals"]
