"""
Position Models
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Position:
    symbol: str
    side: str
    qty: float
    entry_price: float
    opened_at: datetime
    pnl: float = 0.0
    status: str = "OPEN"
