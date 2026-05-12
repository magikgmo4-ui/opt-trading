---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01
status: active
scope: doc-only
opened_at: 2026-05-12
base: sot/mainline
branch: go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01
parent_go: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/60_ADMIN_TRADING_PROBE_RESULTS.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/70_GATE_DECISION.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01/30_AFTER_STATE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01/10_SOURCE_STATE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01/20_PREREQUISITES_CHECK.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01/30_TMUX_IDE_PROBE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01/40_IDE_YML_DECISION.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01/50_GAPS_AND_NEXT_DECISION.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01/90_CLOSEOUT.md
  - docs/index/inbox/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01.md
---

# 00_GO_OPEN

## Identifiant

`GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01`

## Objectif

Qualifier `tmux-ide` et `ide.yml` sur `admin-trading:/opt/trading`, maintenant que la base Git est réalignée sur `sot/mainline`. Lire, vérifier, documenter — sans implémentation runtime non autorisée.

## Contexte établi

| Élément | État | Source | Preuve |
| --- | --- | --- | --- |
| PR #305 mergée | PASS | user 13_ESTABLISHED | ETAT_DECLARE |
| admin-trading:/opt/trading sur sot/mainline | PASS | GO_REALIGN_EXEC_01 | ETAT_DECLARE |
| SSH cursor-ai → admin-trading | PASS | 60_ADMIN_TRADING_PROBE_RESULTS.md, 2026-05-11 | ETAT_DECLARE |
| tmux 3.3a présent | PASS | 60_ADMIN_TRADING_PROBE_RESULTS.md | ETAT_DECLARE |
| node v18.20.4 présent | PASS | 60_ADMIN_TRADING_PROBE_RESULTS.md | ETAT_DECLARE |
| npm 9.2.0 présent | PASS | 60_ADMIN_TRADING_PROBE_RESULTS.md | ETAT_DECLARE |
| tmux-ide | ABSENT | 60_ADMIN_TRADING_PROBE_RESULTS.md, 2026-05-11 | ETAT_DECLARE |
| ide.yml | ABSENT | 60_ADMIN_TRADING_PROBE_RESULTS.md, 2026-05-11 | ETAT_DECLARE |
| db-layer | hors scope | invariants GO | ETAT_DECLARE |
| OpenClaw | hors scope | invariants GO | ETAT_DECLARE |

## Règles

- Ne pas toucher db-layer.
- Ne pas toucher OpenClaw.
- Ne pas modifier modules/.
- Ne pas modifier runtime.
- Ne pas installer tmux-ide sans gate explicite.
- Ne pas créer ide.yml final sans décision documentée.
- Lire, vérifier, documenter d'abord.

## Machine source

cursor-ai (Windows)

## Machine cible

admin-trading, répertoire `/opt/trading`

## Structure

| Fichier | Rôle |
| --- | --- |
| `10_SOURCE_STATE.md` | État Git et SSH au moment du GO |
| `20_PREREQUISITES_CHECK.md` | Re-probe prérequis live |
| `30_TMUX_IDE_PROBE.md` | Re-probe tmux-ide et npx |
| `40_IDE_YML_DECISION.md` | Décision ide.yml |
| `50_GAPS_AND_NEXT_DECISION.md` | Gaps et recommandation suivante |
| `90_CLOSEOUT.md` | Verdict PASS / PARTIAL_PASS / FAIL |

## Critères de verdict

| Verdict | Condition |
| --- | --- |
| PASS | tmux-ide disponible + ide.yml qualifiable sans runtime |
| PARTIAL_PASS | prérequis OK mais tmux-ide absent ou ide.yml absent |
| FAIL | Git non propre, SSH échoue, ou prérequis cassés |
