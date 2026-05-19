---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01
surface: ADMIN_TRADING
source_kind: canonical
updated_at: 2026-05-19
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Tester les pages P0 du bot vision headless sur `admin-trading` avec un profil smoke separe, non utilise par le timer, sans modifier le profil runtime actif.

## 2_INITIAL_PROJECT_DOC

Document transporteur du chantier :

`docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01/00_INITIAL_PROJECT_DOC.md`

## 3_INITIAL_NEED

La reparation runtime Playwright est validee et documentee :

- audit screenshot lifecycle commit : `203b1cc2c` ;
- runtime repair record commit : `1777a721` ;
- `npm run check` : `playwright:OK` ;
- smoke BTC H1 initial : capture, ingestion et extraction prouvees.

Le besoin de ce GO est de tester les trois pages P0 sans brancher ces pages au timer permanent.

## 4_MASTER_PROJECT_PLAN

1. Creer la branche child P0 smoke.
2. Verifier l'etat Git et `npm run check`.
3. Creer `profiles.p0.smoke.local.json` comme profil separe.
4. Executer une capture manuelle unique avec ce profil.
5. Verifier par page : PNG, JSON sidecar, `.uploading`, ingestion et extraction.
6. Faire une revue humaine minimale de lisibilite.
7. Documenter les resultats et les bloqueurs.
8. Committer uniquement les docs et le profil smoke separe, si non ignore.

## 7_CANONICAL_STATE

Etat etabli le 2026-05-19 :

- repo : `/opt/trading` ;
- branche active : `go/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01` ;
- `profiles.example.json` non modifie ;
- profil smoke separe cree : `modules/bot_vision/headless_capture/profiles.p0.smoke.local.json` ;
- `profiles.p0.smoke.local.json` n'est pas ignore par `.gitignore` ;
- `npm run check` : `playwright:OK` ;
- aucun restart manuel service/timer ;
- aucune lecture `.env` ;
- aucune installation supplementaire ;
- aucun trade.

## 8_VALIDATED_PLAN

Commande smoke manuelle executee :

```bash
BOT_VISION_OUT=/srv/sftp/shared_files/shared/vision_inbox \
  npm run capture -- --profile profiles.p0.smoke.local.json --once
```

## 10_SELECTED_SETUP

Fichiers crees pour ce GO :

```text
modules/bot_vision/headless_capture/profiles.p0.smoke.local.json
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01/00_INITIAL_PROJECT_DOC.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01/10_P0_PAGE_MATRIX.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01/20_SMOKE_PROFILE_PLAN.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01/30_SMOKE_EXECUTION_RESULT.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01/40_HUMAN_REVIEW.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01/50_CLOSEOUT.md
docs/index/inbox/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01.md
```

## 11_KEY_DECISIONS

- Ne pas modifier `profiles.example.json`.
- Garder les pages P0 dans un profil smoke separe.
- Ne pas corriger `capture_headless.js` dans ce GO, meme si le timeout `networkidle` bloque deux pages.
- Ne pas promouvoir le profil P0 vers le timer tant que les trois pages ne passent pas.

## 12_INVARIANTS

- Pas de modification `profiles.example.json`.
- Pas de restart timer/service.
- Pas d'installation supplementaire.
- Pas de suppression, compression ou archive.
- Pas de lecture `.env`.
- Pas de trade.
- Pas de modification `GO_INDEX`, `ACTIVE_STREAMS`, `REPRISE`, `BRANCH_STATE`.

## 15_REMAINING_GAP

- `tv_xau_h1` timeout avant screenshot.
- `cg_btc_flow` timeout avant screenshot.
- La logique `waitUntil: networkidle` de `capture_headless.js` est probablement trop stricte pour certaines pages dynamiques.
- `desk/snapshots` reste hors scope et non valide dans ce GO.

## 16_TODO

1. Decider si un GO runtime separe doit assouplir le wait strategy pour les pages dynamiques.
2. Valider humainement une URL TradingView XAU stable.
3. Valider humainement une URL Coinglass stable pour le flow BTC.
4. Relancer un smoke P0 apres correction ou ajustement, toujours hors profil timer.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_P0_PAGE_SELECTION_SMOKE_01
Resultat: BTC H1 PASS complet, XAU H1 et Coinglass BLOCKED timeout networkidle.
Next: ajuster URLs/wait strategy dans un GO separe avant promotion runtime.
```

## Verdict courant

`BLOCKED_WITH_REASON_PARTIAL_P0_TIMEOUT_XAU_COINGLASS`
