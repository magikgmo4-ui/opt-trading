---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01_IDENTITY_AUDIT
doc_type: audit
repo: opt-trading
project: opt-trading
module: ai_team_mvp
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01
parent_go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
status: draft_for_review
lifecycle_stage: audit
surface: chantier
source_kind: canonical_draft
updated_at: 2026-05-09
point_de_reprise: "Section Decision"
---

# 01_IDENTITY_AUDIT

## Gap documente

Source : `03_REMOTE_EXEC_STATE.md` — identity d'execution scindee entre `openclaw` (gateway/agent) et `ghost` (chemin SSH operationnel).

## Etat constate

| Element | Valeur |
|:--------|:-------|
| gateway OpenClaw | tourne sous `openclaw` |
| agent OpenClaw | tourne sous `openclaw` |
| chemin SSH operationnel | porte par `ghost` |
| `sudo -n openclaw -> ghost` | autorise hors agent |
| token gateway depuis `ghost` | mismatch (`unauthorized`) |

## Options

| Option | Description | Risque |
|:-------|:------------|:-------|
| A | Provisionner `openclaw` avec cle SSH directe vers `fantome` | Clef supplementaire a gerer |
| B | Officialiser wrapper `openclaw -> sudo -n -u ghost -> ssh ...` | Depend de `sudo` + ghost |
| C | Aligner token gateway pour permettre pilotage depuis `ghost` | Changement config OpenClaw |

## Decision

A arbitrer. Ne pas executer sans gate.

## RISKS

- À qualifier.
