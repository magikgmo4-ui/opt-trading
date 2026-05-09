---
doc_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_INDEX_CLOSEOUT_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_INDEX_CLOSEOUT_01
status: active
scope: doc-only
opened_at: 2026-05-09
base: sot/mainline
branch: go/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_INDEX_CLOSEOUT_01
parent_go: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01
links:
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/90_CLOSEOUT.md
  - docs/index/GO_INDEX.md
  - docs/index/GO_CLOSED_INDEX.md
  - docs/index/REPRISE.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/inbox/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_INDEX_CLOSEOUT_01.md
---

# 00_GO_OPEN

## Identifiant

`GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_INDEX_CLOSEOUT_01`

## Objectif

Reporter dans les index globaux le closeout PASS du premier run reel de `OPT_TRADING_ATTENTION_CENTER_01`,
et poser le prochain GO de reprise sans ouvrir OpenClaw ni reassigner une machine sans preuve.

## Contexte etabli

- PR #274 du GO `GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01` est mergee dans `sot/mainline`.
- Le run reel du prompt Attention Center est clos en PASS.
- Le prochain GO recommande par les sources canoniques reste `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`.
- La machine cible de ce prochain GO n'est pas prouvee dans les sources lues.
- OpenClaw reste hors scope pour cette passe.

## Perimetre

- doc-only
- aucun runtime
- aucun `modules/`
- aucune execution OpenClaw
- aucune reassignment machine sans preuve
- modification globale limitee a `docs/index/*`

## Resultat attendu

- `GO_CLOSED_INDEX.md` reference le closeout PASS du real run
- `GO_INDEX.md`, `REPRISE.md`, `NEXT_GO_CANDIDATES.md` et `ACTIVE_STREAMS.md`
  alignent la reprise TMUX avec la reserve "machine cible a verifier avant execution"
- le prochain GO reste `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`
- OpenClaw est explicitement hors scope
