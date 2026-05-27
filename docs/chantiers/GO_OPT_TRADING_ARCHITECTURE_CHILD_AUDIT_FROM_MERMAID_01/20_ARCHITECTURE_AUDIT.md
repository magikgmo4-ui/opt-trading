# 20_ARCHITECTURE_AUDIT - GO_OPT_TRADING_ARCHITECTURE_CHILD_AUDIT_FROM_MERMAID_01

## SCOPE

Audit derive uniquement de:

```text
docs/architecture/mermaid/readable/*.preview.md
docs/architecture/mermaid/990_architecture_final.mmd
docs/chantiers/GO_OPT_TRADING_ARCHITECTURE_PARENT_MERMAID_CARTOGRAPHY_01/90_CLOSEOUT.md
```

## POINTS_FORTS

- La separation macro est lisible en cinq zones stables: core runtime, data/strategy/execution, interfaces/entrypoints, ops/governance, quality/contracts/docs.
- Le runtime trading critique reste identifiable de bout en bout: `TradingView alert -> webhook_server.py -> guards/risk -> execution -> perf/state`.
- Le controle et la gouvernance OpenClaw sont visibles separement du coeur trading, avec registries, workers, policy et runtime health.
- La cartographie conserve explicitement les zones d'incertitude via `probable`, `UNKNOWN` et `TODO`, ce qui evite d'inventer des relations non prouvees.
- L'effort qualite est present dans la carte: tests racine, tests module, contracts, schemas, evidence et closeout documentaire.

## POINTS_MOYENS

- La lisibilite est nettement meilleure avec les vues `readable`, mais plusieurs surfaces CLI restent de simples inventaires plutot que des chaines d'execution ordonnees.
- Les registries sont presentes mais la hierarchie d'autorite entre `registry/*`, `config/*` et les lecteurs/consommateurs reste seulement partiellement explicite.
- Les surfaces `data/`, `state/` et `perf/perf.db` sont visibles, mais l'ownership exact des ecritures et des lectures n'est pas encore formalise dans les Mermaid.
- Le volet qualite montre bien les familles de tests, sans aller jusqu'a une table de close-gates par module ou par runtime critique.

## POINTS_FAIBLES

- `webhook_server.py` concentre beaucoup de liens et de responsabilites apparentes: ingress, guards, risk, execution, persistence et bridge vers perf.
- `perf/perf_app.py` apparait a la fois comme surface HTTP, persistence perf et point d'ancrage UI/cockpit, ce qui suggere un entrypoint tres charge.
- Les zones support/historique comme `reports/`, `bundles/`, `_archive/` et `tmp/` sont visibles, mais leur statut architectural actif vs historique n'est pas encore tranche.
- Plusieurs relations structurantes demeurent `probable`, en particulier autour d'OpenClaw, des workers et de certaines frontieres data/runtime.

## RISQUES

- Risque de `god entrypoint` sur `webhook_server.py`: une evolution locale peut impacter simultanement l'entree HTTP, les gardes risque, l'execution et la persistence d'evenements.
- Risque de couplage transversal sur `perf/perf_app.py`: API, UI et persistence perf semblent centralises dans une meme surface.
- Risque de dette de validation: trop de liens `probable` sur les chemins critiques peuvent masquer des dependances runtime reelles non confirmees.
- Risque de confusion control plane vs data plane: la carte globale montre ensemble trading runtime, workers IA, OpenClaw et documentation; utile pour l'inventaire, mais plus difficile pour le pilotage operationnel.
- Risque d'ambiguite sur les surfaces generees ou candidates: `modules/perf/app.py UNKNOWN candidate` signale une zone a clarifier pour eviter une lecture trompeuse du runtime reel.

## HUBS_CRITIQUES

```text
webhook_server.py
perf/perf_app.py
modules/strategy/adapter.py
modules/openclaw_config_modulaire/app/
scripts/ai/workers/
modules/data_center/
```

### Pourquoi ces hubs sont critiques

