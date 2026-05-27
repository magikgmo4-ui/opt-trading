# 20_RUNTIME_LINK_PROOF - GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_LINK_PROOF_01

## METHODE

Ce rapport ne lit pas encore le code applicatif ligne par ligne. Il requalifie les liens a partir des Mermaid et des audits derives deja merges. Un lien est:

- `prouve` si plusieurs vues convergent et qu'aucune ambiguite majeure n'est maintenue dans les audits
- `invalide` si les audits convergent vers une interpretation trompeuse ou non operative
- `reste a investiguer` si la relation reste explicitement partielle ou conditionnelle

## TABLE_DE_PREUVE

### 1. `TradingView alert -> webhook_server.py`

```text
STATUT = prouve
```

Justification:

- visible dans la vue `060_trading_runtime_critical_path.preview.md`
- repris comme point d'entree le plus etabli dans l'audit runtime critical path
- aucune ambiguite concurrente documentee

### 2. `webhook_server.py -> modules/auth/webhook_key.py`

```text
STATUT = prouve
```

Justification:

- visible dans la vue core runtime
- visible dans la vue runtime critical path comme frontiere d'auth/validation

### 3. `webhook_server.py -> modules/webhook/paper_guards`

```text
STATUT = prouve
```

Justification:

- visible dans la vue core runtime
- confirme comme garde du chemin d'ingress dans l'audit runtime critical path

### 4. `webhook_server.py -> modules/risk_engine/app/risk_calculator.py`

```text
STATUT = prouve
```

Justification:

- relation explicite dans la vue runtime critical path
- relation coherente avec la vue data/strategy/execution

### 5. `modules/risk_calculator -> modules/risk_engine`

```text
STATUT = prouve
```

Justification:

- lien explicite dans la vue data/strategy/execution
- repris comme boundary visible dans l'audit runtime critical path

### 6. `modules/decision_engine/app/strategy_logic.py -> modules/risk_engine/app/risk_calculator.py`

```text
STATUT = reste a investiguer
```

Justification:

- la relation apparait dans les Mermaid comme visible/probable
- l'audit runtime precise que le chemin complet n'est pas encore prouve de bout en bout

### 7. `webhook_server.py -> modules/execution_engine/`

```text
STATUT = prouve
```

Justification:

- visible explicitement dans la vue runtime critical path
- l'audit runtime le traite comme chemin d'execution principal

### 8. `modules/trade_executor/app/executor.py -> modules/execution_engine/`

```text
STATUT = reste a investiguer
```

Justification:

- lien visible dans les Mermaid
- l'audit runtime indique que l'implementation d'execution reliee existe, mais pas encore la totalite des appels runtime concrets

### 9. `webhook_server.py -> state/`

```text
STATUT = reste a investiguer
```

Justification:

- visible comme ecriture probable d'evenements
- l'ownership et les regles de reprise ne sont pas encore formalisees

### 10. `adapters/webhook_to_perf.py -> perf/perf_app.py`

```text
STATUT = reste a investiguer
```

Justification:

- c'est la principale frontiere cross-service encore marquee `probable`
- les audits parent et critical path la listent explicitement comme precondition avant refactor

### 11. `perf/perf_app.py -> perf/perf.db`

```text
STATUT = reste a investiguer
```

Justification:

- la persistence attendue est visible, mais encore qualifiee `WAL probable`
- les audits demandent une confirmation avant tout split de `perf/perf_app.py`

### 12. `perf/perf_app.py -> registry/cockpit/automation/index.html`

```text
STATUT = reste a investiguer
```

Justification:

- le lien est documente comme `mounts desk and perf UI probable`
- utile architecturalement, mais pas encore une preuve runtime definitive

### 13. `modules/perf/app.py UNKNOWN candidate -> perf/perf_app.py`

```text
STATUT = invalide comme lien de runtime prouve
```

Justification:

- les audits convergent pour le traiter comme `UNKNOWN candidate`
- il ne peut pas servir de base de refactor tant que son role exact n'est pas etabli

