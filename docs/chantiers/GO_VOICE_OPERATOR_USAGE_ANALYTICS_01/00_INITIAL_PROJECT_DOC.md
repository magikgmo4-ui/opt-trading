---
doc_id: GO_VOICE_OPERATOR_USAGE_ANALYTICS_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_VOICE_OPERATOR_USAGE_ANALYTICS_01
status: open
created_at: 2026-06-15
---

# GO_VOICE_OPERATOR_USAGE_ANALYTICS_01

## Objet

Instrumenter le Voice Operator pour mesurer l'usage reel, sans collecte invasive, afin de guider les priorites d'evolution.

## 7_CANONICAL_STATE

```text
Voice Operator: complet (Lots A-L merges)
Analytics: inexistant
Dashboard: inexistant
```

## 6_FINAL_TARGET

Dashboard LocalCMS `/voice/analytics` avec tops commandes, latences, profils, sources, TTS.

## 4_MASTER_PROJECT_PLAN

A — Instrumentation: capturer evenements dans `voice_events.jsonl`
B — Agregation: `voice_analytics.py` calcule statistiques
C — Dashboard: `/voice/analytics` dans LocalCMS
D — Rapport: automatique aujourd'hui/7j/30j

## 12_INVARIANTS

- Aucune donnee de trading sensible
- Aucun ordre, aucune mutation metier
- Aucune telemetrie externe
- Tout reste local
