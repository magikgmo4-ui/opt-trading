# 20_REGISTRY_OWNERSHIP_AUDIT - GO_OPT_TRADING_ARCHITECTURE_CHILD_REGISTRY_OWNERSHIP_AUDIT_01

## SCOPE

Surfaces principales observees dans la cartographie:

```text
config/machine_runtime_map.yml
configs/openclaw/security/skill_policy.yaml
registry/machines_registry.yaml
registry/meta_index.yaml
registry/modules_registry.yaml
registry/ui_surfaces_registry.yaml
registry/wrappers_registry.yaml
modules/openclaw_config_modulaire/app/
modules/openclaw_operator_bridge/app/bridge.py + client.py + schema.py
modules/model_provider_openclaw/config/
modules/runtime_health/
scripts/ai/workers/
```

## OBSERVATIONS

### Registry producers or source candidates

- `registry/machines_registry.yaml`
- `registry/meta_index.yaml`
- `registry/modules_registry.yaml`
- `registry/ui_surfaces_registry.yaml`
- `registry/wrappers_registry.yaml`
- `config/machine_runtime_map.yml`
- `configs/openclaw/security/skill_policy.yaml`
- `modules/model_provider_openclaw/config/`

### Main consumers visible in Mermaid

- `modules/openclaw_config_modulaire/app/`
- `modules/openclaw_operator_bridge/app/bridge.py + client.py + schema.py`
- `modules/runtime_health/`
- `scripts/ai/workers/`
- `.github/workflows/`

## POINTS_FORTS

- Les registries sont explicites et regroupes dans une vue lisible dediee.
- La machine map, la skill policy et les registries principaux sont visibles comme surfaces distinctes.
- Les consommateurs majeurs apparaissent aussi dans la carte: OpenClaw config modulaire, runtime health, operator bridge, workers et workflows.

## AMBIGUITES_D_AUTORITE

1. `config/machine_runtime_map.yml -> registry/machines_registry.yaml`
   - la relation est visible, mais le sens d'autorite n'est pas entierement etabli: la map derive-t-elle du registry, ou sert-elle de projection operatoire?

2. `registry/* -> modules/openclaw_config_modulaire/app/`
   - la carte montre une consommation des registries, mais pas quel fichier joue le role de source de verite primaire versus aggregation.

3. `configs/openclaw/security/skill_policy.yaml -> workflows / operator bridge`
   - la policy est clairement une surface de gouvernance, mais la chaine exacte d'application reste partielle.

4. `modules/model_provider_openclaw/config/ -> modules/openclaw_operator_bridge`
   - visible comme routage probable, sans preuve finale d'autorite ou de precedence.

## OWNERSHIP_RISKS

- Risque de multi-source ambiguity entre `config/*` et `registry/*` si la responsabilite d'edition n'est pas explicite.
- Risque d'ownership diffus si plusieurs consumers lisent les registries sans couche de validation centralisee clairement identifiee.
- Risque de confusion entre policy de securite, registry d'inventaire et configuration operationnelle.
- Risque de drift documentaire si des patches de registry existent hors des sources principales de gouvernance.

## HYPOTHESES_A_CONFIRMER

```text
machine_runtime_map.yml est une projection operatoire, pas la source primaire
meta_index.yaml sert de couche de navigation plutot que d'autorite fonctionnelle
modules_registry.yaml et wrappers_registry.yaml sont des inventaires structurants consommes par openclaw_config_modulaire
skill_policy.yaml joue un role normatif applique par workflows et/ou bridge
```

## RECOMMANDATIONS

1. Produire une table explicite `source of truth / consumer / validation gate` pour chaque fichier de `registry/*` et `config/*`.
2. Clarifier si `config/machine_runtime_map.yml` derive de `registry/machines_registry.yaml` ou l'inverse.
3. Identifier un point unique de validation pour les registries consommes par `modules/openclaw_config_modulaire/app/`.
4. Distinguer clairement dans un prochain child les roles `inventory`, `policy`, `runtime map` et `operator routing`.

## NEXT_GO_PROPOSED

```text
GO_OPT_TRADING_ARCHITECTURE_CHILD_REGISTRY_SOURCE_OF_TRUTH_MATRIX_01
  - etablir une matrice source/consumer/validator

GO_OPT_TRADING_ARCHITECTURE_CHILD_MACHINE_RUNTIME_MAP_AUTHORITY_01
  - clarifier l'autorite entre machine map et machines registry

GO_OPT_TRADING_ARCHITECTURE_CHILD_OPENCLAW_POLICY_APPLICATION_CHAIN_01
  - prouver comment skill_policy et provider policy sont appliquees
```

## VERDICT

```text
Registry surfaces visible: yes
Registry authority fully clear: no
Main risk: distributed ownership ambiguity
Best next step: source-of-truth matrix and authority proof
```
