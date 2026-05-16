# proposition_engine

Reçoit un `NormalizedSignal` (signal_router), interroge les engines analytiques, puis appelle OpenClaw builder via `openclaw_operator_bridge` pour produire une `Proposition` de trade structurée.

## Pipeline

```
NormalizedSignal
    → query_engines()    # decision_engine + opportunity_ranker + probability_engine
    → compose_prompt()   # contexte analytique structuré
    → OperatorBridge     # OpenClaw builder [EVALUATE]
    → _parse_proposition()
    → Proposition JSON
```

## Output

```json
{
  "action": "BUY|SELL|HOLD|SKIP",
  "size_pct": 0.1,
  "entry": 65000.0,
  "sl": 64000.0,
  "tp": 67000.0,
  "confidence": 0.8,
  "rationale": "...",
  "engines_context": { "decision": {...}, "ranker": {...}, "probability": {...} },
  "status": "ok",
  "dry_run": false
}
```

## Commandes

```bash
scripts/cmd.sh dry BTCUSDT BUY 65000 1h           # dry-run (pas de gateway)
scripts/cmd.sh propose BTCUSDT BUY 65000 1h        # live (nécessite OpenClaw gateway)
scripts/cmd.sh sanity
scripts/cmd.sh test
```

## Invariants

- `dry_run=True` ne touche jamais le gateway OpenClaw
- Si OpenClaw répond du texte non-parseable → `Proposition(action=HOLD, confidence=0)`
- Si un engine échoue → `engines_context` contient l'erreur, `propose()` continue
- Ne déclenche aucun trade

## État

```
Tests    18/18 PASS
Sanity   PASS
Dry-run  PASS (engines_context complet)
Live     nécessite OpenClaw gateway (127.0.0.1:18789)
```
