---
doc_id: GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01_PLAN
doc_type: chantier_plan
repo: opt-trading
project: opt-trading
module:
go_id: GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01
status: active
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - runtime
  - tmux
  - opencode
  - openclaw
  - telegram
surface: chantier
source_kind: canonical
updated_at: 2026-04-16
links:
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md
---

# 01_plan — GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01

## But du plan
- but : structurer le runtime opératoire autour de `tmux + OpenCode + OpenClaw + Telegram`
- principe : partir du cadre validé et descendre par sous-chantiers sans dériver vers l’implémentation immédiate
- ordre retenu : cadrage parent → plan parent → sous-chantiers spécialisés → implémentation ultérieure

## Étapes retenues
1. figer les conventions d’usage (qui fait quoi entre les briques)
2. définir le périmètre et les règles d’orchestration OpenClaw
3. formaliser le contrat runtime `tmux`
4. formaliser les modes opératoires (dev, job long, debug, remote)
5. poser les garde-fous pour éviter dérive et incohérences

## Découpage en sous-chantiers
- GO_TMUX_RUNTIME_CONVENTIONS_01 → conventions d’usage
- GO_OPENCLAW_COMMAND_SCOPE_01 → scope et règles OpenClaw
- GO_TMUX_RUNTIME_CONTRACT_01 → contrat runtime tmux
- GO_TMUX_OPENCODE_OPENCLAW_MODES_01 → modes opératoires
- GO_RUNTIME_GUARDRAILS_01 → garde-fous

## Zones de travail
- `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/`
- futurs dossiers dédiés pour chaque sous-chantier

## Validations prévues
- cohérence stricte avec le cadrage parent
- séparation claire des rôles (tmux / OpenCode / OpenClaw / Telegram)
- absence d’ambiguïté sur les responsabilités
- absence de mélange entre orchestration et production

## Point de reprise
Le prochain travail démarre sur :
**formalisation des conventions d’usage (GO_TMUX_RUNTIME_CONVENTIONS_01)**
