---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01
surface: ADMIN_TRADING
source_kind: canonical
updated_at: 2026-05-19
---

# 60_HUMAN_REVIEW_RUNBOOK

## Objectif

Encadrer la revue humaine avant toute modification runtime ou retention.

## Sequence de revue

1. Lire `00_INITIAL_PROJECT_DOC.md`.
2. Confirmer le blocage Playwright.
3. Autoriser ou refuser la correction de dependance.
4. Autoriser ou refuser une capture smoke unique sur `tv_btc_h1`.
5. Verifier les artefacts produits.
6. Autoriser ou refuser le passage P0 3 pages.
7. Autoriser ou refuser un dry-run retention manifest.
8. Autoriser ou refuser toute archive/compression/suppression ulterieure.

## Checklist PASS

| Verdict | Conditions |
| --- | --- |
| `PASS_INGESTION` | PNG + sidecar produits, downstream traite |
| `PASS_EXTRACTION` | OCR ou metadata non vide dans outbox |
| `PASS_NAMING` | nommage parseable et compatible downstream |
| `PASS_RETENTION_DRY_RUN` | manifest produit sans mutation |
| `BLOCKED_WITH_REASON` | une dependance, un dossier ou une preuve manque |

## Questions humaines ouvertes

- Quel symbole TradingView exact pour XAU H1 cote compte cible ?
- Quelle URL Coinglass publique doit representer `cg_btc_flow` ?
- Le timer doit-il etre temporairement stoppe pendant smoke manuel ?
- `desk/snapshots` doit-il etre cree par desk_bridge ou par une etape d'installation separee ?
- Les sidecars JSON orphelins du 2026-05-05 doivent-ils etre classes `rejected` plus tard ?

## Commandes autorisees sans validation supplementaire

- `git status`, `git diff`, `git log`, `git branch` ;
- `find` read-only sur les dossiers partages ;
- `stat` read-only ;
- `systemctl status/is-active/is-enabled/list-timers` ;
- lecture des fichiers suivis Git.

## Commandes necessitant validation explicite

- `npm install` ;
- `npx playwright install chromium` ;
- `systemctl restart/start/stop` ;
- execution de `capture_headless.js` ;
- modification de `profiles.example.json` ;
- creation, compression, deplacement ou suppression d'artefacts runtime ;
- tout scan qui ecrit un rapport hors repo.

## Verdict courant

`BLOCKED_WITH_REASON_PLAYWRIGHT_MISSING_NO_PNG_INGESTION_NOT_PROVEN`

