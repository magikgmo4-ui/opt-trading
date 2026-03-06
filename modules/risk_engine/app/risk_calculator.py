"""
Risk Engine Calculator
Provides logic for position sizing and risk management.
"""

import math
import sys
from typing import Any, Dict, Tuple, Optional

class RiskCalculator:
    def __init__(self):
        """
        Initialize the Risk Calculator.
        Stateless: configuration is passed in at calculation time.
        """
        pass

    @staticmethod
    def safe_float(x: Any) -> float:
        try:
            return float(x)
        except Exception:
            return 0.0

    @staticmethod
    def round_step(x: float, step: float) -> float:
        """
        Round x down to the nearest multiple of step.
        """
        if step <= 0:
            return x
        # Use a small epsilon to avoid floating point issues
        return math.floor(x / step + 1e-12) * step

    def _get_equity_and_risk_pct(self, acct: dict) -> Tuple[float, float]:
        """
        Extract equity and risk percentage from account config.
        
        Args:
            acct: Account configuration dictionary.
            
        Returns:
            Tuple of (equity, risk_pct).
        """
        # equity can be "equity" or "equity_usd"
        equity = float(acct.get("equity_usd", acct.get("equity", 0)) or 0)

        # risk_pct can be 0.01 (1%), or 1 (1%), or 1.0 (1%), or 2 (2%)
        rp = acct.get("risk_pct", 0)
        try:
            rp = float(rp)
        except Exception:
            rp = 0.0

        if rp <= 0:
            risk_pct = 0.0
        elif rp <= 1.0:
            # treat as fraction
            risk_pct = rp
        else:
            # treat as percent
            risk_pct = rp / 100.0

        return equity, risk_pct

    def calculate_quote(self, 
                        account_config: Dict[str, Any], 
                        engine: str, 
                        price: float, 
                        sl: float, 
                        global_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Calculate position size and risk metrics.
        
        Args:
            account_config: Configuration for the specific account/engine.
            engine: Name of the engine (e.g., "GOLD_CFD_LONG", "COINM_SHORT").
            price: Entry price.
            sl: Stop loss price.
            global_config: Optional global configuration (e.g., for gold_cfd settings).
            
        Returns:
            Dictionary containing quote details (qty, risk_usd, etc.).
        """
        global_config = global_config or {}
        
        equity, risk_pct = self._get_equity_and_risk_pct(account_config)
        risk_usd = equity * risk_pct

        distance = abs(price - sl)
        if distance <= 0 or risk_usd <= 0:
            return {
                "ok": True,
                "type": "LINEAR_FALLBACK",
                "risk_usd": round(risk_usd, 6),
                "risk_real_usd": 0,
                "distance": round(distance, 6),
                "qty": 0
            }

        # Default linear: PnL per 1 qty per $ move = 1 (fallback)
        qty = risk_usd / distance

        if engine == "GOLD_CFD_LONG":
            min_units = self.safe_float(account_config.get("min_units", account_config.get("min_qty", 0.1))) or 0.1
            units_step = self.safe_float(account_config.get("units_step", account_config.get("qty_step", 0.1))) or 0.1
            
            qty = max(qty, min_units)
            qty = self.round_step(qty, units_step)
            qty = round(qty, 6)
            risk_real = qty * distance
            
            # Check global config for unit type
            units_are_oz = (global_config.get("gold_cfd", {}) or {}).get("units_are_oz", True)
            
            return {
                "ok": True,
                "type": "GOLD_CFD_OZ" if units_are_oz else "GOLD_CFD",
                "risk_usd": round(risk_usd, 6),
                "risk_real_usd": round(risk_real, 6),
                "distance": round(distance, 6),
                "qty": qty
            }

        # COINM/USDTM: keep generic sizing
        min_qty = self.safe_float(account_config.get("min_qty", 0.001)) or 0.001
        qty_step = self.safe_float(account_config.get("qty_step", 0.001)) or 0.001
        
        qty = max(qty, min_qty)
        qty = self.round_step(qty, qty_step)
        qty = round(qty, 6)
        risk_real = qty * distance
        
        return {
            "ok": True,
            "type": "LINEAR_FALLBACK",
            "risk_usd": round(risk_usd, 6),
            "risk_real_usd": round(risk_real, 6),
            "distance": round(distance, 6),
            "qty": qty
        }

if __name__ == "__main__":
    # Simple CLI for testing
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "calc":
            # Usage: calc <entry> <sl> <equity> <risk_pct> [engine]
            try:
                if len(sys.argv) < 6:
                    print("Usage: calc <entry> <sl> <equity> <risk_pct> <engine>")
                    sys.exit(1)
                
                entry = float(sys.argv[2])
                sl = float(sys.argv[3])
                equity = float(sys.argv[4])
                risk_pct = float(sys.argv[5])
                engine = sys.argv[6] if len(sys.argv) > 6 else "DEFAULT"
                
                rc = RiskCalculator()
                acct_config = {"equity": equity, "risk_pct": risk_pct}
                
                # Mock global config for GOLD_CFD testing
                global_config = {"gold_cfd": {"units_are_oz": True}}
                
                q = rc.calculate_quote(acct_config, engine, entry, sl, global_config)
                print(f"Quote: {q}")
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)
        elif cmd == "sanity":
             print("Risk Engine Module: OK")
        else:
            print(f"Unknown command: {cmd}")
            sys.exit(1)
    else:
        print("Usage: python -m modules.risk_engine.app.risk_calculator <cmd> [args]")
