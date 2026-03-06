"""
Position Manager
Handles the lifecycle of trading positions.
"""
from typing import Dict, Optional, Any
from datetime import datetime, timezone
from modules.position_engine.models import Position
from modules.position_engine.storage import load_positions, save_positions

class PositionManager:
    def __init__(self):
        # Load state from JSON
        self.positions: Dict[str, Position] = {}
        data = load_positions()
        for k, v in data.items():
            # Reconstruct Position objects
            try:
                # Handle datetime string conversion if needed
                if "opened_at" in v and isinstance(v["opened_at"], str):
                    v["opened_at"] = datetime.fromisoformat(v["opened_at"])
                self.positions[k] = Position(**v)
            except Exception:
                pass

    def _persist(self):
        save_positions(self.positions)

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
        self._persist()
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
        self._persist()
        return {
            "ok": True,
            "status": "closed",
            "symbol": symbol
        }

    def can_open_position(self, symbol: str, side: str) -> Dict[str, Any]:
        """
        Check if a position can be opened (Guardrail).
        Returns: {ok, action, reason}
        """
        pos = self.positions.get(symbol)
        
        # 1. No open position -> ALLOW
        if not pos:
            return {"ok": True, "action": "open", "reason": "no_position"}

        # 2. Same side open -> REJECT
        if pos.side.upper() == side.upper():
            return {"ok": False, "action": "reject", "reason": f"already_{side.lower()}"}

        # 3. Opposite side open -> FLIP
        return {"ok": True, "action": "flip", "reason": "opposite_side_open"}

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
