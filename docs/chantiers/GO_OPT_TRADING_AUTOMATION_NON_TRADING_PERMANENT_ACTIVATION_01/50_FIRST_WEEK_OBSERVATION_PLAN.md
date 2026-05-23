# 50_FIRST_WEEK_OBSERVATION_PLAN

## J1 — Activation Phase 1 (5 timers lecture seule)

```text
Matin :
- [ ] Vérifier git status clean
- [ ] Vérifier kill switch NORMAL
- [ ] Activer timers Phase 1
- [ ] Vérifier systemd --user status
- [ ] Vérifier premier heartbeat ledger

Soir :
- [ ] Vérifier 0 FAIL dans les logs
- [ ] Vérifier 0 WARN nouveaux
- [ ] Vérifier 0 write externe non autorisé
- [ ] Documenter résultats
```

## J2 — Observation Phase 1

```text
Matin :
- [ ] Lire ledger des dernières 24h
- [ ] Vérifier health_status.json
- [ ] Vérifier anti-leak-scan (manuel)

Soir :
- [ ] Gate : PASS → Phase 2 ? (Oui/Non)
```

## J3 — Activation Phase 2 (+4 timers)

```text
Matin :
- [ ] Activer timers Phase 2
- [ ] Vérifier systemd --user status

Soir :
- [ ] Vérifier 0 FAIL
- [ ] Vérifier cohérence ledger
```

## J4-J5 — Observation Phase 2

```text
- [ ] Surveillance continue
- [ ] Vérifier aucun drift
- [ ] Vérifier aucun timer non autorisé actif
```

## J6 — Activation Phase 3 (+2 timers, Drive canary manuel)

```text
Matin :
- [ ] Activer timers Phase 3
- [ ] Exécuter Drive canary manuellement (première fois)
- [ ] Vérifier readback
- [ ] Vérifier ledger event
- [ ] Compensation HITL du fichier canary

Soir :
- [ ] Gate finale : activation complète validée ?
```

## J7 — Bilan semaine

```text
- [ ] Résumé : timers actifs, jobs exécutés, PASS/FAIL/WARN
- [ ] Vérifier aucun accès Gmail/Calendar/trading
- [ ] Vérifier kill switch fonctionnel
- [ ] Documenter leçons apprises
- [ ] Décision : continuer / ajuster / rollback
```

## Critères d'arrêt

- Tout FAIL sur un job READ_ONLY → investigation avant reprise
- Tout write externe non autorisé → kill switch immédiat
- Tout accès Gmail/Calendar/trading → kill switch immédiat + réunion sécurité
- Absence de heartbeat ledger > 15 min → investigation
