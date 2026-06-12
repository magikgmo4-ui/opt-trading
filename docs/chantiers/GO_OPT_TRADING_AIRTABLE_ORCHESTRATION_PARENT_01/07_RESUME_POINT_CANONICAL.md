---
doc_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01_RESUME_POINT_CANONICAL
doc_type: resume_point
repo: opt-trading
project: opt-trading
module: airtable_bridge
go_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01
status: reference
lifecycle_stage: reprise
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - airtable
  - resume_point
  - bridge
  - orchestration
  - continuity
links:
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/04_PRODUCT_FINISH_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/05_IMPLEMENTATION_SPEC.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/06_INDEXATION_STATUS.md
  - docs/index/BRANCH_STATE.md
---

# 07_RESUME_POINT_CANONICAL

## 1_MASTER_TARGET

Construire `Airtable Orchestration Layer V1` comme couche humaine de cockpit, journal, review et orchestration légère pour opt-trading.

Airtable ne remplace pas opt-trading. Airtable ne devient pas moteur de trading, DB massive ou source canonique.

## 4_MASTER_PROJECT_PLAN

Plan global déjà validé :

1. cadrage produit — terminé ;
2. recherche Airtable — terminé ;
3. architecture intégration — terminé ;
4. schéma Airtable Trading Journal V1 — terminé ;
5. spécification d'implémentation — terminé ;
6. indexation minimale — terminée avec GAP index globaux documenté ;
7. prochaine phase — implémentation du bridge.

## 6_FINAL_TARGET

Créer le module :

```text
modules/airtable_bridge/
```

avec :

- client API Airtable ;
- payloads `trade` et `signal` ;
- stratégie fail-open ;
- scripts opérateur `sanity_check.sh`, `cmd.sh`, `menu.sh` ;
- `.env.example` sans secrets ;
- export JSON/CSV prévu.

## 7_CANONICAL_STATE

- Branche active : `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01`.
- Produit : `Airtable Orchestration Layer V1` cadré et verrouillé.
- Point produit principal : `04_PRODUCT_FINISH_PLAN.md`.
- Point technique principal : `05_IMPLEMENTATION_SPEC.md`.
- Point indexation : `06_INDEXATION_STATUS.md`.
- `BRANCH_STATE.md` existe et trace la branche.
- Index globaux non patchés : `GO_INDEX`, `REPRISE`, `ACTIVE_STREAMS`, `NEXT_GO_CANDIDATES` ; gap documenté, non bloquant.

## 8_VALIDATED_PLAN

Séquence à suivre :

```text
SPEC → MODULE → TEST → INTEGRATION → EXPORT → CLOSEOUT
```

## 9_SELECTED_SOLUTION

Solution retenue : `GO_LIMITED`.

Airtable est validé comme :

- UI humaine ;
- journal ;
- review ;
- orchestration légère ;
- cockpit opérateur.

Airtable est interdit comme :

- moteur trading ;
- stockage tick data ;
- backtest massif ;
- dépendance runtime critique.

## 10_SELECTED_SETUP

```text
Core        : opt-trading
Bridge      : airtable_bridge
UI          : Airtable
Export      : JSON / CSV
Future DB   : Timescale / ClickHouse / Postgres
```

## 11_KEY_DECISIONS

- Airtable reste non critique.
- Bridge fail-open obligatoire.
- Export obligatoire.
- Aucun secret dans Git.
- opt-trading reste source canonique.

## 12_INVARIANTS

- Pas de secret Git.
- Pas de tick data Airtable.
- Pas de boucle haute fréquence via Airtable.
- Pas de blocage runtime si Airtable est indisponible.
- Pas de code avant lecture de `05_IMPLEMENTATION_SPEC.md`.

## 13_ESTABLISHED

- Produit défini.
- Limites Airtable documentées.
- Architecture stable.
- Schéma V1 présent.
- Spécification technique présente.
- Indexation minimale traçable.

## 15_REMAINING_GAP

- Implémenter `modules/airtable_bridge/`.
- Créer ou connecter une base Airtable réelle.
- Tester un POST réel seulement après configuration des secrets locaux.
- Patcher plus tard les index globaux si nécessaire.

## 16_TODO

Next GO : `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01`.

Actions :

1. créer `modules/airtable_bridge/` ;
2. créer `app/client.py` ;
3. créer `app/payloads.py` ;
4. créer `scripts/sanity_check.sh` ;
5. créer `scripts/cmd.sh` ;
6. créer `scripts/menu.sh` ;
7. créer `.env.example` ;
8. tester sans réseau ;
9. tester POST réel si base Airtable configurée.

## 17_RESUME_POINT

Reprise opérationnelle :

```text
branche : go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01
ouvrir  : docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/05_IMPLEMENTATION_SPEC.md
exécuter: GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01
```

## 18_TO_DOCUMENT

- `IMPLEMENTATION_REAL_RUN_01`
- `AIRTABLE_BRIDGE_TEST_RESULTS`
- `BOT_VISION_TO_AIRTABLE_PIPELINE`
- `EXPORT_PIPELINE_SPEC`

## 19_TO_REMEMBER

Memory Bricks projet :

- Airtable = lecture humaine.
- opt-trading = exécution.
- bridge = optionnel.
- export = sécurité.
- prochaine reprise = implémentation `airtable_bridge`.

## RISKS

- À qualifier.
