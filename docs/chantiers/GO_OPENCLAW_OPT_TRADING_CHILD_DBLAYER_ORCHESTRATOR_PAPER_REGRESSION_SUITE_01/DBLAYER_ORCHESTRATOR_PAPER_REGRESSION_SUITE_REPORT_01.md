---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_01_REPORT
doc_type: execution_report
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: completed
lifecycle_stage: execution_report
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-18T17:45
topic_keys:
  - openclaw
  - db-layer
  - orchestrator
  - paper
  - regression
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_01/DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_PLAN_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_01/90_CLOSEOUT.md
---

# DBLAYER_ORCHESTRATOR_PAPER_REGRESSION_SUITE_REPORT_01

## Etat

**PASS** — mini-suite de regression PAPER bornee executee avec succes.

## Prechecks

| Controle | Resultat |
|---|---|
| base locale | `origin/sot/mainline @ 11efec96` (>= `9ef55ca0`) |
| SSH `db-layer` | PASS |
| `hostname` | `db-layer` |
| `whoami` | `ghost` |
| `pwd` | `/home/ghost` |
| `git status` pre-run | clean (`sot/mainline...origin/sot/mainline`) |
| `openclaw --version` | `OpenClaw 2026.3.11 (29dc654)` |
| config example | `CONFIG_OK` |

## Step A — baseline PAPER run

Commande:

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator run --config modules/desk_pro_orchestrator/config/run_config.example.json
```

Resultat:

- run id: `desk_run_20260518_174440`
- mode: `PAPER`
- modules: `11/11 OK`, `0 failed`
- post-run `git status`: clean

## Step B — status/explain

Commandes:

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator status
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator explain
```

Resultat:

- status: `Desk Pro Orchestrator Status: OK`, `Modules Registered: 11`
- explain: ordre pipeline 11 modules confirme

## Step C — sample-run (safe alternative)

Commande:

```bash
python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator sample-run
```

Resultat:

- run id: `desk_run_20260518_174501`
- mode: `PAPER`
- modules: `11/11 OK`, `0 failed`
- post-run `git status`: clean

## Verification sécurité (Step A + Step C)

| Controle | Run A (`174440`) | Run C (`174501`) |
|---|---|---|
| mode | PAPER | PAPER |
| modules_ok/modules_failed | 11/0 | 11/0 |
| actions | `NO_ACTION`, `PREPARE_LONG`, `PREPARE_SHORT` | `NO_ACTION`, `PREPARE_LONG`, `PREPARE_SHORT` |
| actions hors allowlist | aucune | aucune |
| execution_modes | `['PAPER']` | `['PAPER']` |
| secret keys (`api_key`,`secret`,`token`,`password`) | aucun | aucun |

Conclusion sécurité:

- aucun ordre reel detecte
- aucun secret detecte
- aucun sudo
- aucun write hors artefacts PAPER prevus

## RISKS

- À qualifier.
