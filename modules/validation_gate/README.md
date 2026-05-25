# validation_gate

Gate de validation pour propositions de trade — règles auto-bornées + approval opérateur.

## Flow

```
Proposition → GateRequest → risk_check → [BLOCK → REJECTED]
                                       → [ALLOW/CAUTION → operator gate → GateDecision]
```

## Verdicts

| Verdict | Condition |
|---------|-----------|
| APPROVED | Risque ALLOW + opérateur approuvé (ou auto-approve si `require_operator=False`) |
| REJECTED | Kill switch actif, action HOLD/SKIP, proposition en erreur, confiance < min, ou opérateur rejette |
| HOLD | Timeout opérateur (pas de décision dans le délai) |
| NEEDS_REVIEW | CAUTION + `require_operator=False` |

## Commands

```bash
cmd.sh sanity                    # validation complète
cmd.sh test                      # 30 tests unitaires
cmd.sh approve <req_id> [VERDICT] # écrire décision opérateur (APPROVE|REJECT)
cmd.sh status                    # vérifier le module
```

## Env

| Variable | Default | Description |
|----------|---------|-------------|
| `GATE_MIN_CONFIDENCE` | 0.6 | Seuil minimum de confiance |
| `GATE_HIGH_CONFIDENCE` | 0.8 | Seuil de confiance haute (auto-approve) |
| `TRADING_KILL_SWITCH` | — | Si défini, tout est bloqué |
| `GATE_APPROVAL_DIR` | `data/gate_approvals/` | Répertoire des fichiers d'approbation |

## Invariants

- `NO_LIVE_TRADE_WITHOUT_GATE` — aucune exécution de trade dans ce module
- Aucun accès exchange
- Aucun secret dans les logs
