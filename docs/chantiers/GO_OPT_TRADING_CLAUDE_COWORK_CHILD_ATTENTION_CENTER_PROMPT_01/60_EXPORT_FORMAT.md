---
doc_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01_60_EXPORT_FORMAT
doc_type: chantier/export_format
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01
status: active
scope: doc-only
---

# 60_EXPORT_FORMAT

## Format cible

Le Live Artifact peut produire un export journalise au format :

```text
reports/YYYY-MM-DD_ATTENTION_CENTER_SUMMARY.md
```

## Regle

Cet export est seulement defini ici comme format cible.

- il n'est pas ecrit automatiquement ;
- il n'entre pas dans le repo sans GO explicite ;
- il reste une trace de travail read-only / synthese, pas une source canonique.

## Structure recommandee

```markdown
# ATTENTION_CENTER_SUMMARY - YYYY-MM-DD

## 7_CANONICAL_STATE
- scope du run
- source canonique principale
- date du snapshot / refresh

## ATTENTION_NOW
### P0
- item
### P1
- item
### P2
- item

## GO_ACTIVE
- GO_ID / statut / source / prochaine action

## BRANCHES_AND_PRS
- PR ouvertes
- branches a verifier

## MULTI_MACHINE_VIEW
- machine / ETAT_DECLARE ou ETAT_VERIFIE ou HYPOTHESE / source

## NEXT_GO_RECOMMENDATION
- une seule action prioritaire

## SOURCES
- fichiers / PR / branches / docs consultes
```

## Champs minimaux

- date
- source principale
- priorites `P0 / P1 / P2`
- recommendation unique
- liste des sources
- niveau de preuve machine
