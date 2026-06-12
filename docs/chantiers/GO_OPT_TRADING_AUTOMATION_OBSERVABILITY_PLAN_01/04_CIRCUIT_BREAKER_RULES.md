---
doc_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01_CIRCUIT_BREAKER_RULES
doc_type: circuit_breaker_rules
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01
status: draft_for_review
lifecycle_stage: child_circuit_breaker
parent_go_id: GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01
topic_keys:
  - opt-trading
  - observability
  - circuit-breaker
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01/04_CIRCUIT_BREAKER_RULES.md
point_de_reprise: "Règles de circuit breaker pour les surfaces d'automation."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01/02_ALERTING_PLAN.md
---

# 04_CIRCUIT_BREAKER_RULES

## 1_PRINCIPE

```text
Un circuit breaker coupe une surface d'automation quand elle échoue
de façon répétée, pour éviter :
- les cascades d'erreurs
- le gaspillage de ressources
- la pollution des logs
- les appels API inutiles
```

## 2_RÈGLES GÉNÉRIQUES

```text
CB1. Après 3 échecs consécutifs → couper la surface
CB2. Après 5 min de coupure → tenter un retry automatique
CB3. Si le retry échoue → doubler le délai (5→10→20→40 min, max 1 h)
CB4. Si le retry réussit → réactiver la surface
CB5. Toute coupure > 15 min → alerte CRITICAL
```

## 3_RÈGLES PAR SURFACE

```text
Desk Pro :
  - si 3 runs consécutifs failed → freeze timer + alerte
  - reprise après run manuel réussi

Bot Vision :
  - si OpenAI API down > 15 min → skip analyse, garder capture
  - si inbox vide > 24 h → warning seulement (pas de coupure)

TradingView :
  - si webhook échoue 3x → log erreur, pas de coupure (les alertes TV sont externes)
  - si /perf/event down → buffer local ou drop après 1 h

PERF :
  - si DB locked > 30s → retry (déjà implémenté)
  - si DB corrompue → alert CRITICAL, pas de coupure auto

Collectors :
  - si API rate limit → backoff exponentiel, pas de coupure
  - si 3x failure → alert, passage manuel requis

OpenClaw :
  - si agent ne répond pas → pas de coupure (manuel)
  - si action destructive demandée → gate humaine obligatoire
```

## 4_NE PAS COUPER

```text
- TradingView webhook (source externe, on ne contrôle pas)
- Bot Vision capture (ne pas perdre de screenshots)
- PERF ingestion (données de trading)
- OpenClaw (agent, pas un service automatisé)
```

## 5_IMPLÉMENTATION FUTURE

```text
Un module `circuit_breaker` minimal peut être ajouté :
- stocker l'état dans un fichier JSON local
- exposer status/reset via CLI
- intégrer aux sanity checks existants
```

## RISKS

- À qualifier.
