---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_SANITY_CHECK_BATCH_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_SANITY_CHECK_BATCH_01
parent_go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: closed
lifecycle_stage: done
topic_keys:
  - opt-trading
  - code_ops
  - sanity_check
  - convention
  - modules
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
working_branch: go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
links:
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01/40_SAFE_MERGE_CANDIDATES.md
---

# GO_CODE_OPS_OPT_TRADING_CHILD_SANITY_CHECK_BATCH_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Créer les `sanity_check.sh` manquants dans les 22 modules qui ne respectaient pas
la convention `modules/` définie dans `CLAUDE.md`.

## 6_FINAL_TARGET

22 fichiers créés. Convention module respectée à 100 % pour cmd.sh + sanity_check.sh.

## 7_CANONICAL_STATE

| Champ | Valeur |
|---|---|
| Fichiers créés | 22 `sanity_check.sh` |
| Tous testés | oui (smoke `bash sanity_check.sh` PASS) |
| Modules HIGH risk testés | `validation_gate`, `trading_lab_v1`, `trading_realtime_v1` — PASS |
| Mutation code | ajout uniquement — aucune suppression, aucun changement d'interface |

## Modules couverts

### Groupe 1 — shell-only (template structure)
```text
configure_openclaw       PASS
dev_validation_hub       PASS
doctor_openclaw          PASS
evidence_openclaw        PASS
gateway_openclaw         PASS
install_module_openclaw  PASS
menu_openclaw            PASS
openclaw_config_modulaire PASS
openclaw_tmux_operator   PASS
```

### Groupe 2 — Python (template import check)
```text
datasheet_writer         PASS
learning_feeder          PASS
localcms                 PASS
model_provider_openclaw  PASS
notification_dispatcher  PASS
openclaw_operator_bridge PASS
proposition_engine       PASS
result_tracker           PASS
signal_router            PASS
trade_executor           PASS
```

### Groupe 3 — HIGH risk (template renforcé)
```text
trading_lab_v1           PASS
trading_realtime_v1      PASS
validation_gate          PASS
```

## Templates utilisés

**Shell-only** : vérifie `cmd.sh`, `menu.sh`, `README.md`.

**Python** : vérifie `cmd.sh`, `app/`, fichier principal, puis
`python3 -c "import <module>"`.

**HIGH risk** : idem Python + vérification de fichiers critiques spécifiques
(ex. `guardrails_v1.py`, `trading_lab_v1.py`).

## Verdict

```text
DONE — A01 résolu.
22 sanity_check.sh créés et testés PASS.
```