### 14. `modules/trading_realtime_v1 -> modules/strategy/adapter.py`

```text
STATUT = reste a investiguer
```

Justification:

- visible comme relation `probable`
- aucun audit ne la requalifie en preuve solide ou en invalidation

### 15. `modules_model_provider_openclaw_config -> modules_openclaw_operator_bridge`

```text
STATUT = reste a investiguer
```

Justification:

- l'audit registry ownership la traite explicitement comme routage probable sans preuve finale d'autorite

### 16. `config/machine_runtime_map.yml -> registry/machines_registry.yaml`

```text
STATUT = reste a investiguer
```

Justification:

- l'audit registry ownership montre une relation visible mais une autorite ambigue
- il faut encore clarifier le sens source -> projection ou l'inverse

### 17. `configs/openclaw/security/skill_policy.yaml -> workflows / operator bridge`

```text
STATUT = reste a investiguer
```

Justification:

- la policy est clairement visible
- la chaine exacte d'application reste partielle selon l'audit registry ownership

## SYNTHESE

### Liens maintenant suffisamment etablis

```text
TradingView alert -> webhook_server.py
webhook_server.py -> modules/auth/webhook_key.py
webhook_server.py -> modules/webhook/paper_guards
webhook_server.py -> modules/risk_engine/app/risk_calculator.py
modules/risk_calculator -> modules/risk_engine
webhook_server.py -> modules/execution_engine/
```

### Liens invalides comme base de refactor immediate

```text
modules/perf/app.py UNKNOWN candidate -> perf/perf_app.py comme lien runtime prouve
```

### Liens qui restent a investiguer avant refactor code

```text
strategy_logic.py -> risk_calculator.py sur le chemin runtime reel
trade_executor/app/executor.py -> execution_engine/ comme implementation dominante
webhook_server.py -> state/
adapters/webhook_to_perf.py -> perf/perf_app.py
perf/perf_app.py -> perf/perf.db
perf/perf_app.py -> registry/cockpit/automation/index.html
modules/trading_realtime_v1 -> modules/strategy/adapter.py
modules_model_provider_openclaw_config -> modules_openclaw_operator_bridge
config/machine_runtime_map.yml -> registry/machines_registry.yaml
configs/openclaw/security/skill_policy.yaml -> workflows / operator bridge
```

## REFACTOR_READINESS

### Surs pour preparer un refactor cible

- `webhook_server.py` peut faire l'objet d'un travail de decomposition conceptuelle
- `perf/perf_app.py` peut faire l'objet d'un plan de split conceptuel

### Pas surs pour un refactor code immediat

- refactor effectif du bridge `adapters/webhook_to_perf.py`
- split concret base sur `modules/perf/app.py UNKNOWN candidate`
- rationalisation ownership state/perf sans preuve supplementaire

## NEXT_GO_SI_REFACTOR_DOIT_DEVENIR_SUR

```text
GO_OPT_TRADING_ARCHITECTURE_CHILD_RUNTIME_BRIDGE_PROOF_01
  - confirmer webhook -> adapters/webhook_to_perf.py -> perf/perf_app.py

GO_OPT_TRADING_ARCHITECTURE_CHILD_PERF_DB_PERSISTENCE_PROOF_01
  - confirmer perf/perf_app.py -> perf/perf.db comme chaine active

GO_OPT_TRADING_ARCHITECTURE_CHILD_STATE_EVENT_OWNERSHIP_PROOF_01
  - formaliser les writes/reads/reprise autour de state/

GO_OPT_TRADING_ARCHITECTURE_CHILD_OPENCLAW_AUTHORITY_PROOF_01
  - confirmer les chaines machine_runtime_map, skill_policy et provider policy
```

## VERDICT

```text
Several critical runtime links are now strong enough to frame refactor intent.
The highest-risk boundaries remain the webhook/perf bridge, perf db persistence, and state ownership.
The next safe step is still proof-first, not code-first.
```
