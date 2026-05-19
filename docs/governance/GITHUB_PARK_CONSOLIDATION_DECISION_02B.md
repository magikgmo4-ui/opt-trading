---
doc_id: OPT_TRADING_GITHUB_PARK_CONSOLIDATION_DECISION_02B
doc_type: governance_decision_addendum
repo: opt-trading
project: opt-trading
go_id: GO_GITHUB_PARK_CONSOLIDATION_DECISION_02
status: validated
lifecycle_stage: governance
topic_keys:
  - github
  - repo_inventory
  - park
  - consolidation
  - addendum
  - legacy
surface: repo
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02.md
---

# GITHUB_PARK_CONSOLIDATION_DECISION_02B

## Objet

Addendum de validation utilisateur au cadrage de consolidation du parc GitHub.

Cet addendum complète `GITHUB_PARK_CONSOLIDATION_DECISION_02.md`.
Il fige explicitement le statut de deux repos encore ouverts dans la matrice précédente.

---

## Validation reçue

Validation utilisateur explicite :

- `Magikgmo` = désuet
- `algo_hf` = désuet
- ces deux repos relèvent d’un **ancien projet / ancienne version**

Cette validation remplace l’hypothèse précédente qui maintenait un audit trunk complet comme prérequis à la décision finale.

---

## Décision consolidée

### `Magikgmo`
Décision mise à jour :
- `FREEZE_LEGACY_OBSOLETE`
- ancien projet / ancienne version
- aucune continuité active
- aucun rôle canonique distinct retenu
- aucun nouveau chantier ne doit être ouvert dessus sauf récupération patrimoniale explicite

### `algo_hf`
Décision mise à jour :
- `FREEZE_LEGACY_OBSOLETE`
- ancien projet / ancienne version
- aucune continuité active
- aucun rôle canonique distinct retenu
- aucun nouveau chantier ne doit être ouvert dessus sauf récupération patrimoniale explicite

---

## Effet sur la matrice du parc

La matrice consolidée devient :

| Repo | Décision consolidée |
|---|---|
| `opt-trading` | KEEP_CANONICAL_EXECUTION |
| `openclaw` | KEEP_CANONICAL_GOVERNANCE |
| `localcms` | KEEP_PRODUCT_CONSUMER |
| `hf_trading` | KEEP_LAB_BOOTSTRAP |
| `llm_wiki_minimal` | KEEP_PRECONSOLIDATION |
| `Llm-wiki` | FREEZE_THEN_ARCHIVE_OR_REPURPOSE |
| `Magikgmo` | FREEZE_LEGACY_OBSOLETE |
| `algo_hf` | FREEZE_LEGACY_OBSOLETE |

---

## Ce qui est validé à partir de cet addendum

1. `Magikgmo` n’est plus un repo à auditer avant décision : il est classé legacy obsolète.
2. `algo_hf` n’est plus un repo à auditer avant décision : il est classé legacy obsolète.
3. Les GO d’audit dédiés ne sont plus des prérequis de gouvernance.
4. Une récupération future reste possible uniquement comme extraction patrimoniale ciblée.
5. Le parc actif utile reste centré sur :
   - `opt-trading`
   - `openclaw`
   - `localcms`
   - `hf_trading`
   - `llm_wiki_minimal`

---

## TODO mis à jour

Retirer des suites prioritaires :
- `GO_GITHUB_PARK_MAGIKGMO_AUDIT_03`
- `GO_GITHUB_PARK_ALGO_HF_AUDIT_03`

Remplacer par, seulement si nécessaire un jour :
- `GO_GITHUB_PARK_LEGACY_EXTRACTION_MAGIKGMO_03`
- `GO_GITHUB_PARK_LEGACY_EXTRACTION_ALGO_HF_03`

---

## Verdict

**PASS — addendum validé**

La décision de consolidation du parc est simplifiée :
`Magikgmo` et `algo_hf` sortent du périmètre actif et entrent dans le périmètre legacy obsolète.
