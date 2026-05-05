---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01_ARCHITECTURE_CIBLE
doc_type: architecture_target
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01
status: open
lifecycle_stage: architecture
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_DOC_AUDIT_01/02_journal_technique.md
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
  - docs/agents/strict_workers/MODELS_MATRIX_01.md
  - scripts/ai/workers/tasks.index.json
---

# 01_ARCHITECTURE_CIBLE — AI Team opt-trading

## Synthese

L'architecture AI Team opt-trading est une **equipe d'agents specialises a autonomie etroite**, orchestree, memorisable, securisee, avec validation humaine obligatoire, inspiree du pattern produit Marblism observe et de la doctrine Strict Workers existante.

L'architecture repose sur trois couches :

```
COUCHE A : Orchestration + Memoire  (framework externe, non fige)
COUCHE B : Securite + Execution    (Strict Workers interne)
COUCHE C : Metier + Surfaces       (trading / desk / modules)
```

Cette architecture ne choisit pas de stack finale : elle definit les **primitives indispensables** et les **contrats de couches**, laissant le choix du framework a un GO enfant dedie (MVP).

---

## Axe 1 — Roles agents/workers

### Primitives indispensables

| Role | Responsabilite | Source d'inspiration |
| --- | --- | --- |
| Observer / Collector | Lire des sources externes, extraire des signaux, ne jamais ecrire | Marblism (pattern operateur) + Strict Workers READ_INVENTORY |
| Analyzer / Reasoner | Analyser un contexte borne, proposer un diagnostic ou un patch draft | CrewAI (role+goal) + Strict Workers PATCH_DRAFT |
| Documenter / Reporter | Produire un rapport structure, un closeout draft, un testplan | Strict Workers DOC_DRAFT + CLOSEOUT_DRAFT |
| Orchestrator / Supervisor | Gerer la sequence de taches, les handoffs, les interruptions HITL | AutoGen (Core runtime/messages) + LangGraph (graphe) |
| Gatekeeper / Validator | Verifier les sorties workers, bloquer avant merge/push, valider HITL | Strict Workers (denied_commands) + OpenAI Agents SDK (guardrails) |

### Options confort

- Specialisation fine par module trading (risk, derivatives, signal, position) → role mapping dedie
- Pool de workers redondants par type de tache pour resilience

### Dependances ecosysteme

- CrewAI : si roles + flows retenus, dependance a l'ecosysteme AMP/enterprise pour l'UX produit

---

## Axe 2 — Orchestration

### Primitives indispensables

| Primitive | Description | Source |
| --- | --- | --- |
| Graphe de taches | Workflow defini comme graphe de noeuds/edges | LangGraph (graphe compile) |
| Handoffs | Transfert de contexte entre agents | OpenAI Agents SDK (handoffs) + AutoGen (messages/subscriptions) |
| Etat partage | Contexte accessible entre noeuds du graphe | LangGraph (checkpoints) + CrewAI (etat de flow) |
| Points d'arret HITL | Capacite a suspendre le graphe et attendre validation humaine | LangGraph (interrupts) + CrewAI (@human_feedback) |
| Reprise | Capacite a reprendre un graphe apres interruption | LangGraph (reprise par checkpoint) |
| Routing conditionnel | Branchements logiques dans le graphe | CrewAI (@router, @listen) + LangGraph (edges conditionnels) |

### Options confort

- Orchestration distribuee multi-processus (AutoGen runtime distribue)
- UI de prototypage visuel (AutoGen Studio — non retenu comme prerequisite)

### Dependances ecosysteme

- LangGraph : couplage LangSmith pour observabilite
- AutoGen : complexite des couches multiples (AgentChat vs Core)

---

## Axe 3 — Memoire / Contexte

### Primitives indispensables

| Type de memoire | Portee | Description | Source |
| --- | --- | --- | --- |
| Memoire intra-session | Thread/execution | Etat courant du workflow, checkpointable et reprenable | LangGraph (checkpointers) |
| Memoire inter-sessions | Projet/chantier | Contexte persistant entre executions, store partage | LangGraph (Store) + Strict Workers (required_sections) |
| Memoire courte | Worker | Contexte du prompt + sortie worker (pas de persistance automatique) | Strict Workers (no_memory durable) + OpenAI Agents SDK (sessions) |
| Historique decisions | Projet | Journal canonique des decisions, merge, closeout | opt-trading docs/ convention + GO_INDEX |

### Options confort

- Chiffrement de la persistence (LangGraph chiffrement checkpointers)
- Base vectorielle pour recherche semantique cross-sessions

### Dependances ecosysteme

- LangGraph : persistence via SQLite/Postgres/Cosmos DB
- CrewAI : memoire unifiee dans flows, surface potentiellement couplee AMP

---

## Axe 4 — HITL / Validation humaine

### Primitives indispensables

| Point HITL | Quand | Validation exigee | Source |
| --- | --- | --- | --- |
| Avant execution | Avant lancement d'un worker | Revue du scope + tache index autorisee | Strict Workers (task index + external validation) |
| Avant merge/push | Apres sortie worker | git diff + revue modele fort/humain | Strict Workers (regle de consolidation) |
| Avant decision | Avant closeout PASS | 3 conditions : revue, test, diff | Strict Workers (regle de consolidation) |
| Blocage securite | Si denied_inputs touches | Arret immediat, escalation | Strict Workers (denied_commands) |

### Options confort

