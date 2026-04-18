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
updated_at: 2026-04-17
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

7. Politique de supervision
   - GO_RUNTIME_SUPERVISION_POLICY_01

8. Politique de télécommande distante
   - GO_RUNTIME_REMOTE_CONTROL_POLICY_01

9. Outillage de télécommande distante
   - GO_RUNTIME_REMOTE_CONTROL_TOOLING_01

10. Implémentation distante
   - GO_RUNTIME_REMOTE_CONTROL_IMPL_01

### État actuel

- chaîne documentaire runtime et remote-control couverte côté gouvernance
- validation explicite du lot `GO_RUNTIME_REMOTE_CONTROL_TOOLING_01` posée : PASS
- `GO_RUNTIME_REMOTE_CONTROL_IMPL_01` a été repris en tour dédié mais n’a pas lancé d’implémentation réelle
- verdict courant sur l’implémentation distante : PARTIAL
- aucune exécution réelle, aucun smoke réel et aucun patch réel de télécommande runtime ne sont encore stabilisés dans le repo canonique
- les briques réutilisables existent mais restent non intégrées à ce stade

### État de reprise figé pour la télécommande distante

- `GO_RUNTIME_REMOTE_CONTROL_IMPL_01` reste au stade : cadrage validé + reprise d’exécution partielle + NO-GO sur patch réel dans le dernier tour
- la prochaine tranche recommandée est une intégration minimale de lecture / statut / confirmation explicite
- ne pas reprendre le lot implémentation de manière large ; repartir sur une tranche bornée, testable et réversible
- ne pas dépendre des fichiers locaux non suivis pour la reprise ; le présent bloc fait foi côté repo canonique

### Prochain GO requis

GO_RUNTIME_REMOTE_CONTROL_READ_STATUS_IMPL_01

### Règle de continuité

- ne pas ouvrir d’implémentation large de télécommande distante avant une tranche minimale lecture / statut / confirmation
- ne pas modifier les politiques et garde-fous déjà posés sauf incohérence réelle
- journaliser uniquement les changements réels
- reprendre systématiquement depuis ce bloc comme source de vérité runtime

### Point de reprise unique

docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/03_decisions.md
