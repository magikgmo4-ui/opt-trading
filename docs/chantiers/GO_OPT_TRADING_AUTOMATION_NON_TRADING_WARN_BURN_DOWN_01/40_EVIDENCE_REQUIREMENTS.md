# 40_EVIDENCE_REQUIREMENTS

## Par WARN

| # | WARN | Evidence requise | Format | Critère d'acceptation |
|---|------|------------------|--------|----------------------|
| 1 | strict-worker-readonly-smoke | Script de test E2E + output d'exécution | Fichier `.sh` ou `.py` + log | Test passe en read-only sans write |
| 2 | .env permissions 0644 | `stat` avant/après + audit fichiers sensibles | Texte dans le registre | `chmod 600 .env` confirmé ; aucun fichier sensible world-readable |
| 3 | REVIEW_DRAFT absent | Diff du registry + vérification croisée | Extrait du diff | Entrée ajoutée ou capability déclassée |
| 4 | CLOSEOUT_DRAFT absent | Diff du registry + vérification croisée | Extrait du diff | Entrée ajoutée ou capability déclassée |
| 5 | handoff_bricks.py source | Localisation + décision (restauration/suppression) | Note dans registre | Source restaurée ou suppression documentée |
| 6 | handoff_renderer.py source | Localisation + décision (restauration/suppression) | Note dans registre | Source restaurée ou suppression documentée |
| 7 | FastAPI absent | Vérification requirements + décision | Note dans registre | Runtime strategy documentée |
| 8 | kill switch widget | Proposition HITL avec emplacement | Note dans registre | Emplacement identifié + proposition faite |
| 9 | Gmail bridge | Inventaire références + décision HITL | Note dans registre | Implémenté ou retiré du contrat |
| 10 | Calendar bridge | Inventaire références + décision HITL | Note dans registre | Implémenté ou retiré du contrat |
| 11 | Drive bridge | Inventaire références + décision HITL | Note dans registre | Implémenté ou retiré du contrat |
| 12 | KG index entries | Localisation index + correction | Extrait du diff | Bricks ajoutées ou entrées retirées |
| 13 | Gmail/Calendar/Drive canary | Décision HITL | Note dans registre | Canary ajoutés ou déclassés |

## Principes

- **Aucun secret** ne doit apparaître dans les evidences
- **Aucun fichier .env** ne doit être commité
- Les diffs doivent passer `git diff --check` sans erreur
- Chaque WARN doit avoir une entrée dans le registre avec statut final
