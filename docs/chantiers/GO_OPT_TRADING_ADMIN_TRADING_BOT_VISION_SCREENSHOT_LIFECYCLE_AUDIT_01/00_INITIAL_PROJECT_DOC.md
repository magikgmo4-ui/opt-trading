---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01
surface: ADMIN_TRADING
source_kind: canonical
updated_at: 2026-05-19
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Stabiliser le Bot Vision Headless Screenshot Lifecycle cote `admin-trading` : choix des pages a capturer, validation ingestion, nommage, classement, extraction, puis politique de retention, compression et archive avec validation humaine.

## 2_INITIAL_PROJECT_DOC

Document transporteur du chantier :

`docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01/00_INITIAL_PROJECT_DOC.md`

## 3_INITIAL_NEED

Le module `modules/bot_vision/headless_capture/capture_headless.js` existe et le flux attendu est :

```text
capture_headless.js -> vision_inbox -> vision_bot/OCR -> vision_processed/vision_outbox -> desk_bridge -> desk/snapshots -> Desk Pro
```

Le profil exemple actuel ne couvre que `tradingview / BTCUSDT.P / H1`. Avant toute retention ou suppression, il faut verifier l'etat reel de la capture et de l'ingestion.

## 4_MASTER_PROJECT_PLAN

1. Documenter le chantier et ses invariants.
2. Proposer une matrice P0 de pages a capturer.
3. Produire un plan de smoke/dry-run non destructif.
4. Formaliser le nommage et le classement.
5. Formaliser la checklist ingestion/extraction.
6. Formaliser la retention et l'archive.
7. Donner un runbook de revue humaine.
8. Ne modifier aucun index global hors entree inbox demandee.

## 6_FINAL_TARGET

Livrer un chantier court produisant :

1. une matrice des pages a screenshot ;
2. un smoke/dry-run non destructif ;
3. une verification ingestion complete ;
4. un contrat de nommage/classement ;
5. une politique de conservation : 1 a 2 screenshots par jour par page screener ;
6. une procedure d'archive/compression/suppression des vieux screenshots.

## 7_CANONICAL_STATE

Etat etabli le 2026-05-19 sur `admin-trading` :

- repo remote localise : `/opt/trading` ;
- branche creee depuis `origin/sot/mainline` : `go/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01` ;
- `modules/bot_vision/headless_capture/capture_headless.js` present ;
- `profiles.example.json` contient une seule entree : `tradingview / BTCUSDT.P / H1` ;
- timer systemd `bot-vision-headless-capture.timer` : enabled + active ;
- service `bot-vision-headless-capture.service` : failed ;
- cause observee : `Cannot find module 'playwright'` ;
- `node_modules/playwright` absent dans le module ;
- aucun restart service, aucune installation et aucune capture executee dans ce passage.

Inventaire read-only `/srv/sftp/shared_files/shared` :

| Surface | Etat observe |
| --- | --- |
| `vision_inbox` | 77 fichiers JSON, 0 PNG, 0 `.uploading`, 77 fichiers < 1 KB, 0 zero-byte |
| `vision_processed` | 0 fichier |
| `vision_outbox` | 0 fichier |
| `inbox` | 0 fichier |
| `desk/snapshots` | dossier manquant |
| `desk_pro/latest` | 5 fichiers, dont 4 JSON |
| `desk/snapshots/latest.json` | manquant |
| `desk/snapshots/history.jsonl` | manquant |
| `desk_pro/latest/latest.json` | manquant |
| `desk_pro/latest/history.jsonl` | manquant |

Interpretation : smoke ingestion complet bloque tant que les captures PNG ne sont pas produites et tant que la dependance Playwright n'est pas restauree.

## 8_VALIDATED_PLAN

Plan valide pour ce chantier : doc-first, read-only inventory, smoke capture uniquement apres validation humaine et correction de dependance.

## 10_SELECTED_SETUP

Fichiers crees :

```text
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01/00_INITIAL_PROJECT_DOC.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01/10_PAGE_SELECTION_MATRIX.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01/20_SMOKE_DRY_RUN_PLAN.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01/30_NAMING_CLASSIFICATION_CONTRACT.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01/40_INGESTION_EXTRACTION_CHECKLIST.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01/50_RETENTION_ARCHIVE_POLICY.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01/60_HUMAN_REVIEW_RUNBOOK.md
docs/index/inbox/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01.md
```

## 11_KEY_DECISIONS

- Ne pas modifier `profiles.example.json` dans ce passage, car le timer actif l'utilise deja.
- Ne pas installer Playwright dans ce passage.
- Ne pas relancer systemd.
- Ne pas supprimer, compresser ou archiver de fichiers.
- Toute retention future doit produire un manifest avant suppression.

## 12_INVARIANTS

- Pas de suppression destructive au premier passage.
- Pas de lecture `.env`.
- Pas de token TradingView, Telegram ou API affiche.
- Pas de trade.
- Pas de restart service sans instruction explicite.
- Dry-run d'abord.
- Tout changement de politique d'archive doit ecrire un manifest avant suppression.
- Les index globaux ne sont pas modifies sauf demande explicite.

## 15_REMAINING_GAP

- Dependances Playwright absentes cote module headless.
- Service capture actuellement failed.
- Aucun PNG present dans `vision_inbox` lors de l'inventaire.
- `desk/snapshots` et ses fichiers `latest/history` manquent.
- Ingestion OCR/processed/outbox non prouvee.
- Profil 3 pages P0 non applique au runtime.
- Retention non executee.

## 16_TODO

1. Faire valider humainement la correction de dependance Playwright.
2. Apres validation, executer un smoke capture non destructif sur une seule page.
3. Verifier sidecar JSON + PNG + taille + dimensions.
4. Verifier ingestion `vision_processed` / `vision_outbox`.
5. Verifier propagation `desk/snapshots/latest.json`.
6. Appliquer ensuite la matrice P0 3 pages si le smoke est PASS.
7. Produire un manifest retention dry-run avant toute archive ou suppression.

## 17_RESUME_POINT

Reprendre par :

```text
GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01
Etape suivante: corriger dependance Playwright avec validation humaine, puis smoke capture non destructif sur 1 page.
```

## Verdict courant

`BLOCKED_WITH_REASON_PLAYWRIGHT_MISSING_NO_PNG_INGESTION_NOT_PROVEN`