- Dashboard de validation (queue de taches en attente d'approbation)
- Escalation automatisee vers canal admin-trading en cas d'anomalie

### Dependances ecosysteme

- CrewAI : `@human_feedback` natif dans les flows
- LangGraph : interrupt + reprise, plus de design applicatif

---

## Axe 5 — Surfaces d'execution

### Primitives indispensables

| Surface | Type | Description | Source |
| --- | --- | --- | --- |
| OpenCode / OpenClaw | Shell agent | Lancement manuel controle, worktree dedie, session bornee | opt-trading runtime actuel |
| Runner securise | Script local | Execution d'un worker dans un couloir ferme, sans write Git | Strict Workers (runner securise) |
| Sandbox agents / Docker | Environnement isole | Execution de code non fiable dans conteneur dedie | OpenAI Agents SDK (sandbox) + AutoGen (Docker executors) |

### Options confort

- Worktree dedie par chantier (deja pratique)
- Surfaces realtime/voice (OpenAI Agents SDK — probablement hors scope trading)

### Dependances ecosysteme

- E2B / Modal pour sandbox code execution (recommande par CrewAI)

---

## Axe 6 — Observabilite / Logs / Smokes

### Primitives indispensables

| Niveau | Quoi | Description | Source |
| --- | --- | --- | --- |
| Worker run | Journal d'execution | Toute sortie worker doit produire 13_ESTABLISHED..VERDICT_DRAFT_ONLY | Strict Workers (required_sections) |
| Smoke | Test READ_INVENTORY | Avant toute promotion worker, smoke read-only obligatoire | Strict Workers (smoke READ_INVENTORY) |
| Diff | git diff reel | Verification que le worker n'a rien ecrit hors perimetre autorise | Strict Workers (regle consolidation) |
| Trace | Graphe de taches | Journal des noeuds executes, temps, erreurs, reprises | LangGraph (LangSmith) + OpenAI Agents SDK (tracing) |

### Options confort

- Dashboard temps reel des workers actifs
- Alertes sur echec smoke ou anomalie diff

### Dependances ecosysteme

- LangSmith pour tracing LangGraph (couplage ecosysteme)
- OpenAI Agents SDK tracing natif

---

## Axe 7 — Securite / Garde-fous

### Primitives indispensables (heritees de Strict Workers)

```text
no_secrets: true
no_env_files: true
no_git_write_ops: true  (git add, commit, push, rebase, merge)
no_runtime_write_by_default: true
requires_external_validation: true
output_status: DRAFT_ONLY
only_verified_models: true
```

### Denied inputs

```text
.env, **/.env, **/*secret*, **/*token*, **/*credential*,
**/id_rsa, **/id_ed25519, **/*.pem, **/*.key
```

### Denied commands

```text
git add, git commit, git push, git rebase, git merge,
rm -rf, chmod -R, chown -R
```

### Options confort

- Garde-fous par module/surface (ex: risk module interdit de lire derivatives strategies)
- Audit trail complet signe par commit

### Dependances ecosysteme

- OpenAI Agents SDK : guardrails natifs
- Sandbox Docker : isolation runtime hardware-level

---

## Axe 8 — Relation AI Team ↔ Strict Workers

Strict Workers n'est **pas un sous-systeme de l'AI Team**. C'est une **couche transversale de securite et d'execution** qui s'applique a tout worker, quel que soit le framework d'orchestration retenu.

| Couche | Framework | Role Strict Workers |
| --- | --- | --- |
| Orchestration + Memoire | A choisir (LangGraph, CrewAI, etc.) | Aucun : Strict Workers n'est pas un orchestrateur |
| Securite + Execution | Strict Workers | Obligatoire : garde-fous, tasks index, denied inputs/commands |
| Modele IA | OpenCode Zen | Strict Workers : matrice modeles + tasks index definissent qui peut faire quoi |
| Metier + Surfaces | opt-trading modules | Aucun : Strict Workers ne definit pas le metier |

### Contrat d'integration

Tout worker IA dans l'AI Team, quel que soit son role metier, DOIT :
1. Etre enregistre dans `tasks.index.json` avec un type de tache autorise
2. Utiliser un modele de `models.registry.json` en statut VERIFIED
3. Passer un smoke READ_INVENTORY avant promotion
4. Respecter les denied_inputs / denied_commands
5. Produire une sortie au format `13_ESTABLISHED..VERDICT_DRAFT_ONLY`
6. Ne jamais ecrire dans Git ou le runtime sans validation externe

---

## Axe 9 — Gaps restants avant MVP

| Gap | Impact | Resolution |
| --- | --- | --- |
| Pas de framework d'orchestration retenu | Bloque l'implementation | GO enfant dedie : benchmark rapide LangGraph vs CrewAI sur cas reel |
| Pas de runner securise implemente | Workers encore manuels via OpenCode | `scripts/ai/workers/` a creer avec runner Python |
| Pas de PATCH_DRAFT execute | Pas de preuve write draft | GO enfant MVP : premier PATCH_DRAFT sur fichier non sensible |
| 6 modeles pending (MiMo-V2, DeepSeek V4, etc.) | Pool restreint | Endpoint verification + smoke READ_INVENTORY |
| Pas de sandbox Docker | Securite execution non testee | MVP peut demarrer sans sandbox (taches doc-only first) |

---

## Axe 10 — Next GO vers setup MVP

```text
GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01

Objectif:
Implementer le premier MVP de l'AI Team avec 3 workers qualifies, sur 1 tache reelle doc-only, sans write runtime, avec smoke validation.

Perimetre:
- Selection de 3 modeles VERIFIED (ex: Qwen3.5 Plus, GLM-5.1, MiniMax M2.5)
- Tache initiale : READ_INVENTORY sur docs/chantiers/ + GO_INDEX.md
- Runner Python simple (pas encore Docker)
- Smoke READ_INVENTORY obligatoire avant validation
- Sortie DRAFT_ONLY
- Closeout draft
```
