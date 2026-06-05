---
doc_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01_20_ATTENTION_CENTER_SPEC
doc_type: chantier/spec
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01
status: active
scope: doc-only
links:
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/01_FULL_RESPONSE_CAPTURE.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/02_REMAINING_GAP.md
---

# 20_ATTENTION_CENTER_SPEC

## Role

`OPT_TRADING_ATTENTION_CENTER_01` est un cockpit dynamique Claude Cowork destine a montrer :
- ce qui bloque ;
- ce qui attend validation ;
- ce qui est a reprendre ;
- les risques de divergence canonique ;
- les branches / GO / PR qui demandent attention.

## Question operatoire

```text
Qu'est-ce qui necessite mon attention maintenant, pourquoi, avec quelle preuve, et quelle est la prochaine action prioritaire ?
```

## Positionnement

| Surface | Role |
| --- | --- |
| Repo / docs / Git | verite canonique |
| Live Artifact Claude Cowork | cockpit dynamique |
| Claude Cowork | assistant de lecture / synthese |
| OpenClaw | orchestration locale / runtime, hors scope ici |

## Sections obligatoires

| Section | Contenu attendu |
| --- | --- |
| `ATTENTION_NOW` | liste P0/P1/P2 |
| `GO_ACTIVE` | GO actifs, checkpoints, prochaine action |
| `BRANCHES_AND_PRS` | PR ouvertes, branches a verifier, branches sans PR |
| `DOC_GOVERNANCE` | closeouts manquants, docs critiques recentes, gaps d'indexation visibles |
| `MULTI_MACHINE_VIEW` | etats machine avec preuve ou hypothese explicite |
| `NEXT_GO_RECOMMENDATION` | une seule prochaine action prioritaire, sourcee |

## Regles de sortie

- citer la source de chaque signal important ;
- ne jamais presenter une hypothese comme un fait verifie ;
- ne jamais proposer une ecriture automatique ;
- ne jamais presenter un merge comme obligatoire sans preuve Git reelle ;
- preferer un signal prioritaire unique a une liste floue.

## RISKS

- À qualifier.
