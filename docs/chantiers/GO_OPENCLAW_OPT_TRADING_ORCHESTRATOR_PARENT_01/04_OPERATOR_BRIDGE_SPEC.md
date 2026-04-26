---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_SPEC_01
doc_type: bridge_spec
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_SPEC_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: open
lifecycle_stage: spec
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-26
topic_keys:
  - openclaw
  - operator_bridge
  - opt-trading
  - orchestrator
  - gateway
  - security
  - validation
  - go_workflow
  - audit
search_tags:
  - surface:chantier
  - doc_role:bridge_spec
  - parent:GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
  - child:GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_SPEC_01
  - bridge:openclaw_operator_bridge
  - boundary:openclaw_to_opt_trading
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/09_OPENCLAW_BOUNDARY_CROSSWALK.md
  - workflow_ai/WORKFLOW.md
  - modules/validated_prompt_factory/README.md
  - docs/deploy_module_multi_machine_continuity.md
---

# GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_SPEC_01

## 1_MASTER_TARGET

Spécifier le bridge contrôlé entre OpenClaw et `opt-trading`.

Objectif : permettre à OpenClaw d'agir comme couche opérateur / interface / agent runner sans devenir source de vérité, sans contourner les GO_XXXX, sans exécuter de shell libre et sans modifier les modules sensibles hors validation.

## 3_INITIAL_NEED

Après recroisement avec le parent multi-agents, le prochain point critique est le bridge technique :

```text
OpenClaw -> demande opérateur -> bridge -> validation -> action opt-trading -> preuve -> retour OpenClaw
```

## 4_MASTER_PROJECT_PLAN

1. Définir les frontières du bridge.
2. Définir le contrat JSON d'entrée.
3. Définir le contrat JSON de sortie.
4. Définir les états autorisés.
5. Définir la whitelist de commandes.
6. Définir le modèle de validation.
7. Définir la journalisation.
8. Définir les refus obligatoires.
9. Préparer l'audit runtime `db-layer` avant implémentation.
10. Préparer le futur module `modules/openclaw_operator_bridge/`.

## 5_GO_PLAN

Parent : `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`

Child : `GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_SPEC_01`

Type : spec / doc-only.

Aucune implémentation dans ce GO.

## 6_FINAL_TARGET

Livrable : une spécification suffisante pour ouvrir ensuite un GO d'implémentation minimal, testable et sécurisé.

## 7_CANONICAL_STATE

- OpenClaw est opérateur / interface / agent runner.
- `opt-trading` reste orchestrateur canonique.
- `workflow_ai` reste couche de gates.
- `validated_prompt_factory` reste couche de génération de prompts.
- `deploy_module_multi_machine` reste couche logistique.
- Les modules `opt-trading` restent les surfaces d'exécution.
- Le bridge est la frontière unique entre OpenClaw et les actions contrôlées.

## 8_VALIDATED_PLAN

Le bridge doit être conçu en deux niveaux :

### Niveau A — Intake contrôlé

Reçoit les intentions OpenClaw sous forme structurée.

### Niveau B — Execution router

Ne route que vers des commandes explicitement autorisées.

Aucun passage direct vers shell libre.

## 9_SELECTED_SOLUTION

Architecture retenue :

```text
OpenClaw Channel
  -> Gateway
  -> Bridge Intake
  -> Policy Guard
  -> GO Router
  -> Command Whitelist
  -> Module Executor
  -> Proof Logger
  -> Response Renderer
```

## 10_SELECTED_SETUP

Structure future recommandée :

```text
modules/openclaw_operator_bridge/
  README.md
  cmd.sh
  menu.sh
  sanity_check.sh
  app/
    __init__.py
    bridge.py
    intake.py
    policy.py
    router.py
    executor.py
    proof.py
    renderer.py
  config/
    allowed_commands.yaml
    policy.yaml
    machines.yaml
  commands/
    status.yaml
    audit.yaml
    doc_only.yaml
  docs/
    CONTRACT.md
    SECURITY.md
    EXAMPLES.md
  tests/
    test_policy.py
    test_router.py
    test_contract.py
```

## 11_KEY_DECISIONS

