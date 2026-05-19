---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01
surface: ADMIN_TRADING
source_kind: canonical
updated_at: 2026-05-19
---

# 40_INGESTION_EXTRACTION_CHECKLIST

## Objectif

Donner une checklist complete pour prouver le flux de bout en bout.

## Capture

| Check | Commande indicative | PASS |
| --- | --- | --- |
| PNG present | `find vision_inbox -name 'screen_*.png'` | au moins 1 PNG recent |
| JSON present | `find vision_inbox -name 'screen_*.json'` | sidecar correspondant |
| Taille PNG | `stat -c %s file.png` | > 1024 octets |
| Taille JSON | `stat -c %s file.json` | > 0, parseable |
| Upload atomique | `find vision_inbox -name '*.uploading'` | aucun stale |
| Dimensions | `file file.png` ou outil image dedie | largeur/hauteur attendues |

## Ingestion

| Check | PASS |
| --- | --- |
| `vision_processed` recoit un artefact | fichier ou metadata recente |
| `vision_outbox` recoit une extraction | texte/md/json recent |
| OCR ou metadata presente | contenu non vide |
| fichiers raw non dupliques indefiniment | mouvement ou statut clair |

## Desk bridge

| Check | PASS |
| --- | --- |
| `desk/snapshots` existe | dossier present |
| `latest.json` existe | JSON parseable |
| `history.jsonl` existe | lignes append-only ou politique explicite |
| Desk Pro latest consomme | surface finale visible ou metadata recente |

## Etat actuel observe 2026-05-19

| Check | Etat |
| --- | --- |
| PNG `vision_inbox` | FAIL, 0 PNG |
| JSON `vision_inbox` | PARTIAL, 77 sidecars |
| `.uploading` | PASS, 0 observe dans dossiers cibles |
| `vision_processed` | FAIL, vide |
| `vision_outbox` | FAIL, vide |
| `desk/snapshots` | FAIL, dossier manquant |
| service capture | FAIL, `Cannot find module 'playwright'` |

## Verdict courant

`BLOCKED_WITH_REASON_PLAYWRIGHT_MISSING_NO_PNG_INGESTION_NOT_PROVEN`

