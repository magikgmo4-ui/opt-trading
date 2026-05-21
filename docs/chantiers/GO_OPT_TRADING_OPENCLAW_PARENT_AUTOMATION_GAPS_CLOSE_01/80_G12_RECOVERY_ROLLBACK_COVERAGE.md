---
doc_id: G12_RECOVERY_ROLLBACK_COVERAGE
doc_type: transversal_coverage
gap_id: G12
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: passed_with_evidence
---

# 80_G12_RECOVERY_ROLLBACK_COVERAGE.md

## Mécanismes de recovery par GO

| Mécanisme | GO source | Déclencheur | Action |
|---|---|---|---|
| **Dry-run guard** | G02 (strict_worker runner) | Toute write attempt | Bloque avant exécution, log dans ledger |
| **Rollback command** | G07 (HITL execution packet) | Échec d'exécution | `rollback_command` dans execution packet |
| **Dead-letter queue** | G09 (CI/scheduler) | Max retry atteint | Stockage + alerte Telegram |
| **Retry policy** | G09 (CI/scheduler) | Échec transient | Exponential backoff, 3 niveaux |
| **Kill switch** | G08 (security) | Anomalie/attaque | Coupe-circuit FULL_STOP ou WRITES_SUSPENDED |
| **Ledger audit** | G06 (observability) | Toute action | Trace complète pour post-mortem |
| **Dual confirm** | G07 (HITL) | Action L6+ | Deuxième approbation avant exécution |
| **Bridge contract rollback** | G04 (bridge contracts) | Échec bridge | `rollback_or_compensating_action` par contrat |

## Error classes et stuck job detection

```yaml
error_classes:
  transient:
    - network_timeout        → retry (G09)
    - rate_limit             → retry with backoff (G09)
    - service_unavailable    → retry (G09)
  permanent:
    - auth_failed            → alerte + dead-letter (G09)
    - invalid_input          → rejet + log ledger (G06)
    - permission_denied      → log BLOCKED dans ledger (G06)
  critical:
    - secret_leak            → kill switch FULL_STOP (G08)
    - data_corruption        → rollback + alerte humaine (G07)
    - security_breach        → kill switch + alerte immédiate (G08)
```

## Stuck job detection

- Un job en statut `running` depuis > 30 min est marqué `stuck`
- Le health_status.py (G09) signale les stuck jobs
- Le dead-letter queue capture les jobs stuck après timeout
- Pas de stuck job sans alerte (G09 alerting → Telegram)
