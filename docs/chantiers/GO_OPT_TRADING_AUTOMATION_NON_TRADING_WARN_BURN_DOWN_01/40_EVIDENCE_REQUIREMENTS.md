# 40_EVIDENCE_REQUIREMENTS

## Par WARN

| # | WARN | Evidence requise | Format | Critère d'acceptation |
|---|------|------------------|--------|----------------------|
| 1 | strict-worker-readonly-smoke | Script de test E2E + rapport d'exécution | `scripts/ai/tests/g05_strict_worker_e2e_readonly.py` + `reports/ai/strict_worker_e2e_readonly.json` | **PASS** — 3/3 checks pass, 0 git write, 0 secret leak, 0 forbidden write |
| 2 | .env permissions 0644 | `stat` avant/après + audit fichiers sensibles | Texte dans le registre | **CLOSED** — `chmod 600 .env` confirmé ; aucun fichier sensible world-readable |
| 3 | REVIEW_DRAFT absent | Diff du registry + vérification croisée | `tasks.index.json` | **CLOSED** — entrée ajoutée avec sections et workers |
| 4 | CLOSEOUT_DRAFT absent | Diff du registry + vérification croisée | `tasks.index.json` | **CLOSED** — entrée ajoutée avec sections et workers |
| 5 | handoff_bricks.py source | Localisation + décision | Note dans registre | **DECLASSIFIED** — obsolète, aucune importation |
| 6 | handoff_renderer.py source | Localisation + décision | Note dans registre | **DECLASSIFIED** — obsolète, aucune importation |
| 7 | FastAPI absent | Vérification requirements + venv | `requirements.txt` + `venv/` | **DECLASSIFIED** — fastapi + uvicorn présents |
| 8 | kill switch widget | Inspection UI | `registry/cockpit/automation/index.html` | **DECLASSIFIED** — widget présent dans Automation Cockpit |
| 9 | Gmail bridge | Décision HITL de retrait | Note dans registre | **DECLASSIFIED** — retiré du périmètre actif |
| 10 | Calendar bridge | Décision HITL de retrait | Note dans registre | **DECLASSIFIED** — retiré du périmètre actif |
| 11 | Drive bridge | Canary packet write-gated | `scripts/ai/workers/job_packets/GO_DRIVE_CANARY_PACKET_01.json` | **CLOSED** — packet prêt à exécution (credentials requis) |
| 12 | KG index entries | Vérification index/bricks 1:1 | `_state/memory_bricks/index/` + `bricks/` | **DECLASSIFIED** — ratio 1:1 vérifié |
| 13 | Gmail/Calendar/Drive canary | Décision HITL + création Drive canary | Note dans registre + Drive packet | **CLOSED** — Gmail/Calendar retirés, Drive canary créé |

## Principes

- **Aucun secret** ne doit apparaître dans les evidences
- **Aucun fichier .env** ne doit être commité
- Les diffs doivent passer `git diff --check` sans erreur
- Chaque WARN doit avoir une entrée dans le registre avec statut final
