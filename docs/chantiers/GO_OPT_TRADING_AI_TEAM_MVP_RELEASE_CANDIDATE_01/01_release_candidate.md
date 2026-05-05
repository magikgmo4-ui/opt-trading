---
doc_id: GO_OPT_TRADING_AI_TEAM_MVP_RELEASE_CANDIDATE_01_RELEASE_CANDIDATE
doc_type: release_candidate
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_MVP_RELEASE_CANDIDATE_01
status: open
lifecycle_stage: release
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 01_RELEASE_CANDIDATE — AI Team MVP RC1

## Version

**RC1** — Release Candidate 1, 2026-05-05.

Statut : **PASS_LOCAL** (push GitHub PENDING).

## Module

```
modules/ai_team_mvp/
  runner.py                         # Runner securise, stdlib only
  README.md                         # Documentation operateur
  tasks/
    read_inventory.json             # READ_INVENTORY packet
    observer_doc_draft.json         # DOC_DRAFT packet
    analyze_inventory.json          # ANALYZE_INVENTORY packet
    patch_draft.json                # PATCH_DRAFT packet
    orchestrator_chain_v2.json      # ORCHESTRATOR_CHAIN packet (3 etapes)
  registry/
    workers.registry.json           # 5 workers
    tasks.registry.json             # 5 task types + contrat commun
    outputs.registry.json           # 4 outputs + 5 smoke traces
  drafts/
    .observer_output_last.txt       # Sortie brute Observer
    analyzer_*.md                   # Analyses structurelles
    documenter_*.md                 # Brouillons documentaires
    patches/
      analyzer_patch_draft_*.md     # Propositions de patch
```

## Task types (5/5)

| Task Type | Worker | Operations | Write zone | Smoke |
|:----------|:-------|:-----------|:-----------|:------|
| READ_INVENTORY | observer | read | — | 6/6 |
| DOC_DRAFT | documenter | read, write_draft | drafts/ | 6/6 |
| ANALYZE_INVENTORY | analyzer | read, analyze, write_draft | drafts/ | 8/8 |
| PATCH_DRAFT | analyzer | read, analyze, write_patch_proposal | drafts/patches/ | 8/8 |
| ORCHESTRATOR_CHAIN | orchestrator | chain_execute | — | 7/7 |

## Workers (5)

| Worker | Role | Task Types | Writes | Statut |
|:-------|:-----|:-----------|:-------|:-------|
| observer | Observer/Collector | READ_INVENTORY | non | ACTIVE |
| analyzer | Analyzer/Reasoner | ANALYZE_INVENTORY, PATCH_DRAFT | oui (drafts/) | ACTIVE |
| documenter | Documenter/Reporter | DOC_DRAFT | oui (drafts/) | ACTIVE |
| orchestrator | Orchestrator/Supervisor | ORCHESTRATOR_CHAIN | non | ACTIVE |
| gatekeeper | Gatekeeper/Validator | GATEKEEPER_VALIDATE | non | ACTIVE_HUMAN (HITL) |

## Contrat Strict Workers

Applique a tous les workers sans exception.

| Regle | Valeur |
|:------|:------|
| no_secrets | true |
| no_env_files | true |
| no_git_write_ops | true |
| no_runtime_write_by_default | true |
| requires_external_validation | true |
| output_status | DRAFT_ONLY |
| only_verified_models | true |
| modele actif | opencode-go/deepseek-v4-pro |

### Denied inputs (communs)

```
.env, **/.env, **/*secret*, **/*token*, **/*credential*,
**/id_rsa, **/id_ed25519, **/*.pem, **/*.key
```

### Denied commands (communs)

```
git add, git commit, git push, git rebase, git merge,
git diff, git apply, patch,
rm -rf, chmod -R, chown -R
```

## Interdits permanents

1. **Aucun git write depuis le runner** (git add, commit, push, rebase, merge).
2. **Aucune application automatique de patch** (PATCH_DRAFT = proposal only).
3. **Aucun acces aux secrets** (denied_inputs).
4. **Aucune ecriture hors drafts/** ou **drafts/patches/**.
5. **Aucune ecriture runtime trading**.
6. **Aucune ouverture ClickUp** sans GO dedie.
7. **Aucun drop/pop du stash reseau_ssh** avant push confirme.

## Artefacts reutilises (non recrees)

| Artefact | Role |
|:---------|:-----|
| Strict Workers (remote) | Securite/execution obligatoire |
| Architecture Canon AI Team | Structure cible (3 couches, 5 roles) |
| validated_prompt_factory | Standardisation prompts |
| Multi-Agents Canon Parent | Doctrine multi-agent |

## Chemin parcouru

```
DOC_AUDIT → ARCHITECTURE_CANON → BUNDLES_REUSE → SETUP_MVP
→ OBSERVER_DOC_DRAFT → MVP_V2_ORCHESTRATOR_ANALYZER
→ REGISTRY_CONSOLIDATION → PARENT_CLOSEOUT → PATCH_DRAFT
→ MVP_RELEASE_CANDIDATE  ← ici
```

## Prochaines etapes possibles

1. **Push GitHub** — quand auth OK.
2. **Model verification** — 6 modeles pending a verifier.
3. **Runtime integration** — wrappers cmd/menu pour le runner.
4. **Sandbox Docker** — isolation pour les taches a risque.
5. **Framework benchmark** — LangGraph vs CrewAI sur cas reel.
6. **Apply patch manuel** — premier patch applique sous controle humain.

## Resume

```
AI TEAM MVP RC1
5/5 task types implementes
5 workers (dont gatekeeper HITL)
35/35 smokes cumules PASS
0 denied inputs (cumul)
0 git write ops (cumul)
Strict Workers respecte
PATCH_DRAFT = proposal only
PASS_LOCAL — PUSH_PENDING_AUTH
```
