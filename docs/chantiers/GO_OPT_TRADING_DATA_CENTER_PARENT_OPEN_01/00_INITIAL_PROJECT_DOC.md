---
doc_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
parent_go_id: null
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
PF_ID: PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
MASTER_TARGET_ID: MT_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: null
BUNDLE_TARGET: null
NEXT_ATTACH_TARGET: null
NEXT_GO: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01
topic_keys:
  - opt-trading
  - data_center
  - producer_contracts
  - consumer_contracts
  - normalized_registry
  - master_project_plan
links:
  - docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01_MASTER_PROJECT_PLAN_CREATION_RULE_01.md
  - docs/index/GO_INDEX.md
  - docs/index/REPRISE.md
  - docs/index/inbox/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01.md
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Data Center opérationnel : producteurs et consommateurs partagent les mêmes contrats de données normalisées, stockées, versionnées et redistribuables. La règle centrale est :

```text
producer <> registry data <> consumer <> registry data <> producer
```

Producteurs identifiés : `derivatives_collector`, `collector_binance_spot`, `collector_coingecko`, futurs collecteurs Telegram/Vision/Webhook.

Consommateurs identifiés : `PF_DESK_PRO`, `PF_STRATEGY_FRAMEWORK_REGISTRY`, `PF_PERF_ENGINE_TRADING_LAB`, `PF_TELEGRAM_SCREENER`, `PF_TELEGRAM_INGESTION`, `PF_GOOGLE_SHEETS_CONSUMER`, `PF_LOCALCMS_COCKPIT`.

Le Data Center n'est pas une base de données unique. C'est le registre normalisé commun qui découple producteurs et consommateurs sans couplage direct.

## 2_INITIAL_PROJECT_DOC

Ce document ouvre le parent canonique `PF_DATA_CENTER` pour la première fois.

Il fige la structure de continuité du parent : `1_MASTER_TARGET`, `4_MASTER_PROJECT_PLAN`, `CLOSE_GATE_MASTER_TARGET`, rattachement à `PF_DATA_CENTER` et `MPP_DATA_CENTER_NORMALIZED_REGISTRY`.

Il ne ferme pas le parent. Il ne modifie pas les index globaux.

## 3_INITIAL_NEED

`PF_DATA_CENTER` est référencé dans `PRODUCT_FINAL_SURFACE_REGISTRY_01.md` comme surface finale P1 avec statut "à créer / promouvoir". `REPRISE.md` confirme que la reprise attendue est : **ouvrir parent Data Center normalisé**.

Aucun dossier chantier ni document parent n'existait pour ce produit avant cette ouverture.

L'ouverture est nécessaire avant tout child GO d'implémentation afin que les child GOs puissent être rattachés (GO_CHILD_ATTACHED_TO_PARENT) à un parent canonique réel.

## 4_MASTER_PROJECT_PLAN

`MPP_DATA_CENTER_NORMALIZED_REGISTRY`

1. **Contrats producer** : définir le format, le schéma, la validation et les règles d'écriture pour chaque producteur (derivatives_collector, binance_spot, coingecko, futurs collecteurs).
2. **Contrats consumer** : définir le format de lecture, la latence acceptable, les endpoints ou paths d'accès, les règles de fallback pour chaque consommateur.
3. **Normalisation des schémas data** : formaliser les schémas trading normalisés — events, metrics, positions, signals, OI, funding, liquidations, long/short — avec types, unités et coverage/gap explicites.
4. **Registre commun de stockage** : implémenter la structure `data/data_center/` avec `raw/`, `normalized/`, `latest.json`, `manifest.json`, `status.json`, `events.jsonl`, `errors.jsonl`, `cache/by_symbol/`.
5. **Versionnage datasets/events** : déclarer `schema_version` dans chaque artefact normalisé, prévoir migration paths et rétrocompatibilité minimale.
6. **Tests de compatibilité** : valider les contrats producer et consumer par tests smoke ou contractuels en CI local ; aucun contrat n'est livrable sans test.
7. **Lecture surfaces** : fournir read-only depuis le Data Center à chaque surface cible — `PF_DESK_PRO`, `PF_STRATEGY_FRAMEWORK_REGISTRY`, `PF_PERF_ENGINE_TRADING_LAB`, `PF_TELEGRAM_SCREENER`, `PF_TELEGRAM_INGESTION`, `PF_GOOGLE_SHEETS_CONSUMER`, `PF_LOCALCMS_COCKPIT`.
8. **Documentation reprise** : documenter les gaps, la qualité, la latence, les couvertures manquantes et le point de reprise pour chaque consommateur.

