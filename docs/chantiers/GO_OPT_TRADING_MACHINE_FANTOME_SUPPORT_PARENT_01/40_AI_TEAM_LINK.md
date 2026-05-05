---
doc_id: GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01_AI_TEAM_LINK
doc_type: link
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01
status: open
lifecycle_stage: link
topic_keys:
  - opt-trading
  - machine_parent
  - fantome
  - ai_team
  - link
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/00_START.md
point_de_reprise: "Lien etabli"
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/00_START.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/20_EXISTING_BRANCHES_INVENTORY.md
---

# GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01 — 40_AI_TEAM_LINK

## Lien vers le parent AI Team Architecture existant

Le parent `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` est deja un parent actif (KEEP_ACTIVE).
Il est rattache a la machine `fantome` via l'arbitrage `AI_TEAM + STRICT_WORKERS = fantome`.

```text id="ai_team_link"
Machine : fantome
Parent rattache : GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
Branche : GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
Dossier : docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/
Statut : KEEP_ACTIVE
```

## Contenu du parent AI Team

Le parent AI Team contient les documents suivants :

| Fichier | Description |
|---------|-------------|
| `00_cadrage.md` | Cadrage canonique complet du parent |
| `01_initial_project_doc.md` | Fiche de reference initiale du projet |
| `02_journal_technique.md` | Journal borne des actions executees |
| `03_decisions.md` | Decisions, exclusions, verdict, reprise |

## Instructions

```text id="ai_team_instructions"
1. NE PAS recréer le parent AI_TEAM.
2. Assigner AI_TEAM comme thread/parent lie a la machine fantome.
3. Traiter AI_TEAM comme chantier porte par la machine fantome.
4. Le contenu existant de AI_TEAM est la reference.
5. La reconciliation GO_CHILD_01 devra etablir le lien formel sans modifier AI_TEAM.
```

## Verdict

Lien etabli. Le parent AI Team est reference, non modifie.
AI_TEAM reste KEEP_ACTIVE et sera porte par la machine fantome.
