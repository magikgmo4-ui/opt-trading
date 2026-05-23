---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01
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
BUNDLE_TARGET: CONSUMER_CONTRACTS_FORMALIZED_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01
topic_keys:
  - opt-trading
  - data_center
  - consumer_contracts
  - desk_pro
  - strategy_framework
  - perf_engine
  - telegram
  - google_sheets
  - localcms
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01/20_PRODUCER_INVENTORY.md
  - modules/desk_pro/service/market_metrics_reader.py
  - docs/index/inbox/GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01.md
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Data Center opérationnel : producteurs et consommateurs partagent les mêmes contrats normalisés via la règle `producer <> registry data <> consumer`. *(hérité de `GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01`)*

## 2_INITIAL_PROJECT_DOC

Second child GO du parent Data Center. Objectif : formaliser les contrats consumers pour chaque surface consommatrice connue et définir le format du registre `consumers.json`.

Ce chantier est **doc-first** : aucun runtime modifié.

## 3_INITIAL_NEED

Le parent déclare comme second axe du `4_MASTER_PROJECT_PLAN` : *définir le format de lecture, la latence acceptable, les endpoints ou paths d'accès, les règles de fallback pour chaque consommateur*.

Seul Desk Pro est actuellement implémenté comme consumer (`market_metrics_reader.py`). Les autres surfaces (Strategy, Perf, Telegram, Sheets, LocalCMS) sont des consumers futurs sans contrat formalisé.

## 4_MASTER_PROJECT_PLAN — périmètre child

1. Définir le format canonique d'un consumer contract Data Center.
2. Formaliser le contrat consumer pour `PF_DESK_PRO` (partiellement implémenté).
3. Formaliser les contrats consumers pour `PF_STRATEGY_FRAMEWORK_REGISTRY`, `PF_PERF_ENGINE_TRADING_LAB`, `PF_TELEGRAM_SCREENER`, `PF_GOOGLE_SHEETS_CONSUMER`, `PF_LOCALCMS_COCKPIT`.
4. Définir le format du registre `data/data_center/_registry/consumers.json`.
5. Documenter la latence, le fallback et le mode d'accès par consumer.

## 5_GO_PLAN

| Fichier | Contenu |
|---|---|
| `00_INITIAL_PROJECT_DOC.md` | Ce document |
| `10_CONSUMER_CONTRACT_SPEC.md` | Format canonique d'un consumer contract |
| `20_CONSUMER_INVENTORY.md` | Contrats des 6 consumers avec mapping Data Center |

## 6_FINAL_TARGET

Les 6 consumers cibles ont un contrat Data Center formalisé dans `20_CONSUMER_INVENTORY.md`, avec :
- format canonique déclaré dans `10_CONSUMER_CONTRACT_SPEC.md` ;
- read_path depuis `data/data_center/` documenté ;
- fallback, latence et mode d'accès définis ;
- registre `consumers.json` spécifié.

## 7_CANONICAL_STATE

### Consumer actuellement implémenté

**Desk Pro** — `modules/desk_pro/service/market_metrics_reader.py` :
- Lit `data/deskpro/inputs/market_metrics/latest.json` (path hardcodé).
- Contract class : `market_metrics.v1`.
- Fallback : `silent_empty` — retourne `[]` si fichier absent, malformé ou sans métriques prouvées.
- Dépendance : ne lit **pas** encore depuis `data/data_center/` — lit depuis le path Desk Pro dédié.

Ce path Desk Pro (`data/deskpro/inputs/market_metrics/`) est un chemin de transit que `market_metrics_writer.py` alimente. Dans la vision Data Center, ce path devient une **vue consumer** dérivée depuis `data/data_center/derivatives/`.

### Consumers futurs (non implémentés)

- **Strategy Framework** : pas de lecture market_metrics dans `modules/strategy/`.
- **Perf Engine** : lit `state/events.jsonl` et `perf/perf.db` — pas de lecture Data Center.
- **Telegram** : `shared/telegram_notify.py` est outbound-only, pas de lecture Data Center.
- **Google Sheets** : aucun consumer implémenté dans le repo.
- **LocalCMS** : lecture read-only de l'état système, pas de lecture Data Center.

## 8_VALIDATED_PLAN

- Produire `10_CONSUMER_CONTRACT_SPEC.md`.
- Produire `20_CONSUMER_INVENTORY.md` avec les 6 consumers.
- Ne modifier aucun module.
- Ne pas modifier les index globaux.

## 9_SELECTED_SOLUTION

Un consumer contract Data Center déclare **ce qu'une surface lit, depuis quel path, avec quelle tolérance de fraîcheur et quel fallback**.

Le path de lecture d'un consumer est toujours sous `data/data_center/` (ou une vue dérivée nommée explicitement comme le path Desk Pro existant).

La règle de fallback est obligatoire : un consumer qui échoue silencieusement doit le déclarer. Un consumer qui bloque doit le déclarer.

## 10_SELECTED_SETUP

```text
data/data_center/_registry/consumers.json  <- registre global des consumers
```

Chaque surface lit depuis son path contractuel :

```text
data/data_center/<family>/<producer_id>/latest.json        # lecture latest
data/data_center/<family>/<producer_id>/cache/by_symbol/   # lecture par symbole
data/data_center/<family>/<producer_id>/status.json        # vérification fraîcheur
data/data_center/<family>/<producer_id>/normalized/        # accès historique (Perf/Strategy)
```

## 11_KEY_DECISIONS

- Le path Desk Pro existant (`data/deskpro/inputs/market_metrics/`) est une **vue consumer nommée** du Data Center, pas un path Data Center natif. Sa migration est un child GO ultérieur.
- Tous les consumers futurs lisent directement depuis `data/data_center/` sans vue intermédiaire.
- `silent_empty` est le fallback par défaut pour les consumers UI (Desk Pro, LocalCMS).
- `error` est le fallback pour les consumers de reporting (Sheets) qui ne doivent pas silencier un échec.

## 12_INVARIANTS

- Aucun runtime modifié.
- Le path `data/deskpro/inputs/market_metrics/` n'est pas supprimé — il reste valide.
- Aucune modification des index globaux.

## 13_ESTABLISHED

- `market_metrics_reader.py` est l'unique consumer implémenté.
- Son fallback `silent_empty` est prouvé et correct pour Desk Pro.
- Les autres surfaces n'ont aucun consumer Data Center.

## 14_HYPOTHESIS

- La migration du path Desk Pro vers `data/data_center/` peut se faire sans casser `market_metrics_reader.py` en changeant seulement la constante `MARKET_METRICS_LATEST`.

## 15_REMAINING_GAP

- `10_CONSUMER_CONTRACT_SPEC.md` : à produire.
- `20_CONSUMER_INVENTORY.md` : à produire.
- Migration path Desk Pro → Data Center : hors scope (child dédié).
- Implémentation des consumers futurs : hors scope (child par surface).

## 16_TODO

1. Écrire `10_CONSUMER_CONTRACT_SPEC.md`.
2. Écrire `20_CONSUMER_INVENTORY.md`.
3. Créer inbox locale.
4. Préparer patch.

## 17_RESUME_POINT

Prochain geste : produire `10_CONSUMER_CONTRACT_SPEC.md`.

Prochain child GO après fermeture : `GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01`.

---

## BUNDLE_TARGET — CONSUMER_CONTRACTS_FORMALIZED_V1

Fermable quand :
- `10_CONSUMER_CONTRACT_SPEC.md` livré ;
- `20_CONSUMER_INVENTORY.md` livré avec les 6 consumers formalisés ;
- registre `consumers.json` spécifié.
