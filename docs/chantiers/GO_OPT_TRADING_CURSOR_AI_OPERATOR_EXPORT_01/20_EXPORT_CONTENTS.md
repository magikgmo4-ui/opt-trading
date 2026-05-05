---
doc_id: GO_OPT_TRADING_CURSOR_AI_OPERATOR_EXPORT_01_20_EXPORT_CONTENTS
doc_type: chantier/export_contents
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/operator-export/EXPORT_MANIFEST.json
---

# 20_EXPORT_CONTENTS

## Inventaire detaille

### Bundles actifs cursor-ai

| Bundle | Emplacement | Fichiers |
| --- | --- | --- |
| Claude artifacts operator pack | `bundles/claude-artifacts/` | 6 (README, PROMPT_TEMPLATES, REPRISE_TEMPLATE, NO_COMMIT_RULES, CHECKLIST_EXECUTION, manifest.json) |
| Operator export pack | `bundles/operator-export/` | 4 (README, EXPORT_MANIFEST, HANDOFF, CHECKLIST_VERIFICATION) |
| Workflow bundles | `bundles/` | ACTIVE_WORKFLOW, BUNDLE_TYPES, OPERATOR_FLOW, NO_RUNTIME_NO_SENSITIVE_RULES |
| Reprise | `bundles/` | CURSOR_AI_OPERATOR_REPRISE_PACKET.md |
| Index | `bundles/` | README.md (8 bundles indexes) |

### GO sequence merges

| # | GO | PR | Dossier |
| --- | --- | --- | --- |
| Plan | Parent operational plan | #205 | `GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01/` |
| 1 | Claude artifacts operator pack | #206 | `GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01/` |
| 2 | Bundles workflow actif | #207 | `GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01/` |
| 3 | Alert webhook pre-admin gate spec | #208 | `GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01/` |
| 4 | Operator reprise packet | #209 | `GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01/` |
| A | Alert webhook test safe | #210 | `GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01/` |
| B | Bundles maintenance | #211 | `GO_OPT_TRADING_CURSOR_AI_BUNDLES_MAINTENANCE_01/` |

### Fichiers de routage

| Fichier | Role |
| --- | --- |
| `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` | Routage machine |
| `bundles/CURSOR_AI_OPERATOR_REPRISE_PACKET.md` | Reprise rapide |

## Ordre de lecture recommande

1. `bundles/operator-export/README.md` — point d'entree.
2. `bundles/CURSOR_AI_OPERATOR_REPRISE_PACKET.md` — reprise rapide.
3. `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` — bloc CURSOR_AI.
4. `bundles/claude-artifacts/README.md` — pack operateur.
5. `bundles/ACTIVE_WORKFLOW.md` — workflow Bundles.
6. GO sequence dans l'ordre (plan parent → 1 → 2 → 3 → 4).
