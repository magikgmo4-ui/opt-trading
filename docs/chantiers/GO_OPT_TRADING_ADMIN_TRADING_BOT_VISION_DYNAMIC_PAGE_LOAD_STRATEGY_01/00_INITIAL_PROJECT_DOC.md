---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01
surface: ADMIN_TRADING
source_kind: canonical
updated_at: 2026-05-19
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Rendre `capture_headless.js` plus robuste pour les pages dynamiques en ajoutant une strategie de chargement configurable par profil, sans modifier `profiles.example.json` et sans redemarrer systemd.

## 2_INITIAL_PROJECT_DOC

Document transporteur du chantier :

`docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01/00_INITIAL_PROJECT_DOC.md`

## 3_INITIAL_NEED

Le smoke P0 precedent a valide `tv_btc_h1`, mais `tv_xau_h1` et `cg_btc_flow` ont bloque sur :

```text
page.goto: Timeout 30000ms exceeded, waiting until networkidle
```

Il faut permettre a chaque profil de choisir un `wait_until`, un timeout et une attente post-load, tout en conservant les defaults existants pour ne pas casser le timer actif.

## 4_SCOPE

Inclus :

1. creer une branche dediee ;
2. etendre `capture_headless.js` avec options par profil ;
3. conserver les defaults actuels ;
4. creer un profil smoke dynamique separe ;
5. lancer des captures manuelles uniquement ;
6. verifier artefacts, ingestion, extraction, `.uploading` et lisibilite ;
7. documenter PASS/BLOCKED proprement.

Exclus :

- modification de `profiles.example.json` ;
- promotion P0 vers le timer ;
- restart service/timer ;
- installation supplementaire ;
- suppression, compression ou archive ;
- lecture `.env` ;
- trade.

## 7_CANONICAL_STATE

Etat etabli le 2026-05-19 :

- branche active : `go/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01` ;
- base : `85661ed0 docs: smoke bot vision p0 screenshot pages` ;
- runtime Playwright : `playwright:OK` ;
- `capture_headless.js` supporte maintenant `wait_until`, `timeout_ms`, `post_load_wait_ms`, `screenshot_mode` ;
- defaults conserves : `networkidle`, `30000`, `3000`, `viewport` ;
- profil dynamic smoke separe cree : `modules/bot_vision/headless_capture/profiles.p0.dynamic.smoke.local.json` ;
- `profiles.example.json` non modifie ;
- aucun restart manuel ;
- aucun `.env` lu ;
- aucun trade.

## 8_VALIDATED_PLAN

Commande de test manuelle :

```bash
BOT_VISION_OUT=/srv/sftp/shared_files/shared/vision_inbox   npm run capture -- --profile profiles.p0.dynamic.smoke.local.json --once
```

## 10_SELECTED_SETUP

Fichiers crees ou modifies :

```text
modules/bot_vision/headless_capture/capture_headless.js
modules/bot_vision/headless_capture/profiles.p0.dynamic.smoke.local.json
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01/00_INITIAL_PROJECT_DOC.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01/10_TIMEOUT_FINDINGS.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01/20_LOAD_STRATEGY_CONTRACT.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01/30_IMPLEMENTATION_PLAN.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01/40_SMOKE_RESULT.md
docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01/50_CLOSEOUT.md
docs/index/inbox/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01.md
```

## 15_REMAINING_GAP

- XAU peut produire un PNG avec `domcontentloaded`, mais la capture observee est un spinner et n'est pas humainement lisible.
- Coinglass reste bloque avant screenshot, meme avec URL simplifiee et `domcontentloaded`.
- Un futur GO doit ajouter un skip/status JSON ou une strategie de capture apres timeout si l'on veut consigner proprement les pages non capturables sans perdre le reste du cycle.

## Verdict courant

`BLOCKED_WITH_REASON_DYNAMIC_LOAD_PARTIAL_XAU_SPINNER_COINGLASS_TIMEOUT`
