# CHECKPOINT

GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_ENFORCEMENT_01

## État actuel

| Élément | Statut |
|---------|:------:|
| Politique rétention | MERGED |
| Plan d'enforcement | DRAFT |
| Script diagnostic | DRAFT |
| Script purge | DRAFT |
| Smoke post-purge | NON TESTÉ |
| Rotation automatique | NON APPLIQUÉ |

## Prochaines étapes

1. [ ] Tester le script diagnostic sur la session active
2. [ ] Simuler une purge contrôlée (archiver session active si saturée)
3. [ ] Exécuter le smoke canonique après purge
4. [ ] Décider si cron installé
5. [ ] Fermer le GO

## Décisions en attente

- La rotation doit-elle être manuelle ou automatisée ?
- Faut-il une notification en cas de saturation détectée ?
- Les scripts doivent-ils être commités dans `/opt/trading` ?

## Risques résiduels

- n_ctx=4096 non modifiable sans changement de modèle
- Script d'exécution en sudo (vérifier permissions)
- Purge accidentelle si RETENTION_DAYS trop bas
