# 20_HUB_REFACTOR_CANDIDATES - GO_OPT_TRADING_ARCHITECTURE_CHILD_HUB_REFACTOR_CANDIDATES_01

## SCOPE

Ce rapport derive uniquement des audits documentaires et des vues Mermaid lisibles. Il ne propose pas encore de changement code; il priorise des candidats de refactor et les preconditions de preuve.

## HUBS_SOURCE_LIST

```text
webhook_server.py
perf/perf_app.py
modules/strategy/adapter.py
modules/openclaw_config_modulaire/app/
scripts/ai/workers/
modules/data_center/
```

## TRIAGE_RULES

Un hub devient candidat de refactor prioritaire si au moins trois conditions sont vraies:

- concentre plusieurs responsabilites differentes
- relie plusieurs zones macro de l'architecture
- porte des liens `probable` ou `UNKNOWN` sur des chemins critiques
- augmente le risque de regression transverse
- ne peut pas etre clarifie uniquement par documentation supplementaire

## CANDIDATS_PRIORITAIRES

### P1 - `webhook_server.py`

#### Pourquoi prioritaire

- concentre ingress HTTP, auth, guards, risk gate, execution, bridge vers perf et ecriture probable vers `state/`
- apparait comme hub principal du runtime trading critique
- porte des frontieres encore partiellement prouvees autour de `adapters/webhook_to_perf.py`

#### Risques de regression

- une modification locale peut impacter le chemin runtime trading complet
- risque de couplage fort entre logique de transport, decision et orchestration d'execution

#### Decoupe sure envisageable

- separer les responsabilites en couches `ingress validation`, `risk gate`, `execution orchestration`, `perf emission`
- garder `webhook_server.py` comme point d'entree mince si les preuves runtime confirment cette architecture cible

#### Precondition avant refactor

- prouver le chemin `webhook -> perf bridge -> perf db`
- documenter l'ownership de `state/`

#### NEXT_GO

```text
GO_OPT_TRADING_ARCHITECTURE_CHILD_WEBHOOK_ENTRYPOINT_DECOMPOSITION_01
```

### P1 - `perf/perf_app.py`

#### Pourquoi prioritaire

- combine apparemment exposition HTTP, UI/cockpit et persistence perf
- se trouve sur le chemin critique de sortie du runtime trading
- depend d'une frontiere encore `probable` avec `adapters/webhook_to_perf.py`

#### Risques de regression

- les changements perf peuvent toucher simultanement API, cockpit et persistence
- risque de couplage entre interface et stockage

#### Decoupe sure envisageable

- distinguer un coeur de persistence perf, une couche API et une couche UI/mount
- ne lancer aucun refactor avant preuve claire de la chaine bridge -> perf db

#### Precondition avant refactor

- confirmer `perf/perf.db` comme persistence runtime effective
- clarifier le role de `modules/perf/app.py UNKNOWN candidate`

#### NEXT_GO

```text
GO_OPT_TRADING_ARCHITECTURE_CHILD_PERF_APP_SURFACE_SPLIT_CANDIDATE_01
```

## CANDIDATS_SECONDAIRES

### P2 - `modules/openclaw_config_modulaire/app/`

#### Pourquoi secondaire

- fort hub de consommation des registries
- ambiguite d'autorite plus forte que risque immediat de regression runtime trading

#### Ce qu'il faut faire d'abord

- produire une matrice `source of truth / consumer / validator`
- clarifier la precedence entre registries, policies et runtime maps

#### NEXT_GO

```text
GO_OPT_TRADING_ARCHITECTURE_CHILD_REGISTRY_SOURCE_OF_TRUTH_MATRIX_01
```

### P2 - `modules/strategy/adapter.py`

#### Pourquoi secondaire

- hub metier important autour des strategy ids
- relie plusieurs surfaces, mais le risque d'architecture semble moins urgent que les entrypoints runtime

#### Ce qu'il faut faire d'abord

- verifier si le hub est surtout un point de normalisation stable ou un vrai point de congestion logique

#### NEXT_GO

```text
GO_OPT_TRADING_ARCHITECTURE_CHILD_STRATEGY_ADAPTER_ROLE_AUDIT_01
```

### P2 - `scripts/ai/workers/`

#### Pourquoi secondaire

- hub large, mais il s'agit d'une famille de workers plus que d'un seul fichier monolithique
- le besoin premier semble etre la classification et la gouvernance plus qu'un refactor immediat

#### Ce qu'il faut faire d'abord

- distinguer orchestration, validation, ledger et outputs avant toute decoupe

#### NEXT_GO

```text
GO_OPT_TRADING_ARCHITECTURE_CHILD_WORKERS_SURFACE_PARTITION_01
```

## CANDIDATS_DIFFERS

### P3 - `modules/data_center/`

- hub de donnees important
- a traiter apres clarification ownership de `data/`, `state/`, `perf/perf.db`

### P3 - surfaces support `reports/`, `bundles/`, `tmp/`, `_archive/`

- besoin de classification d'abord
- pas un refactor hub prioritaire tant que la frontiere active/historique n'est pas tranchee

## DO_NOT_REFACTOR_YET

```text
modules/perf/app.py UNKNOWN candidate
tmp/ UNKNOWN usage boundary
adapters/webhook_to_perf.py sans preuve supplementaire de sa stabilite reelle
```

Raison:

- ces surfaces exigent d'abord une preuve ou une clarification d'authority/runtime, sinon le refactor serait premature.

## PRIORITY_ORDER

```text
P1 webhook_server.py
P1 perf/perf_app.py
P2 modules/openclaw_config_modulaire/app/
P2 modules/strategy/adapter.py
P2 scripts/ai/workers/
P3 modules/data_center/
P3 reports|bundles|tmp|_archive classification
```

## SAFE_EXECUTION_SEQUENCE

1. Prouver les liens runtime critiques encore `probable`.
2. Clarifier ownership et authority des surfaces registry/state/perf.
3. Refactorer les entrypoints les plus denses seulement apres ces preuves.
4. Traiter ensuite les hubs de gouvernance ou de normalisation.

## NEXT_GO_PRIORISES

```text
1. GO_OPT_TRADING_ARCHITECTURE_CHILD_WEBHOOK_ENTRYPOINT_DECOMPOSITION_01
2. GO_OPT_TRADING_ARCHITECTURE_CHILD_PERF_APP_SURFACE_SPLIT_CANDIDATE_01
3. GO_OPT_TRADING_ARCHITECTURE_CHILD_REGISTRY_SOURCE_OF_TRUTH_MATRIX_01
4. GO_OPT_TRADING_ARCHITECTURE_CHILD_STRATEGY_ADAPTER_ROLE_AUDIT_01
5. GO_OPT_TRADING_ARCHITECTURE_CHILD_WORKERS_SURFACE_PARTITION_01
```

## VERDICT

```text
Refactor candidates identified: yes
Highest-value targets: webhook_server.py and perf/perf_app.py
Precondition before code refactor: proof of runtime and authority boundaries
Best next move: open proof-first children before touching code
```
