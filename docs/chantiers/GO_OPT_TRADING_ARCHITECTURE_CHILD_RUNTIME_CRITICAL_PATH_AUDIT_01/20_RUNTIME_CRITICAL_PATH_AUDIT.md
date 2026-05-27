# 20_RUNTIME_CRITICAL_PATH_AUDIT - GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_CRITICAL_PATH_AUDIT_01

## SCOPE

```text
TradingView alert
-> webhook_server.py
-> auth / paper guards / risk gate
-> execution path
-> state/
-> adapters/webhook_to_perf.py
-> perf/perf_app.py
-> perf/perf.db
```

## PATH_SEGMENTS

### 1. Ingress

- `TradingView alert -> webhook_server.py` est le point d'entree runtime le plus visible et le mieux etabli dans la cartographie.
- `modules/auth/webhook_key.py` et `modules/webhook/paper_guards` montrent que l'entree est deja protegee par validation et garde paper/runtime.

### 2. Risk and decision boundary

- `webhook_server.py -> modules/risk_engine/app/risk_calculator.py` est explicite.
- `risk_calculator -> risk_engine` est visible, mais la granularite de decision intermediaire reste partiellement implicite.
- `modules/decision_engine/app/strategy_logic.py -> risk_calculator` reste exprime comme relation visible/probable, pas comme chemin totalement prouve de bout en bout.

### 3. Execution boundary

- `webhook_server.py -> modules/execution_engine/` est visible comme chemin d'execution principal.
- `modules/trade_executor/app/executor.py -> modules/execution_engine/` montre une implementation d'execution reliee, mais pas encore la totalite des appels runtime concrets.

### 4. Persistence and perf boundary

- `webhook_server.py -> state/` est visible comme ecriture probable d'evenements.
- `adapters/webhook_to_perf.py -> perf/perf_app.py` est encore `probable`, donc la frontiere cross-service est un point cle a confirmer.
- `perf/perf_app.py -> perf/perf.db WAL probable` montre la persistence perf attendue, sans preuve finale dans cette vue seule.

## POINTS_FORTS

- Le critical path est suffisamment bien decoupe pour une revue operationnelle.
- Les frontieres `ingress`, `risk`, `execution`, `persistence` et `perf` sont visibles.
- Les zones non prouvees sont marquees au lieu d'etre supposees.

## RISQUES_PRIORITAIRES

1. `webhook_server.py` concentre trop de responsabilites apparentes.
2. Le bridge `adapters/webhook_to_perf.py` reste un point de confiance partielle tant qu'il n'est pas confirme par preuve code/runtime.
3. `perf/perf_app.py` semble combiner exposition HTTP, UI et persistence perf.
4. `state/` et `perf/perf.db` sont visibles, mais les regles d'ownership et de reprise ne sont pas formalisees ici.

## LINKS_TO_CONFIRM

```text
webhook_server.py -> adapters/webhook_to_perf.py -> perf/perf_app.py
perf/perf_app.py -> perf/perf.db
strategy_logic.py -> risk_calculator.py sur le chemin runtime reel
trade_executor/app/executor.py -> execution_engine/ comme implementation dominante
```

## RECOMMANDATIONS

1. Produire une preuve code ciblee du chemin `webhook -> perf bridge -> perf db`.
2. Distinguer explicitement dans un prochain child ce qui releve du traitement synchrone webhook et ce qui releve d'une propagation asynchrone ou cross-service.
3. Documenter l'ownership de `state/` vs `perf/perf.db`.
4. Evaluer si `webhook_server.py` doit etre reduit a un orchestrateur mince autour de services plus explicites.

## NEXT_GO_PROPOSED

```text
GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_LINK_PROOF_01
  - prouver les liens webhook -> perf bridge -> perf db

GO_OPT_TRADING_ARCHITECTURE_CHILD_STATE_AND_PERF_OWNERSHIP_01
  - formaliser ownership, writes, reads et reprise

GO_OPT_TRADING_ARCHITECTURE_CHILD_WEBHOOK_ENTRYPOINT_DECOMPOSITION_01
  - evaluer la reduction du couplage autour de webhook_server.py
```

## VERDICT

```text
Critical path visible: yes
Operationally readable: yes
Fully proven runtime chain: no
Main risk: webhook/perf over-centralization
Next best action: prove bridge and persistence boundaries
```
