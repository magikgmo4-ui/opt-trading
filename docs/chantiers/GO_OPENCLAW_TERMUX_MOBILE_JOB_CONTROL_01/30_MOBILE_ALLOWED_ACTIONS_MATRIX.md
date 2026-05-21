---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01_MOBILE_ALLOWED_ACTIONS_MATRIX
doc_type: action_matrix
go_id: GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01
status: open
updated_at: 2026-05-21
---

# 30_MOBILE_ALLOWED_ACTIONS_MATRIX

## Lecture par niveau

| Niveau | Mobile peut | Gate | Evidence |
|---|---|---|---|
| A0 | rien executer | n/a | blocked reason |
| A1 | consulter, lister, verifier, dry-read | none/preflight | report + ledger if run |
| A2 | demander un draft ou dry-run local | phase packet + preflight | report + ledger |
| HIGH | demander revue ou validation | HITL | decision packet |
| A4 | participer comme approbateur humain | dual confirm / explicit gate | approval + verification packet |

## Actions autorisees initiales

| Action mobile | Autorisation | Condition | Sortie attendue |
|---|---|---|---|
| voir etat repo/job | allowed | read-only | status report |
| lister Phase 01/02 jobs | allowed | registre disponible | job list |
| lancer preflight | allowed | job_id existant | preflight report |
| lancer job Phase 01 read-only | allowed | phase packet PASS | report + ledger |
| refresh LocalCMS status local | allowed | local-only | snapshot + report |
| lire ledger/replay | allowed | read-only | replay summary |
| verifier anti-leak | allowed | read-only/local | PASS/BLOCKED report |
| valider HITL | allowed | packet present | decision packet |
| demander stop/block | allowed | safety reason | blocked event |

## Actions interdites initiales

| Action mobile | Statut | Raison |
|---|---|---|
| write externe direct | forbidden | Phase 08 seulement avec gate |
| signal/trading live | forbidden | hors scope non-trading |
| mutation runtime libre | forbidden | doit deriver du registre et gate |
| modification de secrets | forbidden | surface sensible |
| operation Git destructive | forbidden | surface non mobile |
| bypass HITL | forbidden | rupture gouvernance |
| modification index globaux | forbidden | hors scope sans consigne explicite |

## Actions conditionnelles futures

| Action | Phase minimale | Gate requis | Notes |
|---|---|---|---|
| app bridge read health | Phase 07 | contract gate | read-only |
| canary external write | Phase 08 | dual confirm | canary only + readback |
| scheduler activation | Phase 09 | scheduler policy | apres validation config |
| runtime worker promotion | GO separe | runtime gate | pas dans ce GO |

## Regle d'arbitrage

Si une action n'est pas explicitement autorisee dans cette matrice, elle est traitee comme `forbidden_by_default` jusqu'a ajout dans un GO separe.
