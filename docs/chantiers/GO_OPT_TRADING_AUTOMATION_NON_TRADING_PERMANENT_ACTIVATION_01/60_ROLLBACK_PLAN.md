# 60_ROLLBACK_PLAN

## Rollback immédiat (urgence)

### Kill switch
```bash
# Arrêter tous les timers non-trading
systemctl --user stop 'non-trading-*'
systemctl --user disable 'non-trading-*'

# Vérifier
systemctl --user list-timers --all | grep 'non-trading' || echo "OK"
```

### Post-rollback
1. Vérifier qu'aucun timer n'est actif
2. Vérifier que le ledger n'a pas d'events non traités
3. Vérifier que Drive n'a pas de fichiers canary orphelins
4. Notifier

## Rollback Phase 1

Si une phase doit être déroulée individuellement :

### Déactivation Phase 1
```bash
systemctl --user stop non-trading-repo-status.timer non-trading-ledger-heartbeat.timer non-trading-health-status.timer non-trading-localcms-sync.timer non-trading-strict-worker-smoke.timer
systemctl --user disable non-trading-repo-status.timer non-trading-ledger-heartbeat.timer non-trading-health-status.timer non-trading-localcms-sync.timer non-trading-strict-worker-smoke.timer
```

### Déactivation Phase 2
```bash
systemctl --user stop non-trading-repo-diff.timer non-trading-repo-pr-audit.timer non-trading-ledger-replay.timer non-trading-anti-leak.timer
systemctl --user disable non-trading-repo-diff.timer non-trading-repo-pr-audit.timer non-trading-ledger-replay.timer non-trading-anti-leak.timer
```

### Déactivation Phase 3
```bash
systemctl --user stop non-trading-capability-validate.timer non-trading-bridge-validate.timer
systemctl --user disable non-trading-capability-validate.timer non-trading-bridge-validate.timer
```

## Rollback Drive canary

```bash
# Localiser le fichier canary (par run_id dans le ledger)
grep "DRIVE_CANARY" data/runtime_health/job_logs/ledger.jsonl

# Suppression manuelle HITL (hors script automatisé)
echo "Supprimer manuellement le fichier .canary.txt du dossier Drive dédié"
echo "Ne pas supprimer/modifier d'autres fichiers"
```

## Compensation

| Scénario | Action |
|----------|--------|
| Timer FAIL 3x consécutifs | Désactiver le timer, investiguer |
| Write non autorisé | Kill switch + audit |
| Secret leak | Kill switch + rotation credentials |
| Drive canary FAIL | Vérifier credentials, réessayer manuellement |
| Ledger missing | Vérifier permissions écriture, réparer |
