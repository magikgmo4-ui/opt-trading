---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: closeout_criteria
repo: opt-trading
status: draft
created_at: 2026-05-17
surface: doc-only
---

# 99_CLOSEOUT_CRITERIA

---

## 1_CLOSEOUT_TARGET

Le parent est clos si le bundle doc-first fixe :

```text
Canonical Strategy Framework
ObservationEvent enrichment
Shadow/paper evaluation
SMC/ICT as first child
```

---

## 2_REQUIRED_FILES

| Fichier | Statut attendu |
| --- | --- |
| `00_INITIAL_PROJECT_DOC.md` | Present |
| `10_PR_AND_EXISTING_SURFACES_CROSSCHECK.md` | Present |
| `20_STRATEGY_CANONICAL_SPEC_SCHEMA.md` | Present |
| `30_STRATEGY_LIFECYCLE_GATES.md` | Present |
| `40_OBSERVATION_EVENT_EXTENSION.md` | Present |
| `50_LOCALCMS_STRATEGY_VIEW_REQUIREMENTS.md` | Present |
| `60_PERF_ENGINE_STRATEGY_EVALUATION.md` | Present |
| `70_TELEGRAM_WATCH_SIGNAL_PROTOCOL.md` | Present |
| `80_TRADING_LAB_REPLAY_PROTOCOL.md` | Present |
| `85_GOOGLE_SHEETS_EXPORT_MAPPING.md` | Present |
| `90_IDE_BUNDLE_INSTRUCTIONS.md` | Present |
| `99_CLOSEOUT_CRITERIA.md` | Present |
| `docs/index/inbox/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01.md` | Present |

---

## 3_SCOPE_VALIDATION

Le diff doit etre limite a :

```text
docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/**
docs/index/inbox/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01.md
```

Le parent ne doit pas modifier :

```text
modules/**
scripts/**
tests/**
data/**
requirements.txt
GO_INDEX.md
ACTIVE_STREAMS.md
```

---

## 4_CONTENT_VALIDATION

Le bundle doit documenter explicitement :

- PR #524 `ObservationEvent` schema;
- PR #522 product roadmap;
- PR #514 Phase 1 observation;
- PR #513 kill switch + Telegram dry-run;
- PR #512 paper mode expansion;
- PR #510 live readiness doc-only;
- PR #509 LocalCMS metrics dashboard;
- `scripts/tmux/sessions/screeners.sh`;
- `modules/bot_vision_step2/app/bot_vision_step2.py`;
- `modules/localcms/app/main.py`.

---

## 5_INVARIANTS_VALIDATION

Le closeout est bloque si un document autorise :

```text
live trade
Bitget order
automatic Google Sheets write
runtime mutation in parent
duplicate pipeline
strategy without strategy_id
promotion without Perf Engine evidence
Telegram BUY/SELL direct before validation
Vision-only decision
```

---

## 6_REQUIRED_COMMANDS

Validation locale :

```text
git diff --check
git diff --cached --check
git status --short --branch
```

Verification supplementaire :

```text
Only parent docs + inbox entry modified.
```

---

## 7_EXPECTED_VERDICT

```text
PASS_STRATEGY_CANONICAL_FRAMEWORK_PARENT_DOC_ONLY_OPENED
```

---

## 8_NEXT_RESUME_POINT

```text
Reprendre sur :
GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01

Avec :
strategy_id = SMC_ICT_CHOCH_BOS_RETEST
setup_type  = SWEEP_CHOCH_BOS_FVG_OB_RETEST
```