## 5_GO_PLAN

Chantier parent structurel. Cette ouverture est doc-first : aucun runtime modifié.

Sous-GO proposés (à ouvrir séquentiellement selon priorité opératoire) :

| GO_ID | Cible |
|---|---|
| `GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01` | Définir et formaliser les contrats producers |
| `GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01` | Définir et formaliser les contrats consumers |
| `GO_OPT_TRADING_DATA_CENTER_CHILD_SCHEMA_NORMALIZATION_01` | Normaliser les schémas data trading |
| `GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01` | Implémenter `data/data_center/` et son layout |
| `GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_TESTS_01` | Tests de compatibilité contractuelle |
| `GO_OPT_TRADING_DATA_CENTER_CHILD_SURFACE_READER_DESKPRO_01` | Lecture Desk Pro depuis Data Center |

Premier child recommandé : `GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01`.

## 6_FINAL_TARGET

Livrable de cette ouverture : un parent canonique `GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01` structuré avec `1_MASTER_TARGET`, `4_MASTER_PROJECT_PLAN` et `CLOSE_GATE_MASTER_TARGET` déclarés, rattaché à `PF_DATA_CENTER` et `MPP_DATA_CENTER_NORMALIZED_REGISTRY`, prêt à recevoir les child GOs d'implémentation.

## 7_CANONICAL_STATE

- `PF_DATA_CENTER` dans `PRODUCT_FINAL_SURFACE_REGISTRY_01.md` comme surface finale P1 "à créer / promouvoir".
- `GO_OPT_TRADING_DATA_CENTER_PARENT_01` n'existait pas avant cette ouverture ; ce document en est l'acte de création.
- `market_metrics.v1` est le premier contrat producer identifié dans `GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01` — il sera l'un des contrats producers du Data Center.
- `derivatives_collector` et `collector_binance_spot` sont des producteurs de données éprouvés mais sans contrat Data Center formalisé.
- Aucun registre de stockage commun `data/data_center/` n'existe dans le repo.
- Les surfaces consommatrices (`Desk Pro`, `Perf`, `Sheets`, `Telegram`) n'ont pas de lecture unifiée depuis un registre commun.
- `GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01` est le parent le plus proche ; il produit `market_metrics.v1` qui deviendra un contrat producer du Data Center.

## 8_VALIDATED_PLAN

Plan validé pour cette ouverture :
- créer uniquement les documents de structure du parent ;
- ne pas modifier le runtime ;
- ne pas écrire dans les index globaux (GO_INDEX, ACTIVE_STREAMS, REPRISE) sauf si modification réelle de l'horizon ;
- créer l'entrée inbox locale courte ;
- noter le chemin de bundle/patch pour transport futur.

## 9_SELECTED_SOLUTION

Le Data Center est un registre normalisé de transit, pas une base de données unique. Le découplage producer/consumer est la contrainte architecturale centrale. Chaque contrat doit être déclaré, versionné et testé indépendamment.

`market_metrics.v1` (défini dans GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01) est adopté comme premier contrat producer de référence pour le Data Center.

## 10_SELECTED_SETUP

Structure de stockage cible :

```text
data/data_center/
  <producer_family>/
    raw/
    normalized/
    latest.json          <- market_metrics.v1 ou équivalent normalisé
    manifest.json
    status.json
    events.jsonl
    errors.jsonl
    cache/
      by_symbol/<SYMBOL>.json

data/data_center/_registry/
  producers.json         <- liste des producers actifs, schéma version, dernier write
  consumers.json         <- liste des consumers actifs, format attendu, dernier read
  schema_versions.json   <- mapping schema_version -> spec
```

## 11_KEY_DECISIONS

