---
doc_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01_HEALTH_CHECK_CONTRACT
doc_type: health_check_contract
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01
status: draft_for_review
lifecycle_stage: child_health_check
parent_go_id: GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01
topic_keys:
  - opt-trading
  - observability
  - health-check
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01/01_HEALTH_CHECK_CONTRACT.md
point_de_reprise: "Définir le contrat minimal de health check par surface d'automation."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01/01_AUTOMATION_MATRIX.md
---

# 01_HEALTH_CHECK_CONTRACT

## 1_CONTRAT MINIMAL UNIFIÉ

```json
{
  "surface": "desk_pro",
  "checked_at": "2026-05-12T00:00:00Z",
  "status": "healthy",
  "details": {
    "service": "active",
    "last_run": "2026-05-12T00:00:00Z",
    "last_run_status": "success"
  },
  "errors": []
}
```

Champs obligatoires :

```text
surface      : identifiant de la surface d'automation
checked_at   : timestamp ISO-8601
status       : healthy | degraded | down | unknown
details      : dict libre spécifique à la surface
errors       : liste des erreurs actives (vide si healthy)
```

## 2_STATUS PAR SURFACE

| Surface | Check clé | healthy si |
|---|---|---|
| Desk Pro | statut systemd + last run | timer actif + dernier run < seuil |
| Bot Vision | statut systemd + inbox/outbox | services actifs + files récents |
| TradingView | listener 8010 + dernier event | listener UP + event récent |
| OpenClaw | ping agent | répond dans le timeout |
| DeepSeek | dernier report généré | report < 24h |
| PERF | /perf/summary accessible | endpoint répond + DB accessible |
| Collectors | status.json présent + fresh | status récent + pas d'erreur critique |
| Repo KG | graph_bundle.json présent | fichier existe + parse OK |
| Bitget Bridge | sanity check | binaire + config OK |
| Ops Menu | scripts accessibles | raccourcis présents |

## 3_PÉRIODICITÉ RECOMMANDÉE

```text
Critique (si down = perte de données) : 5 min
  - PERF, TradingView, Bot Vision

Important (si down = perte de capacité) : 15 min
  - Desk Pro, Collectors

Secondaire (si down = inconvénient) : 1 h
  - OpenClaw, DeepSeek, Repo KG, Bitget Bridge, Ops Menu
```

## 4_IMPLÉMENTATION FUTURE

```text
Chaque surface doit exposer un contrat minimal compatible.
La couche d'observabilité agrégera tous les checks en une vue unique.
Les sanity_* existants sont le point de départ.
```
