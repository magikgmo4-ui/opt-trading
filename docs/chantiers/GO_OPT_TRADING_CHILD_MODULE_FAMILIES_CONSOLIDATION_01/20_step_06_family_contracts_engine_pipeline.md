---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_06_ENGINE_PIPELINE
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
  - step-06
  - engine-pipeline
  - contracts
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - modules/engines/README.md
  - modules/decision_engine/README.md
  - modules/execution_engine/README.md
  - modules/journal_engine/README.md
  - modules/perf_engine/README.md
  - modules/portfolio_engine/README.md
  - modules/position_engine/README.md
  - modules/probability_engine/README.md
  - modules/risk_engine/README.md
  - modules/desk_pro_orchestrator/README.md
  - webhook_server.py
---

# Step 06 - family contracts `Engine pipeline`

## Statut
Complete.

## Objet
Durcir la famille `Engine pipeline` par contrats et frontieres, sans chercher une fusion physique entre moteurs.

## Verifications utilisees
- lecture de `modules/engines/README.md`
- lecture des README de :
  - `modules/decision_engine`
  - `modules/execution_engine`
  - `modules/journal_engine`
  - `modules/perf_engine`
  - `modules/portfolio_engine`
  - `modules/position_engine`
  - `modules/probability_engine`
  - `modules/risk_engine`
- lecture de `modules/desk_pro_orchestrator/README.md`
- lecture de `webhook_server.py`

## Carte de famille
| Surface | Role retenu |
|---|---|
| `engines` | coordination legere, registre et routage de compatibilite |
| `probability_engine` | scoring probabiliste central |
| `decision_engine` | arbitrage directionnel final avant risque |
| `risk_engine` | gate de risque et sizing |
| `execution_engine` | planification d'execution |
| `position_engine` | etat de position / bridging execution -> tracking |
| `perf_engine` | tracking de performance |
| `journal_engine` | aggregation d'etats en journal structure |
| `portfolio_engine` | vue consolidee portefeuille |
| `desk_pro_orchestrator` | orchestration de sequence et production du run |

## Ordre de pipeline retenu
L'ordre de reference reste celui documente par `desk_pro_orchestrator` :
1. `market_scanner`
2. `liquidation_analyzer`
3. `probability_engine`
4. `opportunity_ranker`
5. `decision_engine`
6. `risk_engine`
7. `execution_engine`
8. `position_engine`
9. `perf_engine`
10. `journal_engine`
11. `portfolio_engine`

## Contrats a durcir
### 1. Contrat d'entrees / sorties
Chaque moteur doit garder :
- des artefacts d'entree explicites par fichier JSON
- une sortie stable avec :
  - `symbol`
  - statut/metrique principale du moteur
  - `rationale` ou `summary`
  - timestamp ou run-context quand disponible

### 2. Contrat de sequence
- `desk_pro_orchestrator` reste le seul point de reference pour l'ordre de chaînage.
- `engines` ne doit pas redefinir la pipeline produit; il ne fait que coordonner / router.

### 3. Contrat de wrappers
Chaque moteur garde une surface uniforme :
- `cmd`
- `menu`
- `sanity`
- commandes metier courtes (`score`, `decide`, `assess`, `plan`, `build`, `track`, `export`, `explain`)

### 4. Contrat d'erreur
Les moteurs doivent converger sur :
- erreurs lisibles cote CLI
- absence de side effects hors outputs attendus
- possibilite d'execution sample / explain sans dependance runtime lourde

### 5. Contrat d'ownership
- chaque `*_engine` reste proprietaire de sa logique metier specialisee
- `engines` reste proprietaire du routage / registry minimum
- `desk_pro_orchestrator` reste proprietaire du sequencing global et du `run_summary`

## Ce qui doit rester separe
- `engines` et les moteurs metier
- `risk_engine` et `execution_engine`
- `journal_engine` et `portfolio_engine`
- `perf_engine` et la surface applicative `perf/`

## Ce qui peut etre harmonise sans fusion
- vocabulary run-level :
  - `run_id`
  - `summary`
  - `rationale`
  - `status`
- conventions d'outputs et d'export
- conventions `sample` / `explain` / `export`
- nomenclature des fichiers config sample et outputs

## Risques a eviter
- absorber la logique des `*_engine` dans `engines`
- laisser `webhook_server.py` ou d'autres entrypoints contourner les contrats des moteurs sans documentation
- confondre orchestration de pipeline et logique de moteur
- fusionner `journal_engine` et `portfolio_engine` alors qu'ils ont des responsabilites de sortie differentes

## Decision retenue
- oui au durcissement contractuel de la famille
- non a une fusion physique
- prochaine execution utile si besoin :
  - normaliser les envelopes d'output
  - normaliser les commandes `sample/explain/export`
  - documenter explicitement le `run_id` et le `run_summary` comme contrats de pipeline

## Rollback
- revert doc-only de cette note
- revert doc-only du plan si besoin

## Point de reprise
Contrats `Engine pipeline` cadres. Basculer vers `Runtime edge / platform`, puis `Repo / tooling / authoring`.
