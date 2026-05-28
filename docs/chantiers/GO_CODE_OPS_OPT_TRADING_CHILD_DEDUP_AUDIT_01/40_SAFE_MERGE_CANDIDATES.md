---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01_SAFE_MERGE_CANDIDATES
doc_type: dedup_audit
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01
status: open
lifecycle_stage: dedup_audit_complete
topic_keys: [dedup, safe_merge, code_ops]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
---

# 40_SAFE_MERGE_CANDIDATES

Candidats à fusion ou consolidation sûre après preuve.

---

## Aucune fusion candidate dans ce lot

Ce GO ne génère pas de fusion de fichiers.

Les actions retenues sont :
- suppression de fichiers sans consommateur (D05, D06) → lot dédié
- création de fichiers manquants (A01) → lot dédié
- correction de classification registre (A03) → faite ici

---

## Lot A01 — plan de création des 22 sanity_check.sh

Ce n'est pas une fusion mais une création de fichiers manquants.

### Template minimal (convention modules/)

```bash
#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"

echo "=== sanity: $(basename "$MODULE_DIR") ==="

# Vérifier la présence de scripts/cmd.sh
[ -f "$MODULE_DIR/scripts/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }

# Vérifier la présence d'un fichier app principal
APP=$(find "$MODULE_DIR/app" -name "*.py" 2>/dev/null | head -1)
if [ -n "$APP" ]; then
    echo "OK: app found — $APP"
else
    echo "WARN: no app/*.py found"
fi

echo "PASS: $(basename "$MODULE_DIR") sanity OK"
```

### Modules à traiter (22 total)

Lot recommandé par groupe logique :

**Groupe 1 — modules openclaw (8)**
```text
modules/configure_openclaw
modules/doctor_openclaw
modules/evidence_openclaw
modules/gateway_openclaw
modules/install_module_openclaw
modules/menu_openclaw
modules/model_provider_openclaw
modules/openclaw_config_modulaire
```

**Groupe 2 — modules opérateurs (5)**
```text
modules/notification_dispatcher
modules/openclaw_operator_bridge
modules/openclaw_tmux_operator
modules/proposition_engine
modules/result_tracker
```

**Groupe 3 — modules trading/engines (4)**
```text
modules/signal_router
modules/trade_executor
modules/trading_lab_v1
modules/trading_realtime_v1
```

**Groupe 4 — modules infrastructure (5)**
```text
modules/datasheet_writer
modules/dev_validation_hub
modules/learning_feeder
modules/localcms
modules/validation_gate
```

### Priorité de création

`modules/validation_gate` et `modules/trading_lab_v1` sont HIGH risk → prioriser
leur sanity_check.sh dans le premier lot.

### Lot GO dédié

```text
GO_CODE_OPS_OPT_TRADING_CHILD_SANITY_CHECK_BATCH_01
```

Scope : créer `sanity_check.sh` pour les 22 modules, par lot de 4–5, avec test
de chaque script avant commit.
