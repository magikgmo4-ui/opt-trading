---
doc_id: GO_OPENCLAW_NEXT_GO_SEQUENCE_AND_IDE_BUNDLE_PLAN_20260426
doc_type: ide_bundle_plan
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-26
topic_keys:
  - openclaw
  - gateway_supervision
  - operator_bridge
  - agents_mapping
  - ide_bundle
  - tmux
  - reprise
search_tags:
  - surface:chantier
  - doc_role:ide_bundle_plan
  - parent:GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
  - bundle:ide
  - sequence:supervision_bridge_mapping
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/12_IDE_BUNDLE_REPRISE_NEXT_GO.md
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/10_GATEWAY_FOREGROUND_PASS_20260426.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/04_OPERATOR_BRIDGE_SPEC.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/09_OPENCLAW_BOUNDARY_CROSSWALK.md
---

# 11_NEXT_GO_SEQUENCE_AND_IDE_BUNDLE_PLAN

## 1_MASTER_TARGET

Préparer la séquence complète post-validation Gateway OpenClaw :

1. supervision tmux stable ;
2. implémentation bridge V1 minimal ;
3. mapping agents / skills / providers avancé.

Ce document sert de bundle IDE documentaire pour exécuter la suite sans dépendre de la session ChatGPT.

## 7_CANONICAL_STATE

État établi avant cette séquence :

- `db-layer` est l'hôte canonique OpenClaw.
- Gateway lancé et validé en foreground sous `openclaw@db-layer`.
- Bind validé : `127.0.0.1:18789` et `[::1]:18789`.
- Mode actuel : foreground, non durable.
- Systemd user non fiable / indisponible dans le contexte courant.
- Bridge spec V1 existe : `04_OPERATOR_BRIDGE_SPEC.md`.
- Crosswalk multi-agents existe côté parent multi-agents.
- Aucune exposition WAN n'est autorisée.

## 4_MASTER_PROJECT_PLAN

### Phase 1 — Stabiliser Gateway sans systemd

Créer un GO enfant pour supervision tmux :

```text
GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01
```

Objectif : lancer et maintenir le Gateway en session tmux contrôlée, sous utilisateur `openclaw`, loopback-only.

### Phase 2 — Implémenter bridge V1 minimal

Créer un GO enfant :

```text
GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01
```

Objectif : créer `modules/openclaw_operator_bridge/` avec contrats, policy, router, renderer, wrappers et tests minimaux.

### Phase 3 — Mapper agents / skills / providers

Créer un GO enfant côté parent multi-agents :

```text
GO_OPT_TRADING_MULTI_AGENTS_CHILD_AGENT_SKILL_PROVIDER_MAPPING_01
```

Objectif : intégrer OpenClaw dans la matrice multi-agents avec rôles stricts : agent, skill, provider, gateway, orchestrator, deployer, prompt generator.

## 5_GO_PLAN — Liste des prochains GO

### GO immédiat recommandé

```text
GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01
```

Rôle : stabiliser Gateway via tmux V1.

### GO suivant

```text
GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01
```

Rôle : implémentation bridge minimale, local-only, read-only au départ.

### GO parallèle doctrine

```text
GO_OPT_TRADING_MULTI_AGENTS_CHILD_AGENT_SKILL_PROVIDER_MAPPING_01
```

Rôle : mapping doctrine multi-agents.

### GO de validation runtime après bridge

```text
GO_OPENCLAW_OPT_TRADING_CHILD_BRIDGE_SMOKE_LOCAL_01
```

Rôle : smoke local `request -> policy -> response`, sans mutation sensible.

### GO futur sécurité

```text
GO_OPENCLAW_OPT_TRADING_CHILD_SECURITY_POLICY_V1_01
```

Rôle : policy détaillée, audit sécurité, allowlist, interdits.

### GO futur remote contrôlé

```text
GO_OPENCLAW_OPT_TRADING_CHILD_REMOTE_ACCESS_TUNNEL_01
```

Rôle : SSH tunnel / WireGuard uniquement, jamais WAN brut.

## 6_FINAL_TARGET

À la fin de la séquence 1→2→3 :

```text
Gateway stable en tmux
Bridge V1 minimal présent
Mapping agents/skills/providers documenté
Tests/smokes locaux passés
Point de reprise propre
```

## 8_VALIDATED_PLAN

Ordre verrouillé :

1. `GATEWAY_SUPERVISION_TMUX_01`
2. `OPERATOR_BRIDGE_IMPL_V1_01`
3. `AGENT_SKILL_PROVIDER_MAPPING_01`
4. `BRIDGE_SMOKE_LOCAL_01`

