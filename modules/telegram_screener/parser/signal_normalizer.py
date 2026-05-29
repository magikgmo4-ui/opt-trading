from __future__ import annotations

from typing import Optional

from .signal_schema import ScreenerSignal


def normalize_signal(signal: ScreenerSignal) -> dict:
    return signal.to_dict()


def classify_raw_text(raw_text: str) -> Optional[str]:
    from .trade_parser import parse_trade_setup
    from .news_parser import parse_news_alert
    from .alpha_parser import parse_alpha_signal

    if parse_trade_setup(raw_text) is not None:
        return "trade"
    if parse_news_alert(raw_text) is not None:
        return "news"
    if parse_alpha_signal(raw_text) is not None:
        return "alpha"
    return None
