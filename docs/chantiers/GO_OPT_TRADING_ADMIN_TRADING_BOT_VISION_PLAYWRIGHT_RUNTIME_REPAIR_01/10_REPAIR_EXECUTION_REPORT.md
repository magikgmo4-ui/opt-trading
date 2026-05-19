---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_PLAYWRIGHT_RUNTIME_REPAIR_01
surface: ADMIN_TRADING
source_kind: execution_report
updated_at: 2026-05-19
---

# 10_REPAIR_EXECUTION_REPORT

## Objectif

Lever le blocage runtime `Cannot find module 'playwright'` du module `modules/bot_vision/headless_capture`, sans modifier les profils de capture et sans redemarrer le timer ou le service systemd.

## Pre-checks

Commandes et resultats observes sur `admin-trading` :

| Check | Resultat |
| --- | --- |
| `pwd` | `/opt/trading` |
| branche initiale audit | `go/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01` |
| audit doc-only non commit | 8 fichiers docs |
| commit audit | `203b1cc2c docs: audit bot vision screenshot lifecycle` |
| branche child | `go/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_PLAYWRIGHT_RUNTIME_REPAIR_01` |
| `node --version` | `v18.20.4` |
| `npm --version` | `9.2.0` |
| `package.json` | present |
| `package-lock.json` avant install | absent |
| `npm run check` avant install | `playwright:MISSING` |

Le `package.json` declarait deja :

```json
"dependencies": {
  "playwright": "^1.52.0"
}
```

## Validation humaine

Validation recue pour executer :

```bash
cd /opt/trading/modules/bot_vision/headless_capture
npm install
npx playwright install chromium
npm run check
```

Garde explicite : stopper si Playwright demande des dependances systeme ou suggere `install-deps`.

## Execution

### `npm install`

Resultat :

```text
added 2 packages, and audited 3 packages
found 0 vulnerabilities
```

Effets locaux :

- `node_modules` present dans `modules/bot_vision/headless_capture` ;
- `package-lock.json` cree par npm ;
- `package-lock.json` ignore par `.gitignore` ;
- aucun diff Git suivi.

Verification ignore :

```text
.gitignore:97:modules/bot_vision/headless_capture/package-lock.json
```

### `npx playwright install chromium`

Resultat : OK.

Telechargements observes :

```text
Chrome for Testing 148.0.7778.96 (playwright chromium v1223)
Chrome Headless Shell 148.0.7778.96 (playwright chromium-headless-shell v1223)
```

Aucune demande `install-deps` et aucune demande de dependances systeme n'ont ete observees.

Point d'attention : Playwright a automatiquement retire deux anciens caches browser avant installation :

```text
Removing unused browser at /home/ghost/.cache/ms-playwright/chromium-1217
Removing unused browser at /home/ghost/.cache/ms-playwright/chromium_headless_shell-1217
```

Cette suppression vient de Playwright pendant l'installation du browser ; aucune commande de suppression manuelle n'a ete lancee.

### `npm run check` apres install

Resultat attendu et observe :

```text
playwright:OK
```

## Etat Git apres reparation runtime

`git status --short --branch --untracked-files=all` :

```text
## go/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_PLAYWRIGHT_RUNTIME_REPAIR_01
```

`git diff --name-only` : aucune sortie.

`git ls-files --others --exclude-standard` : aucune sortie.

Interpretation : la reparation runtime est locale a l'environnement Node/Playwright. Le repo ne porte pas de diff applicatif, et le lock ignore ne doit pas etre force.

## Verdict

```text
playwright:MISSING -> playwright:OK
```

`PASS_PLAYWRIGHT_RUNTIME_REPAIR`
