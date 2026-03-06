"""
Paper Trading Adapter
Simulates trade execution without external API calls.
"""
from typing import Dict, Any

class PaperAdapter:
    def __init__(self):
        pass

    def execute_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a simulated order.
        """
        return {
            "ok": True,
            "status": "filled",
            "execution_id": f"paper_{order.get('symbol', 'UNK')}_123",
            "filled_qty": order.get("qty", 0),
            "avg_price": order.get("price", 0),
            "adapter": "paper"
        }
