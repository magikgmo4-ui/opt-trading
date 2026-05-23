# 40_KILL_SWITCH_LEDGER_POLICY

## Kill Switch

### État normal
- Widget dans Automation Cockpit affiche `● NORMAL`
- Tous les timers actifs
- Tous les jobs READ_ONLY autorisés
- Drive canary en mode WRITE_GATED (manuel)

### Activation du kill switch
```bash
# Arrêt immédiat de tous les timers non-trading
systemctl --user stop 'non-trading-*'
systemctl --user disable 'non-trading-*'

# Vérification
systemctl --user list-timers --all | grep 'non-trading' || echo "OK — tous arrêtés"
```

### Conséquences
- Tous les jobs programmés stoppés
- Les jobs en cours d'exécution terminent leur cycle
- Aucun nouveau job démarré
- Drive canary bloqué (manuel, ne peut pas démarrer sans timer)
- Ledger continue d'accepter les events manuels

### Réactivation
```bash
systemctl --user enable 'non-trading-*'
systemctl --user start 'non-trading-*'
```

Uniquement après investigation et résolution de la cause du déclenchement.

## Ledger Policy

### Events obligatoires
| Événement | Déclencheur | Contenu |
|-----------|-------------|---------|
| JOB_START | Début de chaque job | job_id, run_id, timestamp, surface, mode |
| JOB_PASS | Fin de job PASS | job_id, run_id, duration, output_summary |
| JOB_FAIL | Fin de job FAIL | job_id, run_id, duration, error_details |
| JOB_WARN | Fin de job WARN | job_id, run_id, duration, warning_details |
| KILL_SWITCH_ON | Activation kill switch | user, timestamp, reason |
| KILL_SWITCH_OFF | Désactivation kill switch | user, timestamp, reason |
| DRIVE_CANARY_START | Début canary Drive | run_id, file_path |
| DRIVE_CANARY_PASS | Canary Drive PASS | run_id, readback_ok |
| DRIVE_CANARY_FAIL | Canary Drive FAIL | run_id, reason |
| PHASE_ACTIVATION | Début/fin phase | phase_number, timers_activated, status |

### Stockage
- Fichier : `data/runtime_health/job_logs/ledger.jsonl`
- Format : JSON Lines, une ligne par event
- Rotation : max 10 MB, archivage hebdomadaire

### Vérification
```bash
# Dernier heartbeat
tail -1 data/runtime_health/job_logs/ledger.jsonl | python3 -m json.tool

# Nombre d'events aujourd'hui
grep -c "$(date +%Y-%m-%d)" data/runtime_health/job_logs/ledger.jsonl
```
