# openclaw_operator_bridge

Interface bornée entre opt-trading et OpenClaw gateway.
opt-trading envoie une requête — OpenClaw builder répond — le bridge retourne un résultat structuré.

## Principe

```
opt-trading → BridgeRequest → OperatorBridge → openclaw agent --agent builder --json → BridgeResponse
```

OpenClaw n'orchestre jamais. Le bridge est le seul point de contact.

## Actions autorisées

| Action | Usage |
|--------|-------|
| `ask` | question ouverte (analyse, explication) |
| `build` | génération de proposition de trade |
| `evaluate` | évaluation d'un signal ou résultat |
| `review` | revue d'une décision ou trade passé |

Toute autre action → `ActionNotAllowed` immédiat.

## Commandes

```bash
scripts/cmd.sh sanity                           # sanity check complet
scripts/cmd.sh health                           # état gateway + CLI
scripts/cmd.sh test                             # tests mock (pas de gateway requis)
scripts/cmd.sh ask "analyse ce signal BTC"      # appel builder
scripts/cmd.sh build "propose un trade XAUUSD"  # génération proposition
```

## Usage Python

```python
from modules.openclaw_operator_bridge.app import OperatorBridge, BridgeRequest

bridge = OperatorBridge()
resp = bridge.send(BridgeRequest(
    action="ask",
    instruction="analyse ce signal BTC haussier",
    context="ticker=BTCUSDT side=long price=65000",
))
print(resp.status, resp.content)
```

## État

```text
GATE 1 Structure   PASS
GATE 2 Sanity      PASS
GATE 3 Mock Tests  PASS (10/10)
GATE 4 Smoke Live  PASS (BRIDGE_OK 2072ms)
GATE 5 Health      PASS
```

## Prérequis runtime

- `openclaw` CLI disponible dans `$PATH`
- gateway actif (`curl http://127.0.0.1:18789/health` → `{"ok":true}`)
- user `ghost` sur `db-layer`