- Le bridge accepte seulement des requêtes structurées.
- Le bridge refuse les commandes libres.
- Le bridge journalise tout.
- Le bridge ne modifie pas `admin-trading` sans GO validé.
- Le bridge ne déclenche pas de trading live.
- Le bridge ne charge pas de skill tiers non audité.
- Le bridge peut répondre `REFUSED`, `NEEDS_VALIDATION`, `READY`, `EXECUTED`, `FAILED`.

## 12_INVARIANTS

- Pas de shell direct.
- Pas de secrets dans les logs.
- Pas de commande destructive sans validation.
- Pas de mutation runtime depuis un groupe Telegram non validé.
- Pas de bypass de `workflow_ai`.
- Pas d'exécution réelle avant audit `db-layer`.
- Pas de confusion entre audit, doc-only, patch, deploy et trading.

## 13_ESTABLISHED

### Rôle du bridge

Le bridge transforme une demande opérateur en demande `opt-trading` validable.

Il ne décide pas la stratégie, il applique une politique.

### Surfaces autorisées au départ

| Domaine | Autorisé V1 | Remarque |
| --- | --- | --- |
| status repo | oui | lecture seule |
| audit runtime | oui | lecture seule |
| génération doc | oui | doc-only |
| création GO doc-only | oui | avec validation |
| patch code | non par défaut | nécessite GO dédié |
| deploy | non par défaut | nécessite GO dédié |
| trading live | interdit | hors V1 |
| secrets | interdit | jamais affichés |

## 14_HYPOTHESIS

- Un format JSON minimal suffit pour V1.
- Les commandes pourront être décrites en YAML.
- Le renderer pourra produire des réponses compatibles Telegram.
- Le logger pourra écrire dans `docs/chantiers/<GO_ID>/` ou `logs/openclaw_operator_bridge/` selon le type d'action.

## 15_REMAINING_GAP

- État réel OpenClaw sur `db-layer`.
- Emplacement exact des logs OpenClaw.
- Auth réelle configurée.
- Mode d'appel concret depuis OpenClaw vers le bridge.
- Choix final Python vs shell wrapper.
- Contrat de stockage des preuves.

## 16_TODO

### Contrat JSON entrée V1

```json
{
  "source": "openclaw",
  "channel": "telegram|cli|tmux|unknown",
  "actor": "operator_id_or_alias",
  "intent": "status|audit|doc|go|patch|deploy|trade",
  "go_id": "GO_...|null",
  "target_machine": "db-layer|admin-trading|student|local|null",
  "requested_action": "short_action_name",
  "payload": {},
  "validation": {
    "mode": "read_only|needs_go|needs_human|forbidden",
    "confirmed": false
  }
}
```

### Contrat JSON sortie V1

```json
{
  "status": "REFUSED|NEEDS_VALIDATION|READY|EXECUTED|FAILED",
  "reason": "human_readable_reason",
  "go_id": "GO_...|null",
  "proof_ref": "path_or_null",
  "next_action": "next_go_or_operator_step",
  "safe_summary": "message_for_channel"
}
```

### États obligatoires

| État | Sens |
| --- | --- |
| `REFUSED` | interdit par invariant |
| `NEEDS_VALIDATION` | action possible mais validation manquante |
| `READY` | préconditions satisfaites, pas encore exécuté |
| `EXECUTED` | action exécutée avec preuve |
| `FAILED` | action échouée avec raison |

### Whitelist initiale

```yaml
allowed_intents:
  status:
    mode: read_only
  audit:
    mode: read_only
  doc:
    mode: needs_go
  go:
    mode: needs_human
forbidden_intents:
  - trade
  - secrets
  - unrestricted_shell
  - destructive_ops
```

## 17_RESUME_POINT

Reprise :

```text
Parent OpenClaw : GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
Child spec bridge : GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_SPEC_01
Statut : spec doc-only créée
Next recommandé : audit réel db-layer avant implémentation
Puis : mapping agents/skills/providers avancé côté parent multi-agents
```

## 18_TO_DOCUMENT

- `OPENCLAW_OPERATOR_BRIDGE_CONTRACT_V1`
- `OPENCLAW_POLICY_GUARD_V1`
- `OPENCLAW_COMMAND_WHITELIST_V1`
- `OPENCLAW_PROOF_LOGGER_V1`

## 19_TO_REMEMBER

- Le bridge OpenClaw doit refuser tout shell libre.
- Le bridge doit retourner des états explicites.
- L'audit `db-layer` précède l'implémentation.
- Le mapping agents/skills/providers doit référencer cette spec.
