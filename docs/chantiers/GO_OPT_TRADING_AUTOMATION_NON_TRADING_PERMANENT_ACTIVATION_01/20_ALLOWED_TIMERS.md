# 20_ALLOWED_TIMERS

## Configuration des timers systemd

| Timer | Job | Intervalle | Unité systemd | Lecture seule |
|-------|-----|------------|---------------|:---:|
| non-trading-repo-status | repo-status-check | 5 min | systemd timer | Oui |
| non-trading-repo-diff | repo-diff-check | 15 min | systemd timer | Oui |
| non-trading-repo-pr-audit | repo-pr-audit | 1 h | systemd timer | Oui |
| non-trading-ledger-heartbeat | ledger-heartbeat | 5 min | systemd timer | Oui |
| non-trading-ledger-replay | ledger-replay-check | 1 h | systemd timer | Oui |
| non-trading-health-status | automation-health-status | 5 min | systemd timer | Oui |
| non-trading-anti-leak | anti-leak-scan | 6 h | systemd timer | Oui |
| non-trading-strict-worker-smoke | strict-worker-readonly-smoke | 30 min | systemd timer | Oui |
| non-trading-capability-validate | capability-matrix-validate | 24 h | systemd timer | Oui |
| non-trading-bridge-validate | bridge-contract-validation | 24 h | systemd timer | Oui |
| non-trading-localcms-sync | localcms-status-sync | 5 min | systemd timer | Oui |

## Timers WRITE_GATED (manuel seulement)

| Job | Déclencheur |
|-----|------------|
| Drive canary packet | HITL manuel via `systemctl --user start non-trading-drive-canary` |

## Activation progressive

```
Phase 1 : 5 timers lecture seule (repo-status, ledger-heartbeat, health-status, localcms-sync, strict-worker-smoke)
→ 24h d'observation
→ Si PASS : Phase 2

Phase 2 : +4 timers (repo-diff, repo-pr-audit, ledger-replay, anti-leak)
→ 48h d'observation
→ Si PASS : Phase 3

Phase 3 : +2 timers (capability-validate, bridge-validate)
→ Drive canary en manuel uniquement
→ Activation complète
```

## Rollback immédiat

```bash
systemctl --user stop 'non-trading-*'
systemctl --user disable 'non-trading-*'
```
