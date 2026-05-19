---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_PLAYWRIGHT_RUNTIME_REPAIR_01
surface: ADMIN_TRADING
source_kind: canonical
updated_at: 2026-05-19
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Documenter et clore la reparation runtime Playwright du module `bot_vision_headless` sur `admin-trading`, apres validation humaine explicite, sans modifier les profils de capture ni la cadence systemd.

## 2_INITIAL_PROJECT_DOC

Document transporteur du chantier :

`docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_PLAYWRIGHT_RUNTIME_REPAIR_01/00_INITIAL_PROJECT_DOC.md`

## 3_INITIAL_NEED

Le chantier d'audit precedent a etabli que `bot-vision-headless-capture.service` etait bloque par l'absence du module Node `playwright` :

```text
playwright:MISSING
Cannot find module 'playwright'
```

Le timer `bot-vision-headless-capture.timer` etait deja enabled + active. La reparation devait donc rester locale au runtime Node/Playwright et ne pas redemarrer systemd.

## 4_SCOPE

Inclus :

1. committer le chantier audit doc-only precedent si non commit ;
2. creer la branche child runtime repair ;
3. verifier Node/npm et `npm run check` ;
4. installer la dependance Playwright et le browser Chromium apres validation humaine ;
5. executer un seul smoke manuel ;
6. verifier PNG, JSON sidecar, absence `.uploading`, ingestion et extraction ;
7. consigner le PASS dans un rapport doc-only.

Exclus :

- lecture `.env` ;
- restart manuel du service ou du timer ;
- modification de `profiles.example.json` ;
- ajout des trois pages P0 ;
- suppression volontaire de fichiers ;
- trade ;
- forcer l'ajout de `package-lock.json`.

## 7_CANONICAL_STATE

Etat etabli le 2026-05-19 sur `admin-trading` :

- repo : `/opt/trading` ;
- branche runtime repair active : `go/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_PLAYWRIGHT_RUNTIME_REPAIR_01` ;
- audit precedent commit : `203b1cc2c docs: audit bot vision screenshot lifecycle` ;
- Node : `v18.20.4` ;
- npm : `9.2.0` ;
- `modules/bot_vision/headless_capture/package.json` present ;
- `package-lock.json` cree par `npm install` mais ignore par `.gitignore` ;
- `npm run check` avant reparation : `playwright:MISSING` ;
- `npm install` : OK ;
- `npx playwright install chromium` : OK ;
- `npm run check` apres reparation : `playwright:OK` ;
- aucun restart manuel ;
- `profiles.example.json` non modifie ;
- aucun `.env` lu ;
- aucun trade.

## 8_VALIDATED_PLAN

Plan valide : reparation runtime Playwright + Chromium uniquement, puis smoke manuel unique avec :

```bash
BOT_VISION_OUT=/srv/sftp/shared_files/shared/vision_inbox npm run capture:example
```

Stop condition definie : stopper et rapporter si `npx playwright install chromium` demande des dependances systeme ou suggere `install-deps`.

Resultat : aucune demande `install-deps` observee.

## 10_SELECTED_SETUP

Fichiers crees pour ce rapport :

```text
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_PLAYWRIGHT_RUNTIME_REPAIR_01/00_INITIAL_PROJECT_DOC.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_PLAYWRIGHT_RUNTIME_REPAIR_01/10_REPAIR_EXECUTION_REPORT.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_PLAYWRIGHT_RUNTIME_REPAIR_01/20_SMOKE_RESULT.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_PLAYWRIGHT_RUNTIME_REPAIR_01/30_CLOSEOUT.md
docs/index/inbox/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_PLAYWRIGHT_RUNTIME_REPAIR_01.md
```

## 11_KEY_DECISIONS

- Garder `profiles.example.json` intact pendant cette reparation.
- Ne pas redemarrer systemd : le timer actif peut declencher naturellement apres correction runtime.
- Ne pas forcer l'ajout de `package-lock.json`, car il est ignore par `.gitignore` pour ce module.
- Reporter la validation `desk/snapshots` a un chantier separe si le bridge Desk n'est pas observe.
- Tester les pages P0 dans un profil smoke separe avant toute promotion runtime.

## 12_INVARIANTS

- Pas de lecture `.env`.
- Pas de restart manuel service/timer.
- Pas de modification `profiles.example.json`.
- Pas de modification `GO_INDEX`, `ACTIVE_STREAMS`, `REPRISE`, `BRANCH_STATE`.
- Pas de trade.
- Pas de suppression volontaire.
- Commit doc-only uniquement.

## 15_REMAINING_GAP

- `desk/snapshots` reste a valider separement.
- Les trois pages P0 ne sont pas activees dans le profil timer.
- Le PASS runtime local n'est pas un diff Git applicatif ; le repo garde seulement ce rapport doc-only comme trace durable.

## 16_TODO

1. Committer ce rapport doc-only.
2. Ouvrir le GO suivant : `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01`.
3. Creer un profil smoke separe non utilise par le timer pour `tv_btc_h1`, `tv_xau_h1`, `cg_btc_flow`.
4. Lancer une capture manuelle controlee.
5. Decider ensuite seulement si le profil runtime actif doit evoluer.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_PLAYWRIGHT_RUNTIME_REPAIR_01 = PASS runtime.
Action immediate: rapport doc-only cree, a committer.
Next: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01.
```

## Verdict courant

`PASS_PLAYWRIGHT_RUNTIME_REPAIR`
