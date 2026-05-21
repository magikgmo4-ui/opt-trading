---
doc_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01_STEPS
doc_type: steps
go_id: GO_CI_SCHEDULER_AUTOMATION_STABILITY_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: passed_with_evidence
---

# 10_STEPS

1. Recenser tous les workflows CI et timers systemd
2. Définir le smoke critique (cible, fréquence, critère)
3. Documenter le scheduler (timers, cron, déclencheurs)
4. Définir la retry policy (tentatives, backoff, fenêtre)
5. Définir le dead-letter (queue, stockage, alerte)
6. Créer le status JSON (modèle, champs, fréquence)
7. Définir la failure ingestion (collecte, classification)
8. Définir l'alerting (Telegram, journal)
