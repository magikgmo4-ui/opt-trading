---
doc_id: GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01_ELIGIBILITY_CHECK
doc_type: eligibility_check
go_id: GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01
checked_at: 2026-05-30
operator_verdict: PASS_WITH_INFRA_EXCEPTION
---

# 10_ELIGIBILITY_CHECK

Vérification Phase 1 requise avant ouverture du GO (spec section 3 du 00_INITIAL_PROJECT_DOC).

---

## Critères gate

| Critère | Requis | Actuel | État |
|---------|--------|--------|------|
| Date | ≥ 2026-05-30 | 2026-05-30 | PASS |
| Runs total | ≥ 30 | 248 | PASS |
| Jours observation | ≥ 14 | 14 (depuis 2026-05-16) | PASS |
| Kill switch testé | oui | oui | PASS |
| fail_count | 0 | 7 | EXCEPTION (voir ci-dessous) |

## Source des données

```
Path  : data/journal/daily/*.json (248 entrées)
Field : all_ok (bool)
Pass  : 241 / 248 = 97.2 %
Fail  : 7 / 248 = 2.8 %
Start : data/journal/daily/20260516_001.json (2026-05-16)
```

## Analyse des 7 échecs

Tous les 7 échecs sont concentrés sur **2026-05-26** (runs 009 à 015).

Signature commune :
```
tmux  : rc=1 — error connecting to /tmp/tmux-1000/default (No such file or directory)
localcms : unreachable — Connection refused
steps : []  (pipeline non démarré)
duration_s : 0.015  (session avortée immédiatement)
pipeline_duration_s : 0
all_ok : False
```

Cause : infrastructure down ce jour-là (tmux non disponible, localcms non joignable).
Il s'agit de sessions qui n'ont pas démarré — aucune erreur pipeline ni stratégie.
Le pipeline n'a pas produit de signal incorrect, il n'a pas tourné.

## Décision opérateur

```
PASS_WITH_INFRA_EXCEPTION

Motif : les 7 échecs sont des transients d'infrastructure (tmux down un jour),
non des échecs de logique pipeline ou stratégie. 241 runs valides sur 14 jours.
La condition fail_count=0 est acceptée avec cette exception documentée.
```

## Gate ouverte

```
GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01 — branche ouverte le 2026-05-30
Semiauto pilot run_id : pilot_808f90b9
```
