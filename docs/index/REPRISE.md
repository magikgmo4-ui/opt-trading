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
updated_at: 2026-04-20
links:
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/governance/JOURNAL_HIERARCHY.md
---

# REPRISE — opt-trading

## Point de reprise

Base de pilotage active retenue pour `opt-trading` :

- périmètre = **12 GO non clos uniquement** (`active` / `open`)
- canon décisionnel = **repo `opt-trading`**
- bundles zip = **supports secondaires** de lecture, transfert ou exécution IDE
- exclusion explicite = `pass` et `reference` hors exécution courante

## Runtime (hors matrice active)

- runtime continuity pointer :
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/03_decisions.md

- état télécommande distante (figé) :
  - implémentation non stabilisée (verdict PARTIAL)
  - prochaine reprise sur tranche minimale lecture / statut / confirmation

## Sources canoniques

- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/GO_INDEX.md`

## Règle d’exécution

- **Source canonique principale** : repo `opt-trading`
- **Bundles zip** : accélérateurs de lecture / transfert / exécution IDE
- **Présence dans le repo** : les bundles et supports listés ici sont des noms de supports secondaires ; ils peuvent être absents du repo (non trackés)
- **Interdiction de dérive** : un bundle zip ne remplace jamais l’état réel du repo
- **Hiérarchie journal** : `journal.md` = brut vivant ; `journal/index/*` = dérivé ; `journal/canon/*` = archive (voir `docs/governance/JOURNAL_HIERARCHY.md`)
- **Liste active à piloter** : strictement les 12 GO ci-dessous

## Matrice de reprise canonique

| GO | status | priority | repo canonical refs | supports secondaires (noms) | etat etabli | gap restant | next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` | open | P0 | `docs/governance/MATRICE_DOC_OPS_MASTER_PLAN_01.md`; `docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/01_cadrage_parent.md` | Aucun bundle canonique | Plan maître complet ancré ; parent dédié ouvert pour fusion gouvernante | La matrice unique finale n'existe pas encore comme surface canonique unique | **Produire la matrice maître unique à partir du recroisement produit -> parent -> GO -> Git** |
| `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01` | active | P0 | `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/03_decisions.md` | Aucun bundle canonique | Chantier parent ouvert pour réaligner la continuité index | Contradictions d’index + concurrence NEXT + hiérarchie journal à propager | **Exécuter LOT 1 : réaligner `docs/index/*` et déclasser `docs/next/NEXT_GO_CANDIDATES.md`** |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | active | P0 | `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_CADRAGE_01/00_cadrage.md` | `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01_bundle.zip`; `consolidation_targets_ide_bundle.zip` | Bundle préparé, cadrage ouvert | Validation machine cible / panes / repo réel non prouvée | **Exécuter `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`** |
| `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01` | active | P0 | `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/03_decisions.md` | `OPT_TRADING_OBSOLETE_RECLASS_AUDIT_BUNDLE.zip` | Parent ouvert (audit/qualification repo-first, doc-only, non destructif) | Matrice canonique à produire + plan de lots physiques futurs | **Produire la matrice (PHASE C) puis le plan de lots (PHASE D)** |
| `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01` | active | P1 | `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/03_decisions.md` | Aucun bundle canonique | Parent PHASE 2 LOT 3 ouvert ; carte humaine des surfaces publiée | Arbitrages de structure canonique à poursuivre selon écarts réels | **Consolider la carte des surfaces et ses points d’ancrage sans dupliquer `registry/*`** |
| `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01` | active | P1 | `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/03_decisions.md` | Aucun bundle canonique | Parent PHASE 2 LOT 4 ouvert ; politique racine posée | Arbitrages de reclassement racine encore ouverts | **Consolider les classes racine et les arbitrages documentés sans chevaucher la politique frontière** |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | active | P1 | `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01/03_decisions.md` | Aucun bundle canonique | Parent PHASE 3 LOT 5 ouvert ; fiches status courtes publiées | Arbitrages de lignée encore ouverts sur plusieurs familles mixtes | **Consolider survivant/transition/legacy/archive en gap-only** |
| `GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01` | active | P1 | `docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/03_decisions.md` | Aucun bundle canonique | Parent PHASE 3 LOT 6 ouvert ; scope/exception clarifiés dans `registry/README.md` | Couverture déclarative à consolider sans dérive doctrinale | **Poursuivre l’alignement scope registry via la source canonique unique** |
| `GO_GIT_PROGRESSIVE_MIGRATION_START_13` | active | P1 | `docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md` | `zip_repos_audit_bundle.zip`; `zip_repos_audit_synthese_complete.md`; `zip_repos_audit_synthese_complete.json`; `zip_docs_line_reading_complete.md` | Dossier minimal ouvert pour GO actif | Suite autonome encore insuffisamment explicitée | **Formaliser la suite opératoire dédiée du chantier de migration avant tout lot d’exécution** |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | open | P1 | `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md` | `reseau_ssh_physical_consolidation_bundle_01.zip` | Survivant canonique `reseau_ssh_step2` confirmé, `step1b` gardé comme prérequis intermédiaire | Preuve détaillée du survivant et classification complète de la famille encore incomplètes | **Exécuter l’audit détaillé de la famille réseau/ssh dans ce GO** |
| `GO_OPT_TRADING_JOURNAL_FULL_READING_03` | active | P2 | `docs/chantiers/GO_OPT_TRADING_JOURNAL_FULL_READING_03/00_cadrage.md`; `docs/chantiers/GO_OPT_TRADING_JOURNAL_FULL_READING_03/03_decision_freeze_after_block_15.md` | Aucun bundle dédié identifié | Lecture figée volontairement à `JOURNAL_MD_BLOCK_15`; `BLOCK_16` et `BLOCK_17` explicitement exclus de la base canonique courante | Couche humaine utile encore incomplète au-delà de `BLOCK_15`, sans arbitrage suffisant pour valider `BLOCK_16`/`BLOCK_17` | **Reprendre plus tard à `BLOCK_16` (ligne 4421) seulement si le chantier est rouvert explicitement** |
| `GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04` | active | P2 | `docs/chantiers/GO_OPT_TRADING_JOURNAL_CANON_INTENT_LAYER_04/00_cadrage.md` | Aucun bundle dédié identifié | Reprise de lecture orientée intention projet engagée | Vérification systématique de l’intention encore partielle | **Poursuivre la lecture de `journal.md` puis croiser brut / canon / intention projet** |
