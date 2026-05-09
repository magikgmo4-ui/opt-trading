---
doc_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01_40_SCORING_P0_P1_P2
doc_type: chantier/scoring
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01
status: active
scope: doc-only
links:
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/01_FULL_RESPONSE_CAPTURE.md
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/02_REMAINING_GAP.md
---

# 40_SCORING_P0_P1_P2

## Grille retenue

| Niveau | Definition | Exemples |
| --- | --- | --- |
| `P0` | action requise ou risque de divergence canonique | PR ouverte bloquant une suite, branche active sans closeout critique, preuve Git contradictoire |
| `P1` | verification requise avant travail suivant | GO actif sans reprise claire, branche sans PR mais doc presente, etat machine a confirmer |
| `P2` | surveillance non bloquante | doc recente a suivre, branche stale reference, closeout deja passe sans action immediate |

## Regles d'usage

- `P0` doit etre rare et justifie par une preuve concrete.
- `P1` couvre les incertitudes operatoires reelles.
- `P2` ne doit pas submerger le cockpit.
- chaque item doit citer sa source et le type de preuve.

## Priorisation de sortie

Le dashboard doit :
1. afficher les `P0` en premier ;
2. limiter les `P1` a ce qui conditionne l'action suivante ;
3. releguer les `P2` a une section de surveillance.

## Anti-bruit

Le prompt doit refuser :
- les listes longues sans classement ;
- les alertes sans source ;
- les priorites gonflees artificiellement ;
- les recommandations definitives sans preuve.
