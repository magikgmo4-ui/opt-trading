---
doc_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01_50_MACHINE_STATE_RULES
doc_type: chantier/machine_state_rules
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01
status: active
scope: doc-only
links:
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/02_REMAINING_GAP.md
---

# 50_MACHINE_STATE_RULES

## Regle canonique

Un etat machine ne doit jamais etre presente comme verifie sans preuve explicite.

## Taxonomie obligatoire

| Etiquette | Definition | Condition |
| --- | --- | --- |
| `ETAT_DECLARE` | etat issu d'une doc, d'un closeout ou d'un point de reprise | pas de preuve technique en direct |
| `ETAT_VERIFIE` | etat prouve par commande, log, sortie Git ou evidence technique datee | preuve explicite disponible |
| `HYPOTHESE` | inference plausible mais non prouvee | doit rester formulee comme hypothese |

## Regles d'affichage

- toute machine doit avoir une etiquette d'etat ;
- `ETAT_VERIFIE` exige une source de preuve ;
- `HYPOTHESE` doit etre visible, jamais masquee ;
- en cas de doute, preferer `ETAT_DECLARE` ou `HYPOTHESE`.

## Machines a afficher

| Machine | Role |
| --- | --- |
| `admin-trading` | runtime trading / services |
| `student` | lab / ollama / tests |
| `db-layer` | openclaw / backend / data |
| `cursor-ai` | orchestration IDE Windows |
| `android / termux / tmux` | acces distant / shells |

## Exemples

| Cas | Sortie correcte |
| --- | --- |
| closeout merge sans commande recente | `ETAT_DECLARE` |
| log technique recent ou commande reelle | `ETAT_VERIFIE` |
| deduction a partir d'un pattern documentaire | `HYPOTHESE` |

## RISKS

- À qualifier.
