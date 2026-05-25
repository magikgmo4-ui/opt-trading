"""trade_executor — exécution de trades validés par validation_gate.

V1 : paper adapter uniquement — pas de Bitget live.
INVARIANT: NO_LIVE_TRADE_WITHOUT_GATE — gate_decision doit être APPROVED.
"""