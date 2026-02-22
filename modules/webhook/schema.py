from __future__ import annotations
from typing import TypedDict, NotRequired, Literal, Any

Signal = Literal["BUY", "SELL"]

class WebhookPayload(TypedDict, total=False):
    # auth
    key: NotRequired[str]

    # routing
    engine: str
    signal: Signal

    # market
    symbol: str
    tf: str
    price: float

    # trade params (optional)
    tp: NotRequired[float]
    sl: NotRequired[float]

    # misc
    reason: NotRequired[str]
    raw: NotRequired[dict[str, Any]]
