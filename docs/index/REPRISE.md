---
doc_id: OPT_TRADING_REPRISE
doc_type: reprise
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - reprise
  - continuity
surface: chantier
source_kind: canonical
updated_at: 2026-04-16
links:
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
---

# REPRISE — opt-trading

## Point de reprise

Base de pilotage active retenue pour `opt-trading` :

- périmètre = **6 GO non clos uniquement** (`active` / `open`)
- canon décisionnel = **repo `opt-trading`**
- bundles zip = **supports secondaires** de lecture, transfert ou exécution IDE
- exclusion explicite = `pass` et `reference` hors exécution courante

## Sources canoniques

- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/GO_INDEX.md`

## Règle d’exécution

- **Source canonique principale** : repo `opt-trading`
- **Bundles zip** : accélérateurs de lecture / transfert / exécution IDE
- **Présence dans le repo** : les bundles et supports listés ici sont des noms de supports secondaires ; ils peuvent être absents du repo (non trackés)
- **Interdiction de dérive** : un bundle zip ne remplace jamais l’état réel du repo
- **Liste active à piloter** : strictement les 6 GO ci-dessous

## Matrice de reprise canonique

| GO | status | priority | repo canonical refs | supports secondaires (noms) | etat etabli | gap restant | next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GO_GITHUB_PARK_AUDIT_EXPANSION_01` | open | P0 | `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md` | `github_park_file_role_cartography_01_bundle.zip`; `github_repo_inventory_full.json`; `github_repo_inventory_full.md`; `github_repo_inventory_from_zips_v2.md` | Cadrage validé, séquencement en couches établi | Consolidation incomplète sur rattachement branch / trunk / chantier | **Exécuter `GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01`** |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | active | P0 | `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md` | `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01_bundle.zip`; `consolidation_targets_ide_bundle.zip` | Bundle préparé, cadrage ouvert | Validation machine cible / panes / repo réel non prouvée | **Exécuter `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`** |
| `GO_GIT_PROGRESSIVE_MIGRATION_START_13` | active | P1 | `docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md` | `zip_repos_audit_bundle.zip`; `zip_repos_audit_synthese_complete.md`; `zip_repos_audit_synthese_complete.json`; `zip_docs_line_reading_complete.md` | Dossier minimal ouvert pour GO actif | Suite autonome encore insuffisamment explicitée | **Formaliser la suite opératoire dédiée du chantier de migration avant tout lot d’exécution** |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | open | P1 | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` | `reseau_ssh_physical_consolidation_bundle_01.zip` | Survivant canonique `reseau_ssh_step2` confirmé, `step1b` gardé comme prérequis intermédiaire | Preuve détaillée du survivant et classification complète de la famille encore incomplètes | **Exécuter l’audit détaillé de la famille réseau/ssh dans ce GO** |
| `GO_OPT_TRADING_JOURNAL_FULL_READING_03` | active | P2 | `docs/chantiers/GO_OPT_TRADING_JOURNAL_FULL_READING_03/00_cadrage.md` | Aucun bundle dédié identifié | Cadre inter-repos posé | Couche humaine vivante non réinjectée proprement | **Relire le journal canon complet et produire des blocs de validation humaine exploitables** |
| `GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04` | active | P2 | `docs/chantiers/GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04/00_cadrage.md` | Aucun bundle dédié identifié | Reprise de lecture orientée intention projet engagée | Vérification systématique de l’intention encore partielle | **Poursuivre la lecture de `journal.md` puis croiser brut / canon / intention projet** |

## Correspondance consolidée GO ↔ supports secondaires (noms)

### GitHub Park / inventaires
- `GO_GITHUB_PARK_AUDIT_EXPANSION_01`
  - `github_park_file_role_cartography_01_bundle.zip`
  - `github_repo_inventory_full.md`
  - `github_repo_inventory_full.json`
  - `github_repo_inventory_from_zips_v2.md`

### IDE / tmux
- `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`
  - `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01_bundle.zip`
  - `consolidation_targets_ide_bundle.zip`

### Migration / audits transverses
- `GO_GIT_PROGRESSIVE_MIGRATION_START_13`
  - `zip_repos_audit_bundle.zip`
  - `zip_repos_audit_synthese_complete.md`
  - `zip_repos_audit_synthese_complete.json`
  - `zip_docs_line_reading_complete.md`

### Réseau / SSH
- `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`
  - `reseau_ssh_physical_consolidation_bundle_01.zip`

### Journal
- `GO_OPT_TRADING_JOURNAL_FULL_READING_03`
  - aucun bundle dédié identifié

- `GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04`
  - aucun bundle dédié identifié

## Priorité opératoire retenue

### P0
- `GO_GITHUB_PARK_AUDIT_EXPANSION_01`
- `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`

### P1
- `GO_GIT_PROGRESSIVE_MIGRATION_START_13`
- `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`

### P2
- `GO_OPT_TRADING_JOURNAL_FULL_READING_03`
- `GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04`
