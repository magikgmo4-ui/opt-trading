---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01_REPRISE
doc_type: reprise
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 90_REPRISE

## Etat

GO ouvert pour traiter les warnings résiduels STEP 5 du runtime healthcheck :

- `ENV`
- `PORTS`
- `PATHS`
- `stale_machines = cursor-ai, fantome`

Objectif : aboutir à `PASS` ou à `WARN_ACCEPTED_WITH_EXPLICIT_POLICY` sans rouvrir Python/PyYAML.

## Etat repo-first établi

- Le healthcheck classe `optional_*` en `WARN` lorsqu’absent/injoignable (mécanique).
- Le scope `db-layer` contient des `optional_env`, `optional_ports`, `optional_paths` suffisants pour générer des WARN sans FAIL.
- `stale_machines` est basé sur un seuil 15 minutes.

## Gap restant (preuve terrain)

Le repo ne contient pas (sur cette branche locale) un artefact post-deploy matérialisant la sortie exacte :

- quels ports/paths/env sont effectivement en WARN sur `db-layer`
- si `cursor-ai` et `fantome` sont stale parce que “offline” ou parce que la collecte est cassée

Ce gap doit être comblé par la validation read-only listée dans `50_VALIDATION_PLAN.md`.

## Point de reprise (next step)

1) Exécuter les commandes terrain read-only (db-layer) de `50_VALIDATION_PLAN.md`.
2) Produire une table “WARN → cause exacte → action” :
   - correction (viser PASS) ou
   - acceptation explicite (WARN_ACCEPTED_WITH_EXPLICIT_POLICY).
3) Si un patch est nécessaire :
   - le borner à `config/machine_runtime_map.yml` et/ou au calcul fleet,
   - préserver le signal (ne pas masquer un défaut réel),
   - conserver l’interdiction watchdog 11-12.

## Index globaux

Ce GO ouvre un nouveau dossier sous `docs/chantiers/`.

Règle : si l’indexation globale (`docs/index/GO_INDEX.md`, etc.) doit être mise à jour, le faire dans une mission dédiée, uniquement si nécessaire et prouvé.

