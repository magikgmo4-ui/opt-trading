---
doc_id: GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01_JOURNAL
doc_type: chantier_journal
repo: opt-trading
project: opt-trading
module:
go_id: GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01
status: active
lifecycle_stage: journal
topic_keys:
  - opt-trading
  - runtime
surface: chantier
source_kind: canonical
updated_at: 2026-04-16
links:
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md
---

# 02_journal_technique — GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01

## 2026-04-16 — Ouverture du chantier
- ouverture du chantier parent runtime
- cadrage validé hors Git puis figé dans le repo
- séparation claire posée : tmux / OpenCode / OpenClaw / Telegram
- décision de ne pas implémenter immédiatement
- décision de découper en sous-chantiers spécialisés

## État actuel
- architecture logique : VALIDÉE
- documentation Git : EN COURS DE STRUCTURATION
- implémentation technique : NON DÉMARRÉE

## Risques identifiés
- confusion entre OpenCode et OpenClaw
- dérive vers implémentation sans conventions
- perte de cohérence entre sessions tmux

## Prochaine étape
- démarrer GO_TMUX_RUNTIME_CONVENTIONS_01
