# 30_DOWNSTREAM_OBSERVATION

## Vision pipeline

Observé pendant la fenêtre de soak (`2026-05-19 07:39` à `07:42`) :

- les PNG ont été déplacés vers `vision_processed`
- les sidecars JSON sont restés présents dans `vision_inbox`
- les sorties `.txt` et `.md` ont été générées dans `vision_outbox`
- aucun fichier `rejected/` nouveau sur la fenêtre

## Desk downstream

Contrôles réalisés pendant la fenêtre de soak :

- `shared/inbox` : aucun nouvel artefact
- `desk/snapshots` : aucun nouvel artefact

Conclusion :

- aucun `blocked` ou `invalid_visual` n’a pu être promu vers Desk pendant la fenêtre
- le bridge Desk n’a pas été activé pendant ce soak manuel, donc la vérification Desk reste `not_applicable_runtime_inactive`

## Conclusion aval

- `vision_processed` : OK
- `vision_outbox` : OK
- `desk` : non exercé en live durant ce GO, mais gate content présent et absence de non-ready confirmée