Ne pas inverser 1 et 2 : le bridge dépend d'un Gateway stable.

## 9_SELECTED_SOLUTION

Approche retenue :

```text
foreground validé -> tmux stable -> bridge V1 read-only -> mapping doctrine -> smokes -> extension contrôlée
```

## 10_SELECTED_SETUP

### tmux Gateway cible

```text
user=openclaw
session=openclaw-gateway
command=openclaw gateway
bind=127.0.0.1
port=18789
log=/tmp/openclaw-1001/openclaw-YYYY-MM-DD.log
```

### Bridge V1 cible

```text
modules/openclaw_operator_bridge/
  README.md
  cmd.sh
  menu.sh
  sanity_check.sh
  app/
  config/
  commands/
  docs/
  tests/
```

### Mapping cible

```text
agent -> rôle conversationnel / exécuteur borné
skill -> capacité encapsulée
provider -> modèle / backend IA
orchestrator -> opt-trading, jamais OpenClaw
prompt_generator -> validated_prompt_factory
deployer -> deploy_module_multi_machine
gateway -> OpenClaw runtime
```

## 11_KEY_DECISIONS

- tmux V1 avant systemd repair.
- Bridge V1 commence read-only.
- Pas de trading live.
- Pas de WAN.
- Pas de secrets dans logs.
- Les commandes sensibles restent refusées.
- Mapping multi-agents après stabilisation Gateway, mais avant extensions.

## 12_INVARIANTS

- OpenClaw ne devient pas source de vérité.
- OpenClaw ne bypass pas `GO_XXXX`.
- Gateway reste loopback-only.
- Bridge refuse shell libre.
- Bridge journalise toute action.
- Toute extension vers remote passe par GO dédié.

## 13_ESTABLISHED

- Gateway fonctionne réellement en foreground.
- Port 18789 fonctionne en loopback.
- Systemd user est le blocage actuel.
- tmux est le plus petit superviseur pragmatique.
- Bridge spec est disponible.
- Crosswalk doctrine/runtime est disponible.

## 14_HYPOTHESIS

- Une session tmux stable suffit pour la phase prototype.
- Le bridge V1 peut commencer sans connexion RPC complexe, avec wrapper CLI et contrats JSON.
- Le mapping agents/skills/providers devra être ajusté après lecture des configs OpenClaw réelles.

## 15_REMAINING_GAP

- Script tmux exact à valider sur `db-layer`.
- Choix du chemin repo local de travail pour implémentation.
- Smoke exact du Gateway après tmux.
- Méthode d'appel du bridge depuis OpenClaw.
- Fichiers config OpenClaw à lire sans secrets.

## 16_TODO

### Prochain GO immédiat

Créer `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01` avec :

- doc cadrage ;
- script run tmux ;
- script status ;
- script stop contrôlé ;
- smoke `ss -ltnp | grep 18789` ;
- invariant loopback.

### GO bridge V1

Créer module minimal :

- `cmd.sh status` ;
- `cmd.sh validate-request` ;
- policy YAML ;
- tests contrat ;
- renderer safe summary.

### GO mapping

Créer côté parent multi-agents :

- `10_AGENT_SKILL_PROVIDER_MAPPING.md` ou prochain index disponible ;
- matrice OpenClaw / workflow_ai / validated_prompt_factory / deploy_module_multi_machine.

## 17_RESUME_POINT

```text
Reprise opérationnelle :
1. Lire 10_GATEWAY_FOREGROUND_PASS_20260426.md.
2. Lire ce fichier 11_NEXT_GO_SEQUENCE_AND_IDE_BUNDLE_PLAN.md.
3. Lancer GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01.
4. Ne pas implémenter bridge tant que tmux supervision n'est pas validée.
5. Après tmux PASS, ouvrir OPERATOR_BRIDGE_IMPL_V1_01.
```

## 18_TO_DOCUMENT

- `OPENCLAW_NEXT_GO_SEQUENCE_20260426`
- `OPENCLAW_IDE_BUNDLE_PLAN_01`
- `OPENCLAW_GATEWAY_TMUX_FIRST_01`
- `OPENCLAW_BRIDGE_IMPL_AFTER_TMUX_01`

## 19_TO_REMEMBER

- Après validation foreground, le prochain GO obligatoire est la supervision tmux du Gateway.
- Le bridge V1 vient après Gateway stable.
- Le mapping agents/skills/providers vient après ou en parallèle doc-only, mais doit référencer la réalité runtime.
