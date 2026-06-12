---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_05_COLLECTORS_MARKET_INTEL
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - modules
  - step-05
  - collectors
  - market-intelligence
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - docs/COLLECTORS_FAMILY_DOCTRINE_01.md
  - docs/COLLECTORS_MIGRATION_MAP_01.md
  - packages/collectors_core/README.md
  - modules/collector_binance_spot/README.md
  - modules/collector_coingecko/README.md
  - modules/derivatives_collector/README.md
  - modules/derivatives_analyzer/README.md
  - modules/market_scanner/README.md
  - modules/marketdata/README.md
  - modules/liquidation_analyzer/README.md
  - modules/opportunity_ranker/README.md
---

# Step 05 - family plan `Collectors / market intelligence`

## Statut
Complete.

## Objet
Figer la structuration P2 de la famille `Collectors / market intelligence`, en separant collecte, fondation partagee, facade de navigation et intelligence aval.

## Verifications utilisees
- lecture de `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`
- lecture de `docs/COLLECTORS_MIGRATION_MAP_01.md`
- lecture de `packages/collectors_core/README.md`
- lecture des README de :
  - `modules/collector_binance_spot`
  - `modules/collector_coingecko`
  - `modules/derivatives_collector`
  - `modules/derivatives_analyzer`
  - `modules/market_scanner`
  - `modules/marketdata`
  - `modules/liquidation_analyzer`
  - `modules/opportunity_ranker`
- lecture des manifests runtime de :
  - `modules/collector_binance_spot/src/collector_binance_spot/run.py`
  - `modules/collector_coingecko/src/collector_coingecko/run.py`

## Carte de suite
| Couche | Surface retenue | Role |
|---|---|---|
| fondation partagee | `packages/collectors_core` | config, env, HTTP, lifecycle et artefacts partages |
| collectors spot | `collector_coingecko`, `collector_binance_spot` | providers pilotes fondes sur `collectors_core` |
| collector derive | `derivatives_collector` | collecte canonique des derives, sur trajectoire de convergence non destructive |
| facade de navigation | `marketdata` | enveloppe legere d'exploration, pas coeur fonctionnel |
| intelligence derivee | `derivatives_analyzer`, `liquidation_analyzer` | analyse structurelle et signaux derives |
| intelligence de scan / classement | `market_scanner`, `opportunity_ranker` | scan d'opportunites et classement aval |
| consumer externe eventuel | `localcms` | cible de compatibilite de certains artefacts, hors repo producteur |

## Frontieres retenues
- `collectors_core` reste une fondation package. Il ne devient pas un faux mega-module qui absorberait tous les collectors.
- `collector_coingecko` et `collector_binance_spot` restent des providers spot distincts, relies par doctrine et runtime partage.
- `derivatives_collector` reste le collector derive canonique. La doctrine gele deja qu'une migration forcee vers `collectors_core` n'est pas requise.
- `marketdata` reste une facade legere de navigation tant que sa valeur fonctionnelle propre n'est pas prouvee.
- `derivatives_analyzer`, `liquidation_analyzer`, `market_scanner` et `opportunity_ranker` appartiennent a la chaine d'intelligence, pas au noyau de collecte.
- la mention `compatibility_targets: [\"opt-trading\", \"localcms\"]` dans les collectors spot confirme un consumer externe possible, mais ne change pas le fait que `opt-trading` reste producer canonique.

## Ce qui doit etre harmonise
- vocabulaire de famille :
  - `run_id`
  - `manifest.json`
  - `status.json`
  - `latest.json`
  - `events.jsonl`
  - `errors.jsonl`
- doctrine config :
  - defaults commits
  - overrides locaux
  - env overrides
- surface operateur :
  - `cmd`
  - `menu`
  - `sanity`
  - runbook expectations

## Ce qui peut etre mutualise plus tard
- runtime concerns non metier supplementaires vers `collectors_core`
- adaptateurs d'artefacts entre `derivatives_collector` et la doctrine collectors
- contrats de sortie read-only vers un consumer externe comme `localcms`

## Ce qui doit rester separe
- semantique spot et semantique derives
- collecte et intelligence aval
- facade `marketdata` et logique metier de collecte
- collectors et modules de trading/decision qui consomment leurs sorties

## Risques a eviter
- forcer une migration totale de `derivatives_collector` dans `collectors_core`
- introduire un provider #3 avant clarification effective de la doctrine
- confondre `market_scanner` ou `opportunity_ranker` avec des collectors
- surpromouvoir `marketdata` comme coeur fonctionnel alors qu'il reste une facade legere

## Decision retenue
- oui a une suite P2 `Collectors / market intelligence`
- oui a la convergence selective vers `collectors_core`
- non a une fusion runtime large dans ce lot
- `localcms` est retenu seulement comme consumer externe eventuel d'artefacts normalises
- prochain sous-lot logique si besoin :
  - baseline inventory
  - vocabulary alignment
  - artifact family alignment
  - config boundary alignment
  - operator surface alignment

## Rollback
- revert doc-only de cette note
- revert doc-only du plan si besoin

## Point de reprise
Suite P2 `Collectors / market intelligence` cadree. Basculer sur `Vision`, puis vers `Step 06`.

## RISKS

- À qualifier.
