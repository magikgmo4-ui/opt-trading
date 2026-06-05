---
doc_id: OPT_TRADING_MULTI_AGENTS_SESSION_REPRISE_GO_ORDER_01
doc_type: reprise_order
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: ready_for_user_confirmation
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - multi_agents
  - reprise
  - go_order
  - openclaw
  - tmux
  - indexation
  - codexoauth
  - closeout
search_tags:
  - surface:chantier
  - doc_role:reprise_order
  - continuity:session_independent
  - go:ordered_reprise
  - governance:multi_agents_doctrine
  - index:local_first
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 8 - Ordre recommande"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/11_SESSION_INDEPENDENCE_VALIDATION.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/10_CROSS_CHANTIERS_OPENCLAW_TMUX_AGENTS_REVIEW.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/INDEX_PATCH.md
  - docs/index/inbox/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01.md
---

# 12_SESSION_REPRISE_GO_ORDER

## 1. Objet

Figer un point de reprise ordonne pour les differents GO apparus ou recroises pendant la session.

But : reprendre sans dependance conversationnelle, sans melanger les chantiers multi-agents, OpenClaw runtime, tmux/OpenCode, indexation et codexoauth.

## 2. GO courant ouvert

### GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01

Statut : `OPEN / ACTIVE DOC-ONLY`.

Branche :

```text
go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
```

Role : parent de canonisation multi-agents.

Surface :

```text
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/
```

Point de reprise primaire :

```text
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md
```

Etat etabli :

- socle GitHub recroise ;
- workflow_ai confirme ;
- validated_prompt_factory confirme ;
- deploy_module_multi_machine confirme ;
- OpenClaw borne comme orchestrateur experimental / provider layer ;
- matrice agents / skills / providers creee ;
- methode local-first + index inbox atomique creee ;
- recroisement avec OpenClaw/tmux/agents documente ;
- session independence validee.

Prochaine action directe :

```text
90_CLOSEOUT_DRAFT.md
```

## 3. GO initialement propose puis remplace

### GO_OPT_TRADING_OPENCLAW_MULTI_AGENT_ORCHESTRATOR_PARENT_01

Statut : `NON OUVERT / SUPERSEDED BY GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`.

Raison : le nom risquait de faire croire que le chantier etait proprietaire de l'implementation runtime OpenClaw.

Decision : ne pas ouvrir sauf besoin futur tres specifique centre OpenClaw, et seulement avec un perimetre runtime clair.

## 4. GO futurs recommandes depuis la session

### GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01

Statut : `RECOMMENDED NEXT GOVERNANCE GO`.

Role : promouvoir la methode parent-local + index inbox atomique + batch d'agregation au niveau gouvernance/matrice.

Declencheur : apres validation utilisateur ou apres closeout draft du parent multi-agents.

Livrables attendus :

- canonisation de `PARENT_STATE.md`, `NEXT.md`, `ACTIVE.md`, `DECISIONS.md`, `INDEX_PATCH.md` ;
- canonisation `docs/index/inbox/<GO_ID>.md` ;
- interdiction du gros `docs/index/INBOX.md` unique ;
- politique post-agregation : `applied_at`, `applied_by_go`, `archive_after_apply`.

### GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01

Statut : `FUTURE BATCH GO`.

Role : appliquer les `INDEX_PATCH.md` et les entrees `docs/index/inbox/<GO_ID>.md` vers les index globaux.

Declencheur : apres canonisation ou validation de la methode inbox.

Surfaces visees :

- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/REPRISE.md`

Regle : a faire localement ou avec outil capable de lire les fichiers complets sans troncature.

### GO_OPENCLAW_CODEXOAUTH_POLICY_QUALIFICATION_01

Statut : `OPTIONAL / CONDITIONAL`.

Role : qualifier `codexoauth`, visible runtime mais hors policy V1 observee.

Declencheur : seulement si on veut savoir si `codexoauth` doit entrer dans policy V1/V2, ou s'il s'agit d'un bridge Codex/OAuth, agent transitoire, ou surface runtime a laisser hors canon.

Contraintes : doc-only / lecture-only au depart ; aucune correction runtime.

## 5. GO existants recroises et leur place

### GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01

Statut : `EXISTING ACTIVE PARENT`.

Role : parent runtime vivant :

- tmux = persistance ;
- OpenCode = production / code engine ;
- OpenClaw = orchestration / control plane ;
- Telegram = interface distante.

Decision : ne pas fusionner avec le parent multi-agents.

### GO_OPENCLAW_CHAIN_03

Statut : `EXISTING OPENCLAW CHAIN DOC`.

Role : chaine operateur OpenClaw : install, config modulaire, gateway, configure, doctor, evidence.

Decision : reference OpenClaw, pas doctrine multi-agents generale.

### GO_OPENCLAW_PROVIDER_POLICY_04

Statut : `EXISTING PROVIDER POLICY`.

Role : policy providers/modeles pour agents OpenClaw.

Decision : policy provider, pas orchestrateur.

### GO_OPENCLAW_POLICY_RUNTIME_ALIGNMENT_05

Statut : `EXISTING DIAGNOSTIC`.

Role : comparer policy V1 et runtime observe.

Decision : diagnostic seulement ; ne corrige pas runtime.

### GO_HERMES_OPENCLAW_BRIDGE_05

Statut : `EXISTING BRIDGE GO`.

Role : premiere preuve bornee Hermes -> OpenClaw -> validation humaine.

Decision : bridge experimental, pas automatisation generale.

### GO_OPENCLAW_STATE_DIR_REPAIR_10

Statut : `EXISTING RUNTIME REPAIR LOCAL`.

Role : reparation locale bornee gateway/state-dir sur db-layer.

Decision : ne pas utiliser comme doctrine multi-agents ; reste runtime repair local.

## 6. Sous-GO runtime connus depuis parent tmux/OpenClaw

A ne pas rouvrir ici, mais a respecter comme surfaces runtime dediees :

```text
GO_TMUX_RUNTIME_CONVENTIONS_01
GO_OPENCLAW_COMMAND_SCOPE_01
GO_TMUX_RUNTIME_CONTRACT_01
GO_TMUX_OPENCODE_OPENCLAW_MODES_01
GO_RUNTIME_GUARDRAILS_01
GO_RUNTIME_SUPERVISION_POLICY_01
GO_RUNTIME_REMOTE_CONTROL_POLICY_01
GO_RUNTIME_REMOTE_CONTROL_TOOLING_01
GO_RUNTIME_REMOTE_CONTROL_IMPL_01
GO_RUNTIME_REMOTE_CONTROL_READ_STATUS_IMPL_01
```

Role : runtime / remote-control / garde-fous, pas doctrine multi-agents transverse.

## 7. Regles d'ordre

### Regle 1 — Fermer ou stabiliser le parent courant avant nouvelle branche

Ne pas ouvrir de nouveau parent tant que `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` n'a pas au moins un closeout draft.

### Regle 2 — Methode indexation avant batch d'agregation

Ne pas lancer `GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01` avant d'avoir valide ou promu la methode inbox/local-first.

### Regle 3 — codexoauth seulement apres closeout multi-agents

Ne pas ouvrir `GO_OPENCLAW_CODEXOAUTH_POLICY_QUALIFICATION_01` avant de fermer ou stabiliser le parent multi-agents, sauf besoin runtime urgent.

### Regle 4 — OpenClaw runtime reste dans ses chantiers dedies

Toute action sur gateway, state-dir, provider runtime, policy runtime ou tmux doit repartir des chantiers OpenClaw/tmux dedies.

### Regle 5 — le parent multi-agents reste doctrine transverse

Pas de mutation runtime, pas de trading live, pas de merge automatique.

## 8. Ordre recommande

### 1. Clore/stabiliser le parent multi-agents

GO :

```text
GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
```

Action :

```text
creer 90_CLOSEOUT_DRAFT.md
```

### 2. Promouvoir la methode parent-local / inbox atomique

GO :

```text
GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01
```

Action :

```text
canoniser la methode dans gouvernance / matrice / architecture
```

### 3. Agreger les index globaux par batch

GO :

```text
GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01
```

Action :

```text
appliquer les INDEX_PATCH.md et docs/index/inbox/<GO_ID>.md vers les index globaux
```

### 4. Qualifier codexoauth si encore pertinent

GO :

```text
GO_OPENCLAW_CODEXOAUTH_POLICY_QUALIFICATION_01
```

Action :

```text
lecture-only, qualifier statut runtime/policy, aucune correction runtime
```

### 5. Revenir au parent runtime seulement si besoin d'execution OpenClaw/tmux

GO existant :

```text
GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01
```

Action :

```text
reprendre selon 03_decisions.md et sous-GO runtime dedies
```

## 9. Reprise courte

Point de reprise immediat :

```text
Branche : go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
Fichier : docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/PARENT_STATE.md
Prochaine action : docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/90_CLOSEOUT_DRAFT.md
```

## 10. Verdict

Le bon ordre est :

```text
1. GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01 -> closeout draft
2. GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01 -> canoniser methode
3. GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01 -> appliquer index globaux
4. GO_OPENCLAW_CODEXOAUTH_POLICY_QUALIFICATION_01 -> optionnel, qualifier codexoauth
5. GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01 -> seulement si execution runtime/tmux/OpenClaw
```

## RISKS

- À qualifier.
