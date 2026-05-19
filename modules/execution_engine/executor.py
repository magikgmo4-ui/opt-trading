"""
Executor
Routes orders to the appropriate adapter.
"""
from typing import Dict, Any
from modules.execution_engine.adapters.paper import PaperAdapter

class Executor:
    def __init__(self):
        self.adapters = {
            "paper": PaperAdapter()
        }

    def execute(self, order: Dict[str, Any], adapter_name: str = "paper") -> Dict[str, Any]:
        """
        Execute an order using the specified adapter.
        """
        adapter = self.adapters.get(adapter_name)
        if not adapter:
            return {"ok": False, "error": f"Adapter '{adapter_name}' not found"}
        
        try:
            return adapter.execute_order(order)
        except Exception as e:
            return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    # CLI Test
    import sys
    import json
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        ex = Executor()
        res = ex.execute({"symbol": "BTCUSDT", "qty": 0.1, "price": 50000}, "paper")
        print(json.dumps(res))
