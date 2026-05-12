---
doc_id: GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01_GAPS_AND_RISKS
doc_type: gaps_and_risks
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01
status: draft_for_review
lifecycle_stage: child_gaps
topic_keys:
  - opt-trading
  - automation
  - gaps
  - risks
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01/03_GAPS_AND_RISKS.md
point_de_reprise: "Gaps et risques par surface d'automation."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01/01_AUTOMATION_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01/02_TRIGGER_MAP.md
---

# 03_GAPS_AND_RISKS

## 1_GAPS TRANSVERSAUX

```text
G1. pas de health dashboard unifié pour toutes les surfaces d'automation
G2. pas d'alerting centralisé en cas d'échec d'un timer/service
G3. pas de circuit breaker automatique (arrêt si erreur en cascade)
G4. pas de rate limiting global (API externes)
G5. pas de backup automatique des artefacts critiques
G6. pas de runbook automatisé de reprise
```

## 2_GAPS PAR SURFACE

```text
Desk Pro :
  - pas d'alerting en cas d'échec de run
  - pas de reprise automatique

Bot Vision :
  - pas de fallback si OpenAI down
  - pas d'alerte si pipeline inbox vide trop longtemps

TradingView :
  - pas de retry si webhook échoue
  - pas de confirmation de réception

OpenClaw :
  - pas de supervision autonome
  - pas de circuit breaker

DeepSeek :
  - scheduling non fiable
  - scripts legacy à migrer

PERF :
  - pas de backup DB automatique
  - pas de reprise sur crash

Collectors :
  - pas de scheduling autonome
  - pas de retry / fallback provider

Repo KG :
  - régénération manuelle uniquement
  - pas d'incrémental

Simex Bitget Bridge :
  - pas de reconnexion automatique
  - pas de circuit breaker
```

## 3_RISQUES

```text
R1. Dépendance aux API externes sans fallback → silence en cas de panne
R2. Timers sans heartbeat → on ne sait pas si ça tourne
R3. Pas de politique de retry uniforme → comportement incohérent
R4. Services manuels ayant un fort potentiel d'automation → sous-utilisation
R5. Absence de matrice partagée → duplication d'effort ou angles morts
```

## 4_NEXT_GO

```text
GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01
```

But :

```text
Définir un plan d'observabilité unifié pour toutes les surfaces d'automation :
health checks, alerting, dashboard, circuit breakers.
```
