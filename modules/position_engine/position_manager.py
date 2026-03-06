"""
Position Manager
Handles the lifecycle of trading positions.
"""
from typing import Dict, Optional, Any
from datetime import datetime, timezone
from modules.position_engine.models import Position

class PositionManager:
    def __init__(self):
        # In-memory storage for scaffold: Symbol -> Position
        self.positions: Dict[str, Position] = {}

    def open_position(self, symbol: str, side: str, qty: float, price: float) -> Dict[str, Any]:
        """
        Open a new position or add to existing (scaffold: overwrite).
        """
        pos = Position(
            symbol=symbol,
            side=side,
            qty=qty,
            entry_price=price,
            opened_at=datetime.now(timezone.utc)
        )
        self.positions[symbol] = pos
        return {
            "ok": True,
            "status": "opened",
            "position": pos.__dict__
        }

    def close_position(self, symbol: str) -> Dict[str, Any]:
        """
        Close an existing position.
        """
        pos = self.positions.get(symbol)
        if not pos:
            return {"ok": False, "error": "Position not found"}
        
        pos.status = "CLOSED"
        del self.positions[symbol]
        return {
            "ok": True,
            "status": "closed",
            "symbol": symbol
        }

    def get_position(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve position details.
        """
        pos = self.positions.get(symbol)
        if not pos:
            return None
        return pos.__dict__

if __name__ == "__main__":
    # CLI Test
    import sys
    import json
    
    # Custom JSON encoder for datetime
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            return super().default(o)

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        pm = PositionManager()
        pm.open_position("BTCUSDT", "BUY", 0.1, 50000)
        res = pm.get_position("BTCUSDT")
        print(json.dumps(res, cls=DateTimeEncoder))
