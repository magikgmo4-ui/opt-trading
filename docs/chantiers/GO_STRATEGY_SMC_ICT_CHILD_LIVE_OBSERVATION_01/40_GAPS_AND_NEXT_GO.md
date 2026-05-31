---
doc_id: GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01_GAPS_AND_NEXT_GO
doc_type: gaps_and_next_go
go_id: GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01
created_at: 2026-05-30
---

# 40_GAPS_AND_NEXT_GO

---

## Gaps identifiés

### G01 — pilot_runner ne lit pas les specs
Le pilot_runner exécute le contrat et arrête — il ne lit pas les fichiers spec, ne calcule pas
la confidence, ne produit pas de résumé d'activation. L'analyse est faite par l'opérateur.
Ce gap est structurel (REAL_CASE_01). Hors scope de ce GO.

### G02 — ObservationEvent non encore automatisé
Le posting des ObservationEvents est manuel. Il n'existe pas de pipeline qui lit automatiquement
un screenshot bot_vision et produit un ObservationEvent SMC_ICT. C'est un futur GO.

### G03 — Telegram watch signal non branché sur le scoring
La logique `confidence >= 0.60 → Telegram` n'est pas implémentée en runtime. Le signal Telegram
sera envoyé manuellement en phase paper. Hors scope de ce GO.

### G04 — Perf Engine metrics non connectées à SMC_ICT
Les métriques Perf Engine (`80_PERF_ENGINE_METRICS.md`) ne sont pas encore produites pour cette
stratégie. Requis pour la promotion ACTIVE_LIVE. Futur GO.

---

## Prochains GOs

| GO | Périmètre | Gate |
|----|-----------|------|
| `GO_STRATEGY_SMC_ICT_CHILD_PAPER_CLOSEOUT_01` | Fermer la fenêtre paper après 14 jours (≥2026-06-13) + ≥30 ObsEvents + Perf Engine evidence | ≥2026-06-13 |
| `GO_STRATEGY_SMC_ICT_CHILD_ACTIVE_LIVE_01` | Promotion ACTIVE_LIVE si paper gate passée | Après PAPER_CLOSEOUT_01 |
| `GO_STRATEGY_SMC_ICT_CHILD_OBS_EVENT_AUTOMATION_01` | Automatiser le posting ObservationEvent depuis bot_vision | Séparé |

---

## État stratégie post-activation

```
SMC_ICT_CHOCH_BOS_RETEST
  observation_status : ACTIVE_PAPER
  perf_status        : UNMEASURED
  window_start       : 2026-05-30
  window_end         : 2026-06-13 (minimum)
  promotion_gate     : BLOCKED_INSUFFICIENT_SAMPLE
```
