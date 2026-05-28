---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01_CONSUMER_MAP
doc_type: dedup_audit
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01
status: open
lifecycle_stage: dedup_audit_complete
topic_keys: [dedup, consumer_map, code_ops]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
---

# 20_CONSUMER_MAP

Carte des consommateurs pour chaque candidat de ce GO.

Méthode : `git grep` sur `*.sh`, `*.yml`, `*.json`, `*.py` hors `docs/chantiers/`.

---

## D05 — execution_engine scripts doublés

### Scripts legacy (`execution_engine_*`)

| Script | Consommateurs hors docs/ | Verdict |
|---|---|---|
| `execution_engine_cmd.sh` | aucun — référencé uniquement par `execution_engine_menu.sh` | AUCUN CONSOMMATEUR EXTERNE |
| `execution_engine_menu.sh` | aucun — self-referential (appelle `execution_engine_cmd.sh`) | AUCUN CONSOMMATEUR EXTERNE |
| `execution_engine_sanity_check.sh` | aucun — appelé par `execution_engine_cmd.sh` et `execution_engine_menu.sh` | AUCUN CONSOMMATEUR EXTERNE |

**Conclusion** : les trois scripts legacy forment un cluster auto-référentiel. Aucun script,
workflow CI, runbook ou module Python ne les appelle depuis l'extérieur.

### Scripts canoniques (`cmd.sh`, `menu.sh`, `sanity_check.sh`)

| Script | Consommateurs prouvés |
|---|---|
| `cmd.sh` | dispatch interne vers `sanity_check.sh`, convention module |
| `sanity_check.sh` | invoqué par `cmd.sh` via `exec bash "$MODULE_DIR/scripts/sanity_check.sh"` |
| `menu.sh` | invoqué par `cmd.sh` via `exec bash "$MODULE_DIR/scripts/menu.sh"` |

**Conclusion** : scripts canoniques fonctionnels et cohérents avec la convention.

---

## D06 — répertoires .bak

### modules/install_module_openclaw.bak_20260314/

| Type de consommateur | Résultat |
|---|---|
| Import Python | aucun |
| Référence dans un script `.sh` actif | aucune (refs dans docs/chantiers historiques uniquement) |
| Référence dans un workflow CI | aucune |
| Référence dans un runbook opérationnel | aucune |
| Décision préexistante | `rm -rf` recommandé dans `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01` |

### modules/ops_wrappers.bak/

| Type de consommateur | Résultat |
|---|---|
| Import Python | aucun |
| Référence dans un script `.sh` actif | aucune |
| Référence dans un workflow CI | aucune |
| Référence dans un runbook opérationnel | aucune |
| Décision préexistante | `SUPPRIMER — dette .bak` dans `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01` |

---

## A03 — modules/router/

| Type de consommateur | Résultat |
|---|---|
| Import Python `from modules.router` | aucun |
| Appel dans un workflow CI | aucun |
| Référence dans `install_shortcuts.sh` | oui — installe `menu-router`, `cmd-router`, `sanity-router` dans `/usr/local/bin` |
| README | explicite : facade CLI wrapper, `actif mais minimal` |

**Conclusion** : `modules/router/` est une surface CLI opératoire (wrappers shell locaux)
sans logique Python. Il installe des commandes `menu-router` et `cmd-router`. Son rôle est
distinct de `modules/engines/router.py`. FALSE_POSITIVE confirmé.

---

## A01 — 22 modules sans sanity_check.sh

Aucune grep requise — il s'agit de fichiers manquants à créer, pas de consommateurs
de fichiers existants.

Convention applicable : chaque module doit avoir `scripts/sanity_check.sh` qui vérifie
la présence des fichiers clés et retourne `PASS` ou `FAIL`.

---

## A04/A05/A06 — validateurs sans test

| Path | Test existant | Grep résultat |
|---|---|---|
| `tools/governance/validate_master_target_continuity.py` | aucun | `git grep` — aucun fichier `test_validate_master_target*.py` |
| `tools/strategy/validate_strategy_registry.py` | aucun | `git grep` — aucun fichier `test_validate_strategy_registry*.py` |
| `docs/ot/trading/schemas/trading_event_v1.schema.json` | aucun | aucun test de validation JSON Schema |
| `docs/ot/trading/schemas/trading_trade_v1.schema.json` | aucun | aucun test de validation JSON Schema |
