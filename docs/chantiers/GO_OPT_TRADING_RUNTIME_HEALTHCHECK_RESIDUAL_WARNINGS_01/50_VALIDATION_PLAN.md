---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01_VALIDATION_PLAN
doc_type: validation_plan
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 50_VALIDATION_PLAN

## Contraintes de validation

- Read-only (pas de mutation runtime destructive).
- Aucun watchdog `11-12`.
- Ne pas afficher de secrets (valeurs).

## Validation repo-first (locale)

```bash
git diff --check
git status -sb
```

Contrôle “no secrets in diff” (manuel) :

- vérifier qu’aucune valeur de token / clé n’apparaît (uniquement des noms de variables)

## Validation terrain (db-layer) — commandes read-only

### Healthcheck machine (db-layer)

```bash
cd /opt/trading
bash scripts/runtime_healthcheck.sh --dry-run --no-telegram
MACHINE_ROLE=db-layer bash scripts/runtime_healthcheck.sh --dry-run --no-telegram
```

### Fleet orchestrator

```bash
cd /opt/trading
python3 modules/runtime_health/fleet_orchestrator.py --dry-run --no-telegram
```

### Preuve stale_machines

Objectif : confirmer l’âge des `latest.json` de `cursor-ai` et `fantome` + la méthode de collecte (SSHFS/SSH/local).

Read-only (exemples) :

```bash
ls -la /opt/trading/data/runtime_health/latest.json
ls -la /shared/cursor-ai/runtime_health/latest.json || true
ls -la /shared/fantome/runtime_health/latest.json || true
```

### Preuve ENV (sans valeurs)

Objectif : confirmer présence/absence des clés attendues dans l’environnement du service.

Read-only (exemples) :

```bash
systemctl cat opt-trading-runtime-health.service --no-pager
systemctl show opt-trading-runtime-health.service -p EnvironmentFiles --no-pager
```

Note : ne pas `cat` les fichiers `.env` si cela risque d’exposer des valeurs en clair.

### Preuve PATHS (owner/permissions)

Objectif : compléter `check_path` par une preuve read-only d’ownership/perms.

Read-only (exemples) :

```bash
stat -c '%U:%G %a %n' /opt/trading /opt/trading/data /var/log/trading /shared 2>/dev/null || true
```

## Critère de sortie

- `STEP 5 = PASS` si `healthcheck.py` rend un `overall_status=PASS` (ou équivalent) et `stale_machines` vide.
- `STEP 5 = WARN_ACCEPTED_WITH_EXPLICIT_POLICY` si les WARN restants correspondent exactement à la politique écrite et qu’aucun FAIL n’existe.

