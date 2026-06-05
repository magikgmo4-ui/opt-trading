---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
child_go: GO_STRATEGY_IDE_BUNDLE_01
doc_type: ide_bundle_instructions
repo: opt-trading
status: open
created_at: 2026-05-17
surface: doc-only
---

# 90_IDE_BUNDLE_INSTRUCTIONS

---

## 1_OBJECTIF

Fournir un bundle de reprise pour ouvrir le prochain child strategie :

```text
GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
```

---

## 2_CONTEXT_TO_LOAD

Avant d'ouvrir le child SMC/ICT, lire :

```text
docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/00_INITIAL_PROJECT_DOC.md
docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/10_PR_AND_EXISTING_SURFACES_CROSSCHECK.md
docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/20_STRATEGY_CANONICAL_SPEC_SCHEMA.md
docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/40_OBSERVATION_EVENT_EXTENSION.md
docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/99_CLOSEOUT_CRITERIA.md
```

Surfaces a recroiser :

```text
scripts/tmux/sessions/screeners.sh
modules/bot_vision_step2/app/bot_vision_step2.py
modules/localcms/app/main.py
modules/notification_dispatcher/app/events.py
modules/notification_dispatcher/app/dispatcher.py
```

---

## 3_CHILD_OPENING_PROMPT

```text
Tu es dans le repo canonique opt-trading.

Objectif :
ouvrir le child doc-only :
GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01

Parent :
GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01

But :
definir comment SMC/ICT enrichit ObservationEvent comme premier cas
d'application du Canonical Strategy Framework.

Contraintes :
- doc-only
- no runtime mutation
- no live trade
- no Bitget order
- no automatic Google Sheets write
- no Telegram BUY/SELL direct
- no Vision-only decision
- no duplicate pipeline

Strategy seed :
strategy_id = SMC_ICT_CHOCH_BOS_RETEST
setup_type  = SWEEP_CHOCH_BOS_FVG_OB_RETEST

Livrer au minimum :
- 00_INITIAL_PROJECT_DOC.md
- 10_SMC_ICT_SIGNAL_TAXONOMY.md
- 20_OBSERVATION_EVENT_FIELD_MAPPING.md
- 30_BOT_VISION_EVIDENCE_MAPPING.md
- 40_PERF_ENGINE_EVALUATION_PLAN.md
- 50_TELEGRAM_WATCH_SIGNAL_DRAFT.md
- 60_TRADING_LAB_REPLAY_LABELS.md
- 90_CLOSEOUT_CRITERIA.md
```

---

## 4_IMPLEMENTATION_DISCIPLINE

Pour tout child strategie :

1. Commencer par `git status --short --branch`.
2. Verifier la branche attendue.
3. Garder le scope dans `docs/chantiers/<GO_ID>/` et inbox si demande.
4. Ne pas modifier `modules/` depuis un child doc-only.
5. Ne pas modifier d'index global sans justification explicite.
6. Recroiser les PR/surfaces existantes avant d'ecrire le schema.
7. Terminer par `git diff --check`.

---

## 5_SMC_ICT_SPEC_SEED

```json
{
  "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
  "strategy_version": "v0.1.0",
  "setup_type": "SWEEP_CHOCH_BOS_FVG_OB_RETEST",
  "direction": "WATCH_ONLY",
  "signal_source": "bot_vision",
  "evidence_source": [
    "screenshot",
    "vision_summary",
    "journal_daily"
  ],
  "observation_status": "CANDIDATE",
  "perf_status": "UNMEASURED"
}
```

---

## 6_HANDOFF_VERDICT_TARGET

```text
PASS_SMC_ICT_OBSERVATION_SIGNAL_ENRICHMENT_DOC_ONLY_OPENED
```

## RISKS

- À qualifier.
