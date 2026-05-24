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

Validation terrain read-only effectuée (2026-05-23).

Éléments établis :

- `db-layer` : `ENV=WARN`, `PORTS=WARN`, `PATHS=WARN` dus uniquement à des checks `optional_*` (détails dans `10_RESIDUAL_WARNINGS_PROOF.md`).
- Fleet : `stale_machines = cursor-ai, fantome` avec `unreachable=[]` et `failing=[]`.
- `fantome` répond en SSH mais son `latest.json` est ancien (stale du point de vue fleet).

Gap restant :

- établir la cause exacte du stale `cursor-ai` (machine offline vs absence/chemin de `latest.json`) sans écrire côté Windows.

## Point de reprise (next step)

1) Fixer le statut final STEP 5 :
   - recommandé : `WARN_ACCEPTED_WITH_EXPLICIT_POLICY` (voir section Décision).
2) Consolider la politique “WARN acceptés” :
   - `ENV`: `db-layer` optionnel (TELEGRAM_BOT_TOKEN, ALLOWED_CHAT_ID)
   - `PORTS`: ports optionnels fermés sur `db-layer` (18789, 8000)
   - `PATHS`: `/var/log/trading` optionnel absent sur `db-layer`
   - `stale_machines`: `cursor-ai`, `fantome` acceptés tant que machines non-runtime
3) Si un patch est nécessaire pour viser `PASS` :
   - le borner à `config/machine_runtime_map.yml` et/ou au calcul fleet,
   - préserver le signal (ne pas masquer un défaut réel),
   - conserver l’interdiction watchdog 11-12.

## Décision (proposée)

```text
STEP_5 = WARN_ACCEPTED_WITH_EXPLICIT_POLICY
```

## Index globaux

Ce GO ouvre un nouveau dossier sous `docs/chantiers/`.

Règle : si l’indexation globale (`docs/index/GO_INDEX.md`, etc.) doit être mise à jour, le faire dans une mission dédiée, uniquement si nécessaire et prouvé.

