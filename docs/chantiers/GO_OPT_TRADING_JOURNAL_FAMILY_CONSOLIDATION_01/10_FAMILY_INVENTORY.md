---
doc_id: GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01_FAMILY_INVENTORY
doc_type: family_inventory
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - journal
  - inventory
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_JOURNAL_FAMILY_CONSOLIDATION_01/00_INITIAL_PROJECT_DOC.md
---

# 10_FAMILY_INVENTORY

## Baseline family

| Module | Baseline current | Registry | Famille normalized |
| --- | --- | --- | --- |
| `journal_de_bord` | non present | non verifie dans registry modules | `journal` historique |
| `journal_engine` | oui | absent | `journal` |

Preuves baseline:

- `13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv` ligne 39: `journal_engine,functional_candidate,no,review_missing_registry,journal`
- aucune entree `journal_de_bord` dans la baseline courante normalisee

## Vue d'ensemble

| Surface | Etat constate | Role constate | Statut retenu |
| --- | --- | --- | --- |
| `modules/journal_de_bord/` | absente du repo | ancienne surface operateur historique | retiree / legacy hors parc courant |
| `modules/journal_engine/` | presente | moteur de journalisation structuree, wrappers actifs | survivant canonique documentaire + moteur actif |

## Detail `journal_de_bord`

Le GO ne trouve aucun dossier `modules/journal_de_bord/` dans le checkout courant.

Les preuves canoniques recentes indiquent :

- `docs/governance/REPO_ROOT_POLICY.md` : `modules/journal_de_bord/` supprime comme outillage operatoire obsolete
- plusieurs closeouts et realignments documentent aussi son absence du repo

Conclusion:

- `journal_de_bord` n'est plus une surface runtime utile du parc courant
- la famille ne peut plus etre lue comme coexistence active entre deux modules presents

## Detail `journal_engine`

- `modules/journal_engine/app/journal_engine.py`
  - agrege `decision`, `risk`, `execution`, `position`, `perf`
  - construit des entrees `DESK_STATE_UPDATE`
  - derive `desk_state` (`ACTIVE_LONG_CANDIDATE`, `ACTIVE_SHORT_CANDIDATE`, `WATCHLIST`, `BLOCKED`, `INACTIVE`)
- `modules/journal_engine/scripts/cmd.sh`
  - expose `status`, `sample`, `build`, `export`, `explain`
- `README.md`
  - positionne le module comme system of record du Desk Pro

## Nature de la famille

La famille `journal` n'est plus un couple complementaire vivant.

Etat courant retenu :

- `journal_de_bord` = surface historique retiree
- `journal_engine` = unique survivant fonctionnel du parc courant

## Inventaire decisionnel

- l'audit historique voyait une dualite potentielle a clarifier
- le repo courant montre une resolution deja engagee par retrait de `journal_de_bord`
- le vrai travail restant ne porte pas sur une fusion entre deux modules vivants, mais sur l'alignement documentaire/registry autour de `journal_engine`
