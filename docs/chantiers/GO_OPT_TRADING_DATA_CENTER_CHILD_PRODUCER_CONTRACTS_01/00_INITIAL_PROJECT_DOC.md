---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
BUNDLE_TARGET: PRODUCER_CONTRACTS_FORMALIZED_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01
topic_keys:
  - opt-trading
  - data_center
  - producer_contracts
  - market_metrics
  - derivatives_collector
  - binance_spot
  - normalized_registry
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01/20_MARKET_METRICS_V1_CONTRACT.md
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01/30_STORAGE_AND_INGESTION_PLAN.md
  - modules/derivatives_collector/app/market_metrics_v1.py
  - modules/derivatives_collector/app/market_metrics_writer.py
  - modules/collector_binance_spot/src/collector_binance_spot/normalize.py
  - docs/index/inbox/GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01.md
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Data Center opérationnel : producteurs et consommateurs partagent les mêmes contrats normalisés via la règle `producer <> registry data <> consumer`. *(hérité de `GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01`)*

## 2_INITIAL_PROJECT_DOC

Premier child GO du parent Data Center. Objectif : formaliser les contrats producers pour chaque collecteur connu et définir le format du registre `producers.json`.

Ce chantier est **doc-first** : aucun runtime modifié.

## 3_INITIAL_NEED

Le parent `GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01` déclare comme premier axe du `4_MASTER_PROJECT_PLAN` : *définir le format, le schéma, la validation et les règles d'écriture pour chaque producteur*.

Les producers actuels (`derivatives_collector`, `collector_binance_spot`) ont des outputs connus mais aucun contrat Data Center formalisé. Ce GO produit ces contrats.

## 4_MASTER_PROJECT_PLAN — périmètre child

Sous-ensemble du MPP parent appliqué à ce child :

1. Définir le format canonique d'un producer contract Data Center.
2. Formaliser le contrat producer pour `derivatives_collector` (famille `derivatives`).
3. Formaliser le contrat producer pour `collector_binance_spot` (famille `spot`).
4. Définir le format du registre `data/data_center/_registry/producers.json`.
5. Cartographier les outputs existants vers les paths Data Center cibles.

## 5_GO_PLAN

Chantier doc-first. Livrables attendus dans ce dossier chantier :

| Fichier | Contenu |
|---|---|
| `00_INITIAL_PROJECT_DOC.md` | Ce document |
| `10_PRODUCER_CONTRACT_SPEC.md` | Format canonique d'un producer contract |
| `20_PRODUCER_INVENTORY.md` | Contrats des producers connus avec mapping Data Center |

## 6_FINAL_TARGET

Tous les producers connus (`derivatives_collector`, `collector_binance_spot`) ont un contrat Data Center formalisé dans `20_PRODUCER_INVENTORY.md`, avec :
- format canonique déclaré dans `10_PRODUCER_CONTRACT_SPEC.md` ;
- mapping output existant → path `data/data_center/<family>/` documenté ;
- registre `producers.json` spécifié.

## 7_CANONICAL_STATE

### `derivatives_collector`

Implémenté et opérationnel. Produit :

- `market_metrics.v1` via `modules/derivatives_collector/app/market_metrics_v1.py`
- Écrit via `market_metrics_writer.py` vers :
  - `data/collectors/derivatives/latest.json`
  - `data/collectors/derivatives/cache/by_symbol/<SYMBOL>.json`
  - `data/deskpro/inputs/market_metrics/latest.json`
  - `data/deskpro/inputs/market_metrics/by_symbol/<SYMBOL>.json`
- Providers : `bitget` (OI, funding, volume_futures — couverture partielle), `binance` (similaire)
- Metrics connues : `open_interest`, `funding_rate`, `volume_futures`, `long_short_ratio`, `liquidations_long`, `liquidations_short`
- `long_short_ratio` et `liquidations_*` souvent `null` (dépend de Coinglass non prouvé runtime)

### `collector_binance_spot`

Opérationnel via `collectors_core`. Produit un `pair_market_snapshot` avec :

- `pair_symbol`, `base_asset`, `quote_asset`, `trading_status`
- `last_price`, `open_price_24h`, `high_price_24h`, `low_price_24h`
- `volume_24h`, `quote_volume_24h`, `price_change_24h`, `price_change_pct_24h`
- Layout : `raw/`, `normalized/`, `latest.json`, `manifest.json`, `status.json`, `events.jsonl`, `errors.jsonl`

### `collector_coingecko`

Présent dans `modules/` mais couverture réelle à confirmer. Non inclus dans ce child GO ; traité dans un child ultérieur.

