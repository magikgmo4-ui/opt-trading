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

### D1b — Modèle double cockpit + canon
- Trae = cockpit local de construction (dev / doc / repo)
- le repo Git + docs reste la source canonique de continuité
- les cockpits (local ou distant) ne remplacent pas le canon

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

## ÉTAT DE REPRISE GLOBAL (FIGÉ)

### Chaîne documentaire runtime validée

1. Parent runtime
   - GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01

2. Conventions
   - GO_TMUX_RUNTIME_CONVENTIONS_01

3. Scope orchestration
   - GO_OPENCLAW_COMMAND_SCOPE_01

4. Contrat persistance
   - GO_TMUX_RUNTIME_CONTRACT_01

5. Modes opératoires
   - GO_TMUX_OPENCODE_OPENCLAW_MODES_01

6. Garde-fous transverses
   - GO_RUNTIME_GUARDRAILS_01

### État actuel

- chaîne documentaire validée jusqu’aux garde-fous
- politique de supervision NON encore matérialisée dans le repo
- aucun lot d’implémentation ouvert

### Prochain GO requis

GO_RUNTIME_SUPERVISION_POLICY_01

### Règle de continuité

- ne pas ouvrir de lot d’implémentation avant création de GO_RUNTIME_SUPERVISION_POLICY_01
- ne pas modifier les lots précédents sauf incohérence réelle
- reprendre systématiquement depuis ce bloc comme source de vérité runtime

### Point de reprise unique

docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/03_decisions.md
