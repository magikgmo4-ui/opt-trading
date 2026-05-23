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
| non-trading-airtable-health | airtable-read-health | 30 min | systemd timer | Oui |
| non-trading-clickup-health | clickup-read-health | 30 min | systemd timer | Oui |
| non-trading-botpress-health | botpress-read-health | 30 min | systemd timer | Oui |
| non-trading-sheets-health | sheets-read-health | 30 min | systemd timer | Oui |
| non-trading-telegram-digest | telegram-automation-digest | 1 h | systemd timer | Oui |

## Jobs WRITE_GATED (manuel seulement, aucun timer permanent)

| Job | Surface | Déclencheur |
|-----|---------|------------|
| Drive canary packet | drive | HITL manuel via `systemctl --user start non-trading-drive-canary` |
| airtable-write-canary | airtable | HITL manuel |
| clickup-write-canary | clickup | HITL manuel |
| botpress-write-canary | botpress | HITL manuel |
| sheets-write-canary | google_sheets | HITL manuel |

## Activation progressive

```
Phase 1 : 5 timers READ_ONLY core (repo-status, ledger-heartbeat, health-status, localcms-sync, strict-worker-smoke)
→ 24h d'observation
→ Si PASS : Phase 2

Phase 2 : +4 timers READ_ONLY core (repo-diff, repo-pr-audit, ledger-replay, anti-leak)
→ 48h d'observation
→ Si PASS : Phase 3

Phase 3A : +2 timers READ_ONLY registry (capability-validate, bridge-validate)
→ Si PASS : Phase 3B

Phase 3B : +5 timers READ_ONLY external apps (airtable-health, clickup-health, botpress-health, sheets-health, telegram-digest)
→ Drive canary + write canaries externes en manuel uniquement (aucun timer permanent)
→ Activation complète
```

## Rollback immédiat

```bash
systemctl --user stop 'non-trading-*'
systemctl --user disable 'non-trading-*'
```
