---
doc_id: GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
module:
go_id: GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01
status: active
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - runtime
surface: chantier
source_kind: canonical
updated_at: 2026-04-16
links:
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md
---

# 03_decisions — GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01

## Décisions structurantes

### D1 — Architecture runtime retenue
- tmux = persistance
- OpenCode = production
- OpenClaw = orchestration
- Telegram = interface distante

### D2 — Nature du système
- le système est considéré comme un runtime vivant continu
- on sort du modèle session locale IDE

### D3 — Découpage en sous-chantiers
- le parent ne descend pas en implémentation
- chaque responsabilité devient un sous-chantier dédié

### D4 — Ordre de travail
1. conventions d’usage
2. orchestration OpenClaw
3. contrat tmux
4. modes opératoires
5. garde-fous

### D5 — Canonisation différée
- ce parent est volontairement ouvert et structurant
- la canonisation fine (naming, uniformisation totale) est reportée

## Points stabilisés
- séparation des rôles validée
- architecture validée
- point de reprise fixé

## Points ouverts
- niveau d’autonomie OpenClaw
- règles exactes de delegation OpenCode
- discipline tmux (sessions / fenêtres)
