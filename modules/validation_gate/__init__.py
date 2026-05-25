"""validation_gate — risk gate + operator approval pour propositions de trade.

Règles auto-bornées + approval flow opérateur via notification_dispatcher.
INVARIANT: NO_LIVE_TRADE_WITHOUT_GATE — aucun trade executé dans ce module.
"""