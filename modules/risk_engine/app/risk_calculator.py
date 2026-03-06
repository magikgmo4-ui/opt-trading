"""
Risk Engine Calculator
Provides logic for position sizing and risk management.
"""

import sys

class RiskCalculator:
    def __init__(self, default_risk_per_trade_usd: float = 50.0, max_portfolio_risk_pct: float = 1.0):
        """
        Initialize the Risk Calculator.
        
        Args:
            default_risk_per_trade_usd: Default risk amount in USD per trade.
            max_portfolio_risk_pct: Maximum percentage of portfolio to risk per trade.
        """
        self.default_risk_per_trade_usd = default_risk_per_trade_usd
        self.max_portfolio_risk_pct = max_portfolio_risk_pct

    def calculate_qty(self, entry_price: float, stop_loss: float, balance: float) -> float:
        """
        Calculate position size based on risk parameters.
        
        Args:
            entry_price: Entry price of the asset.
            stop_loss: Stop loss price.
            balance: Current account balance.
            
        Returns:
            Calculated quantity (size) for the trade.
        """
        if entry_price <= 0 or stop_loss <= 0 or balance <= 0:
            return 0.0
            
        risk_per_share = abs(entry_price - stop_loss)
        if risk_per_share == 0:
            return 0.0

        # Risk based on percentage of balance
        max_risk_usd = balance * (self.max_portfolio_risk_pct / 100.0)
        
        # Cap risk at default USD limit
        target_risk = min(max_risk_usd, self.default_risk_per_trade_usd)
        
        qty = target_risk / risk_per_share
        return round(qty, 4)

    def check_safety(self, symbol: str, qty: float, price: float) -> bool:
        """
        Perform safety checks (sanity guardrails).
        
        Args:
            symbol: Trading pair symbol.
            qty: Quantity to trade.
            price: Current price.
            
        Returns:
            True if safe to trade, False otherwise.
        """
        # Placeholder for L4 "garde-fous"
        if qty < 0: # Allow 0 but not negative
            return False
        if price <= 0:
            return False
        return True

if __name__ == "__main__":
    # Simple CLI for testing
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "calc":
            # Usage: calc <entry> <sl> <balance>
            try:
                if len(sys.argv) < 5:
                    print("Usage: calc <entry> <sl> <balance>")
                    sys.exit(1)
                entry = float(sys.argv[2])
                sl = float(sys.argv[3])
                bal = float(sys.argv[4])
                rc = RiskCalculator()
                q = rc.calculate_qty(entry, sl, bal)
                print(f"Calculated Qty: {q}")
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
