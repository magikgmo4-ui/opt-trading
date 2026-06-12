---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_REGISTRY_REGULARIZATION_01
doc_type: gate_decision
strategy_id: xau_session_open_v1
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
---

# 40_GATE_DECISION

## Gate decision : régularisation registry

---

## 1_SITUATION

| Critère | État |
|---|---|
| `strategy_id` défini | Oui (`xau_session_open_v1`) |
| `strategy_version` fixée | Oui (`v0.1.0`) |
| Code runtime existant | Oui (`trading_realtime_v1`, `trading_lab_v1`) |
| Profil YAML existant | Oui (`xauusd_dual_stack_v1.profile.yaml`) |
| Spécification documentaire produite | Oui (ce GO) |
| Entrée registry proposée | Oui |
| Parent GO référencé | Oui |

---

## 2_VERDICT

```text
GATE_PASS
→ xau_session_open_v1 régularisée comme stratégie officielle registrée
→ lifecycle canonique = CANDIDATE
→ lifecycle réel = ACTIVE (inchangé)
→ aucun runtime modifié
```

---

## 3_PROCHAINES_GATES

| Gate | Condition | État |
|---|---|---|
| CANDIDATE → OBSERVED | Premier ObservationEvent avec strategy_id | DÉJÀ FAIT (runtime produit des events) |
| OBSERVED → PAPER_VALIDATED | Perf Engine + 30 runs | FUTUR |
| Promo → MULTI_SIGNAL | Phase 1 valide x2 périodes | FUTUR |
| Promo → LIVE_REVIEW_ONLY | Dossier readiness complet | FUTUR |

Note : le runtime produit déjà des events avec `strategy_id`. La transition
`CANDIDATE → OBSERVED` est considérée comme déjà remplie par l'activité
pré-existante de `trading_realtime_v1`, bien que documentée seulement via
ce GO de régularisation.

## RISKS

- À qualifier.
