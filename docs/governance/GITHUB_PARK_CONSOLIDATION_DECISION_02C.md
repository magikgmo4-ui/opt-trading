---
doc_id: OPT_TRADING_GITHUB_PARK_CONSOLIDATION_DECISION_02C
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
  - llm_wiki
surface: repo
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02.md
  - docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02B.md
---

# GITHUB_PARK_CONSOLIDATION_DECISION_02C

## Objet

Addendum de gouvernance pour figer la ligne de décision sur la lane `Llm-wiki` / `Llm-wiki-minimal`.

---

## Validation reçue

Validation utilisateur explicite :

- `Llm-wiki` = désuet
- conserver `Llm-wiki-minimal`

---

## Décision consolidée

### `Llm-wiki`
Décision mise à jour :
- `FREEZE_LEGACY_OBSOLETE`
- lane désuète
- aucune continuité active
- aucune promotion comme lane documentaire utile du parc

### `Llm-wiki-minimal`
Décision confirmée :
- `KEEP_PRECONSOLIDATION`
- lane conservée pour la pré-consolidation documentaire
- repo utile du parc actif

---

## Effet sur la matrice du parc

La matrice consolidée devient :

| Repo | Décision consolidée |
|---|---|
| `opt-trading` | KEEP_CANONICAL_EXECUTION |
| `openclaw` | KEEP_CANONICAL_GOVERNANCE |
| `localcms` | KEEP_PRODUCT_CONSUMER |
| `hf_trading` | KEEP_LAB_BOOTSTRAP |
| `Llm-wiki-minimal` | KEEP_PRECONSOLIDATION |
| `Llm-wiki` | FREEZE_LEGACY_OBSOLETE |
| `Magikgmo` | FREEZE_LEGACY_OBSOLETE |
| `algo_hf` | FREEZE_LEGACY_OBSOLETE |

---

## Ce qui est validé à partir de cet addendum

1. `Llm-wiki` n’est plus seulement gelé ou à réaffecter : il est classé legacy obsolète.
2. `Llm-wiki-minimal` est confirmé comme la seule lane conservée sur ce périmètre.
3. Aucun chantier actif ne doit repartir de `Llm-wiki`.
4. Une récupération future éventuelle sur `Llm-wiki` ne pourra être qu’une extraction patrimoniale ciblée.

---

## Verdict

**PASS — addendum validé**

## RISKS

- À qualifier.