- `webhook_server.py` est le noeud de convergence le plus visible du runtime trading.
- `perf/perf_app.py` connecte persistence perf, UI et exposition HTTP.
- `modules/strategy/adapter.py` relie plusieurs surfaces metier et runtime autour des strategy ids.
- `modules/openclaw_config_modulaire/app/` apparait comme point d'entree de plusieurs registries.
- `scripts/ai/workers/` centralise la couche worker, validation et outputs.
- `modules/data_center/` sert de pivot implicite entre sources de marche, contrats et consommation aval.

## ZONES_UNKNOWN_OR_PROBABLE

### A confirmer en priorite

- `adapters/webhook_to_perf.py -> perf/perf_app.py` comme frontiere cross-service reelle et stable.
- `perf/perf.db WAL probable` pour confirmer la persistence effectivement active dans le runtime courant.
- `modules/perf/app.py UNKNOWN candidate` pour verifier s'il s'agit d'un ancien entrypoint, d'un duplicat logique ou d'une fausse piste issue de l'inventaire.
- `modules/trading_realtime_v1 -> modules/strategy/adapter.py` pour qualifier si le lien est central ou seulement opportuniste.
- `modules_model_provider_openclaw_config -> modules_openclaw_operator_bridge` pour confirmer la chaine effective de routage modele.
- `tmp/ UNKNOWN usage boundary` pour distinguer support local, transit temporaire ou residu non architectural.

### A confirmer ensuite

- frontiere exacte entre `reports/`, `bundles/`, `_archive/` et les surfaces vraiment actives
- ordre runtime detaille de certaines CLI
- autorite source de verite entre registries, machine map et policy files

## RECOMMANDATIONS

1. Conserver `990_architecture_final.mmd` comme carte d'inventaire globale et ne pas l'utiliser comme seule vue operationnelle.
2. Utiliser en priorite `docs/architecture/mermaid/readable/060_trading_runtime_critical_path.preview.md` pour la revue du chemin trading critique.
3. Ouvrir un child dedie a la validation des liens `probable` autour de `webhook_server.py`, `perf/perf_app.py` et `adapters/webhook_to_perf.py`.
4. Ouvrir un child dedie au control plane OpenClaw pour clarifier la hierarchie `registry/* -> config/* -> operator bridge -> gateway`.
5. Formaliser une classification des surfaces `reports/`, `bundles/`, `_archive/`, `tmp/` en `runtime`, `generated`, `historical` ou `support-only`.
6. Si un refactor est envisage, traiter d'abord les hubs les plus denses plutot que les zones de support.

## NEXT_GO_PROPOSED

```text
GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_LINK_VALIDATION_01
  - confirmer les liens probable du chemin webhook -> perf -> persistence

GO_OPT_TRADING_ARCHITECTURE_CHILD_OPENCLAW_CONTROL_PLANE_AUDIT_01
  - clarifier registries, policies, operator bridge et gateway

GO_OPT_TRADING_ARCHITECTURE_CHILD_DATA_STATE_OWNERSHIP_01
  - documenter ownership et flux de data/, state/ et perf/perf.db

GO_OPT_TRADING_ARCHITECTURE_CHILD_ENTRYPOINT_DEDENSIFICATION_01
  - evaluer si webhook_server.py et perf/perf_app.py doivent etre decomposes

GO_OPT_TRADING_ARCHITECTURE_CHILD_SUPPORT_SURFACES_CLASSIFICATION_01
  - classer reports/, bundles/, tmp/, _archive/
```

## AUDIT_VERDICT

```text
GLOBAL_INVENTORY_QUALITY = good
READABLE_VIEW_QUALITY = good enough for review
RUNTIME_CERTAINTY = partial
PRIMARY_ARCHITECTURE_RISK = over-centralized entrypoints
PRIMARY_INFORMATION_GAP = probable/UNKNOWN links on critical boundaries
NEXT_STEP = open targeted child audits rather than change the parent map
```
