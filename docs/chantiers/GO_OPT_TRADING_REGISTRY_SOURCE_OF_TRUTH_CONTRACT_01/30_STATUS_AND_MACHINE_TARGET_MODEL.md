---
go_id: GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_CONTRACT_01
doc_type: STATUS_AND_MACHINE_TARGET_MODEL
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 30_STATUS_AND_MACHINE_TARGET_MODEL

## Minimal status model

### Keep centrally valid now

- `active` = composant operatoire normal
- `ready` = surface ou entrypoint disponible et exploitable
- `beta` = operatoire mais encore sous reserve explicite

### Add centrally in follow-up implementation

- `legacy` = conserve pour compatibilite ou historique, non cible canonique
- `transitional` = surface encore utile pendant une migration, avec sortie attendue

## Status rule

- `legacy` et `transitional` doivent etre ajoutes a la grammaire centrale plutot que laisses seulement dans les docs libres.
- `deepseek_student` est le premier cas justifiant ce futur ajout, mais ne doit pas forcer une mutation registry dans ce GO.

## Minimal machine_target model

### Keep now

- valeur primaire unique liee a `registry/machines_registry.yaml`
- `admin_trading`, `msi_db_layer`, `student`, `dell_cursor_ai`, `debian_network_future`

### Keep with restriction

- `any` reste acceptable seulement pour les surfaces vraiment machine-agnostic ou purement portables
- `any` ne doit plus servir de raccourci pour "cross-machine mais pas precise"

### Cross-machine representation

Pour les surfaces cross-machine, le contrat recommande:

1. garder `machine_target` comme cible primaire dominante
2. decrire la diffusion multi-machine via champ futur dedie ou metadonnee derivee
3. ne pas surcharger `any` pour masquer une topologie reelle

## Future refinement direction

Un GO dedie doit introduire soit:

- `machine_targets` derive,
- soit `execution_scope` / `placement_mode`,
- soit une meta vue transversale,

mais sans casser la compatibilite simple actuelle de `machine_target`.
