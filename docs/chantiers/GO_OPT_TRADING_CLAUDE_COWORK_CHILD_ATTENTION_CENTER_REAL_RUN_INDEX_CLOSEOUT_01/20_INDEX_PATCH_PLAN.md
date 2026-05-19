---
doc_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_INDEX_CLOSEOUT_01_20_INDEX_PATCH_PLAN
doc_type: chantier/plan
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_INDEX_CLOSEOUT_01
status: active
scope: doc-only
---

# 20_INDEX_PATCH_PLAN

## Cibles de patch

| Surface | Action |
| --- | --- |
| `docs/index/GO_CLOSED_INDEX.md` | ajouter l'entree close/pass du GO `REAL_RUN` |
| `docs/index/GO_INDEX.md` | actualiser l'entree active `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` |
| `docs/index/REPRISE.md` | durcir la reserve sur la machine cible avant `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` |
| `docs/index/NEXT_GO_CANDIDATES.md` | poser explicitement la verification machine comme prerequis |
| `docs/index/ACTIVE_STREAMS.md` | aligner le flux TMUX sur le PASS du real run et la reserve machine |

## Regles de contenu

- ne pas ouvrir de nouveau flux OpenClaw
- ne pas changer la priorisation canonique P0/P1/P2
- ne pas creer de rattachement machine non prouve
- ne pas modifier les surfaces bundle ou runtime
- garder `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` comme prochain GO de reprise

## Formulation retenue

- closeout du real run: `PASS`
- prochain GO: `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`
- reserve obligatoire: `machine cible a verifier avant execution`
- borne de suite: `OpenClaw hors scope`