### `data/data_center/`

N'existe pas encore dans le repo. Ce child GO documente les contrats mais ne crée pas le layout. Le layout est couvert par `GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01`.

## 8_VALIDATED_PLAN

- Produire `10_PRODUCER_CONTRACT_SPEC.md` définissant le format canonique d'un contrat producer.
- Produire `20_PRODUCER_INVENTORY.md` avec les deux contrats connus et leur mapping.
- Ne pas modifier les modules `derivatives_collector` ni `collector_binance_spot`.
- Ne pas créer `data/data_center/` (hors scope).
- Ne pas modifier les index globaux.

## 9_SELECTED_SOLUTION

Un producer contract Data Center est une déclaration JSON/YAML qui doit contenir :

```yaml
producer_id: <string unique>
family: derivatives | spot | events | vision | other
schema_version: v1
contract_class: market_metrics.v1 | pair_market_snapshot.v1 | <autre>
output_path_root: data/data_center/<family>/<producer_id>/
write_mode: atomic | append
latency_class: oneshot | scheduled | realtime
collectable_metrics: [liste]
missing_metrics: [liste]
coverage_status: full | partial | not_proven_runtime_adapter
validated_at: <YYYY-MM-DD>
```

Le registre `data/data_center/_registry/producers.json` liste tous les producers actifs avec leur `producer_id`, `contract_class`, `schema_version` et `last_write`.

## 10_SELECTED_SETUP

Paths cibles Data Center pour les producers connus :

```text
data/data_center/derivatives/derivatives_collector/
  raw/
  normalized/
  latest.json         <- market_metrics.v1 payload
  manifest.json
  status.json
  events.jsonl
  errors.jsonl
  cache/by_symbol/<SYMBOL>.json

data/data_center/spot/binance_spot/
  raw/
  normalized/
  latest.json         <- pair_market_snapshot.v1 payload
  manifest.json
  status.json
  events.jsonl
  errors.jsonl
```

Ces paths cibles sont documentés ici. Leur création effective est dans `GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01`.

## 11_KEY_DECISIONS

- `market_metrics.v1` existant est adopté tel quel comme `contract_class` du producer `derivatives_collector`.
- `pair_market_snapshot.v1` est le `contract_class` proposé pour `collector_binance_spot` (nouveau nom du format existant).
- Le registre `producers.json` est le seul index global des producers actifs du Data Center.
- `collector_coingecko` est hors scope de ce child GO.

## 12_INVARIANTS

- Aucun runtime modifié.
- Aucune modification de `market_metrics_v1.py` ni `market_metrics_writer.py`.
- Aucun fichier `data/data_center/` créé à ce stade.
- Aucune modification des index globaux.

## 13_ESTABLISHED

- `market_metrics.v1` implémenté et testé dans `derivatives_collector`.
- `collector_binance_spot` produit un `pair_market_snapshot` normalisé via `collectors_core`.
- `collectors_core` fournit déjà les primitives de stockage (atomic_write, append, manifest, status).
- Layout `data/collectors/` existant est aligné avec le layout Data Center cible.

## 14_HYPOTHESIS

- `pair_market_snapshot` peut être renommé `pair_market_snapshot.v1` sans casser l'implémentation existante.
- `market_metrics.v1` peut être réutilisé sans modification comme contrat producer Data Center.

## 15_REMAINING_GAP

- `10_PRODUCER_CONTRACT_SPEC.md` : à produire.
- `20_PRODUCER_INVENTORY.md` : à produire.
- `collector_coingecko` : couverture réelle à confirmer dans un child ultérieur.
- Layout `data/data_center/` : hors scope (child `REGISTRY_STORAGE_01`).

## 16_TODO

1. Écrire `10_PRODUCER_CONTRACT_SPEC.md` — format canonique contrat producer.
2. Écrire `20_PRODUCER_INVENTORY.md` — contrats `derivatives_collector` et `binance_spot`.
3. Créer l'inbox locale.
4. Préparer le patch de transport.

## 17_RESUME_POINT

Prochain geste : produire `10_PRODUCER_CONTRACT_SPEC.md`.

Prochain child GO après fermeture : `GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01`.

---

## BUNDLE_TARGET — PRODUCER_CONTRACTS_FORMALIZED_V1

Ce child est fermable quand :
- `10_PRODUCER_CONTRACT_SPEC.md` livré et cohérent avec `market_metrics.v1` existant ;
- `20_PRODUCER_INVENTORY.md` livré avec contrats pour `derivatives_collector` et `collector_binance_spot` ;
- mapping vers paths `data/data_center/` documenté.
