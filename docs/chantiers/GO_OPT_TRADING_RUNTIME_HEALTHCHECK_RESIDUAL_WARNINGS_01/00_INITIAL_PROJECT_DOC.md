---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 00_INITIAL_PROJECT_DOC — GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01

## Contexte canonique (entrée)

- NEXT_GO issu de `GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01`.
- Le blocage Python/PyYAML est considéré **fermé** et **hors-scope** ici.
- Résiduel ciblé : `STEP_5_FINAL = WARN_RESIDUAL_ENV_PORTS_PATHS_STALE_MACHINES`.
- Warnings résiduels :
  - `ENV`
  - `PORTS`
  - `PATHS`
  - `stale_machines = cursor-ai, fantome`
- `failing = []`, `unreachable = []`.
- Gateway non incriminé.
- Watchdog `11-12` non lancé (contrainte).

## Besoin initial

Traiter les warnings résiduels du runtime healthcheck (STEP 5) **sans rouvrir** le diagnostic Python/PyYAML.

## Cible finale

Transformer :

```text
STEP 5 = WARN_RESIDUAL
```

en un statut propre :

- `STEP 5 = PASS`
ou
- `STEP 5 = WARN_ACCEPTED_WITH_EXPLICIT_POLICY`

## Solution retenue (ordre de travail)

Ne pas corriger à l’aveugle. D’abord classifier les warnings (lecture/configs/preuves read-only), puis choisir :

- correction minimale prouvée (si le warning révèle un défaut réel), ou
- acceptation explicite avec une politique écrite et opposable.

## Contraintes

- Branch dédiée : `go/GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01`.
- Commencer par documentation + commandes read-only.
- Ne pas toucher aux secrets (ne pas afficher de valeurs secrètes).
- Ne pas lancer watchdog `11-12`.
- Ne pas pop `stash@{0}`.
- Ne pas réaligner db-layer sur sot/mainline tant que le commit local unique `1a8d49a5` n’est pas arbitré.
- Ne pas modifier les index globaux sauf nécessité prouvée (préférer une mission dédiée si nécessaire).

## Livrables minimaux (dans ce chantier)

- `00_INITIAL_PROJECT_DOC.md`
- `10_RESIDUAL_WARNINGS_PROOF.md`
- `20_ENV_PORTS_PATHS_ANALYSIS.md`
- `30_STALE_MACHINES_POLICY.md`
- `40_FIX_OR_ACCEPTANCE_PLAN.md`
- `50_VALIDATION_PLAN.md`
- `90_REPRISE.md`