- Le chantier est parent structurel ; aucun runtime modifié à l'ouverture.
- `data/data_center/` est le layout canonique cible.
- `market_metrics.v1` est le premier contrat producer de référence.
- Les child GOs d'implémentation seront `GO_CHILD_ATTACHED_TO_PARENT` rattachés à ce parent.
- Pas de fermeture parent avant que `CLOSE_GATE_MASTER_TARGET` soit satisfait.

## 12_INVARIANTS

- Ne pas fermer le parent à l'ouverture.
- `GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN` — permanent.
- Aucun ordre live.
- Aucune écriture Google Sheets globale.
- Aucun Telegram live.
- Aucune ingestion DB active.
- Aucun refactor forcé des collectors existants vers un nouveau layout sans child GO dédié.
- Pas de modification des index globaux sauf si le master target ou l'horizon change réellement.

## 13_ESTABLISHED

- `PF_DATA_CENTER` identifié comme surface finale P1 dans `PRODUCT_FINAL_SURFACE_REGISTRY_01.md`.
- `MPP_DATA_CENTER_NORMALIZED_REGISTRY` référencé dans `GO_INDEX.md` et `REPRISE.md` comme plan maître cible.
- `market_metrics.v1` comme contrat de jonction collector/Desk Pro défini dans `GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01`.
- `derivatives_collector` et `collector_binance_spot` prouvés en runtime comme producteurs de données.
- La règle `producer <> registry data <> consumer` canonisée dans `GO_INDEX.md`, section `MASTER_PROJECT_PLAN_INDEX`.
- Règle de création structurée GO dans `MATRICE_DOC_OPS_MASTER_MATRIX_01_MASTER_PROJECT_PLAN_CREATION_RULE_01.md`.

## 14_HYPOTHESIS

À valider par les child GOs :
- `market_metrics.v1` peut être produit et stocké dans `data/data_center/` sans modifier le contrat existant vers Desk Pro.
- Les consommateurs peuvent lire depuis `data/data_center/` en read-only sans nécessiter de refactor profond.
- Le versionnage de schéma peut être introduit sans casser les exports JSONL existants.

## 15_REMAINING_GAP

- Aucun registre de stockage commun `data/data_center/` dans le repo.
- Contrats producer non formalisés.
- Contrats consumer non formalisés.
- Schema versioning absent.
- Tests de compatibilité contractuelle absents.
- Aucune surface ne lit depuis un Data Center centralisé.
- Coinglass confirmé comme `NOT_PROVEN_RUNTIME_ADAPTER` — son rôle producer reste conditionnel.

## 16_TODO

1. Ouvrir `GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01` — définir contrats producers.
2. Définir layout `data/data_center/` canonique.
3. Formaliser `market_metrics.v1` comme premier contrat producer.
4. Établir lecture Desk Pro depuis `data/data_center/` (child dédié).
5. Ouvrir tests de compatibilité contractuelle.

## 17_RESUME_POINT

Reprendre sur le premier child GO :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01
```

Ou, si priorité opératoire, commencer par la définition du layout `data/data_center/` dans un child `GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01` selon disponibilité.

---

## CLOSE_GATE_MASTER_TARGET

Le parent peut être fermé uniquement si toutes les conditions suivantes sont satisfaites :

```text
1. PF_DATA_CENTER utilisable :
   - au moins 2 surfaces consommatrices lisent des données normalisées depuis data/data_center/
   - lecture prouvée en dry-run ou smoke réel

2. Contrats producer :
   - au moins 2 producteurs avec contrats formalisés, schémas versionnés, testés

3. Contrats consumer :
   - au moins 2 consommateurs avec lecture prouvée depuis data/data_center/

4. Tests de compatibilité :
   - tests contractuels smoke passant en local ou CI

5. Documentation reprise :
   - gaps, qualité, latence et points de reprise documentés pour chaque consommateur actif

6. Aucun gap bloquant non documenté.
```

---

## BUNDLE / PATCH

Artefacts de transport prévus (à créer lors des child GOs d'implémentation) :

```text
bundles/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/
  TARGETS.md
  bundle_meta/target_card.json
  patches/<YYYYMMDD>_GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01_open.patch
```

Pour l'ouverture seule (ce document) :

```text
docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/patches/
  20260523_GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01_opening.patch
```
