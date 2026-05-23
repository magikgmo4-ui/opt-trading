---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01_STALE_MACHINES_POLICY
doc_type: policy
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 30_STALE_MACHINES_POLICY

## Définition

`stale_machines` est calculé par l’orchestrateur fleet à partir de l’âge des `latest.json` collectés.

Seuil repo-first :

```text
modules/runtime_health/fleet_orchestrator.py
_STALE_THRESHOLD_MINUTES = 15
```

## Machines concernées (entrée GO)

```text
stale_machines = cursor-ai, fantome
```

## Interprétation attendue

Un “stale” peut signifier :

- la machine ne tourne pas le timer `opt-trading-runtime-health.timer`
- le fichier `latest.json` n’est pas publié au bon endroit (data_dir) / pas collectable
- la machine est volontairement inactive (hors runtime) mais reste dans la map fleet

## Politique à expliciter (choix)

### Option 1 — Restaurer (viser PASS)

But : `cursor-ai` et `fantome` doivent publier un `latest.json` frais.

Pré-requis :

- `opt-trading-runtime-health.timer` actif sur la machine concernée
- `data_dir` correct (Linux) ou `data_dir_candidates` résolu (Windows)
- collecte fleet fonctionnelle (SSHFS / SSH pull / local)

Effet attendu :

- suppression de `stale_machines`
- STEP 5 plus proche d’un `PASS` (si ENV/PORTS/PATHS non bloquants)

### Option 2 — Retirer de la map (viser PASS)

But : si la machine est retirée de la flotte utile, elle ne doit plus compter dans le calcul fleet.

Actions possibles :

- retirer l’entrée machine de `config/machine_runtime_map.yml`, ou
- introduire un flag explicite (ex: `fleet_enabled: false`) et patcher `fleet_orchestrator.py` pour ignorer ces machines

Nota : la seconde approche conserve la mémoire de la machine sans imposer la fraîcheur.

### Option 3 — Conserver mais accepter (WARN_ACCEPTED_WITH_EXPLICIT_POLICY)

But : conserver ces entrées (histoire, future réactivation) tout en évitant que “stale” bloque un closeout.

Politique minimale :

- lister explicitement les machines autorisées à être stale
- justifier pourquoi (role non-runtime / machine d’atelier / machine éteinte)
- fixer un critère de révision (ex: “à réévaluer avant fermeture parent umbrella” ou “à réévaluer lors du prochain déploiement fleet”)

