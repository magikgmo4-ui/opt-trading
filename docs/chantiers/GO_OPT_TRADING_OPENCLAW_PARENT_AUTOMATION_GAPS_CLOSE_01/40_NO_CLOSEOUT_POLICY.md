---
doc_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01_NO_CLOSEOUT_POLICY
doc_type: no_closeout_policy
repo: opt-trading
project: opt-trading
module: automation
go_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
lifecycle_stage: parent_gap_control
topic_keys:
  - no_closeout
  - parent_guard
  - automation
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/40_NO_CLOSEOUT_POLICY.md
point_de_reprise: "NO_CLOSEOUT_UNTIL_ALL_GAPS_PASS"
updated_at: 2026-05-20
---

# 40_NO_CLOSEOUT_POLICY — politique de non-fermeture

## Règle principale

Ce parent ne doit pas être fermé avant que tous les gaps listés dans `10_GAPS_REGISTER.md` et `30_CHECKLIST_MASTER.md` soient en `PASS_WITH_EVIDENCE`.

## Interdictions

Il est interdit de fermer ce parent si :

- un gap est `OPEN` ;
- un gap est `PARTIAL` ;
- un gap est `DRAFT_ONLY` ;
- un gap est `HYPOTHESIS` ;
- un gap n'a pas d'evidence ref ;
- un GO enfant critique n'est pas livré ;
- un test est seulement théorique ;
- une app externe n'a pas de contrat ;
- un worker n'a pas de permission matrix ;
- un write path n'a pas de HITL gate ;
- un secret ou scope n'est pas cadré ;
- une action trading live est implicite ou non contrôlée.

## Closeout autorisé seulement si

```text
ALL_GAPS_CLOSED_WITH_EVIDENCE = true
CHECKLIST_MASTER_COMPLETE = true
NO_DRAFT_ONLY_REMAINING = true
NO_UNGATED_WRITE_PATH = true
NO_EXTERNAL_APP_UNCONTRACTED = true
NO_SIGNAL_LIVE_ORDER_PATH = true
```

## Verdict courant

```text
CLOSEOUT_ALLOWED: NO
CURRENT_REASON: parent opening only; gaps not closed
```

## Prochain fichier closeout

`90_CLOSEOUT.md` ne doit pas être créé maintenant.

Il pourra être créé seulement quand `30_CHECKLIST_MASTER.md` prouve la fermeture complète.
