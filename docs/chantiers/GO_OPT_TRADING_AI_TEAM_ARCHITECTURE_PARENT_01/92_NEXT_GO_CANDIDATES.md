---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01_NEXT_GO_CANDIDATES
doc_type: candidates
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
status: closing
lifecycle_stage: closeout
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 92_NEXT_GO_CANDIDATES — Prochains GO AI Team

## Priorite immediate (Phase 2)

### P0 — GO_OPT_TRADING_AI_TEAM_PATCH_DRAFT_01

**Objectif** : Etendre le runner avec PATCH_DRAFT, le 5e task type manquant de l'Architecture Canon. Permettre au runner d'ecrire un patch draft sur un fichier non sensible hors drafts/, dans une zone explicitement autorisee et bornee.

**Pourquoi** : C'est le dernier task type manquant de l'Architecture Canon. Tous les 4 autres sont deja implementes et smokes.

**Risque** : Le write hors drafts/ doit etre soigneusement borne pour ne pas casser le contrat Strict Workers.

### P1 — GO_OPT_TRADING_AI_TEAM_MODEL_VERIFICATION_01

**Objectif** : Verifier les 6 modeles pending (MiMo-V2, DeepSeek V4, etc.) via smoke READ_INVENTORY et les ajouter au registry models.

**Pourquoi** : Le pool de modeles est actuellement restreint a 1 seul (deepseek-v4-pro). Diversifier permet de tester la robustesse.

### P1 — GO_OPT_TRADING_AI_TEAM_RUNTIME_INTEGRATION_01

**Objectif** : Integrer le runner AI Team dans les surfaces runtime reelles (menu, cmd wrappers, cron/timer si pertinent).

**Pourquoi** : Le runner est actuellement lance manuellement. L'integration runtime permettrait une execution reguliere ou programmee.

## Moyen terme

### P2 — GO_OPT_TRADING_AI_TEAM_SANDBOX_DOCKER_01

**Objectif** : Ajouter un sandbox Docker pour l'execution isolee des workers.

**Pourquoi** : L'Architecture Canon prevoit un sandbox pour les taches a risque. Actuellement tout est doc-only, le sandbox devient necessaire des que PATCH_DRAFT est actif.

### P2 — GO_OPT_TRADING_AI_TEAM_GO_INDEX_CROSS_AUDIT_01

**Objectif** : Croiser le GO_INDEX.md avec l'inventaire reel des chantiers (34 inventories, 12 CLOS, 22 ACTIVE) pour identifier les ecarts et les chantiers orphelins.

**Pourquoi** : L'Analyzer a detecte 34 chantiers mais le GO_INDEX en reference moins. Un croisement systematique ameliorerait la continuite.

### P2 — GO_OPT_TRADING_AI_TEAM_FRAMEWORK_BENCHMARK_01

**Objectif** : Benchmark LangGraph vs CrewAI sur un cas reel opt-trading pour choisir le framework d'orchestration.

**Pourquoi** : L'Architecture Canon ne fige pas le framework. Un benchmark sur cas reel permettrait de decider.

## Long terme

### P3 — GO_OPT_TRADING_AI_TEAM_PARALLEL_CHAIN_01

**Objectif** : Etendre l'Orchestrator pour supporter des chaines paralleles (plusieurs workers simultanes).

### P3 — GO_OPT_TRADING_AI_TEAM_GATEKEEPER_AUTO_01

**Objectif** : Automatiser partiellement le Gatekeeper (blocage automatique des denied_commands, validation pre-merge).

## Priorites resumees

```
P0: PATCH_DRAFT (5e task type)
P1: Model verification + Runtime integration
P2: Sandbox Docker + GO_INDEX cross-audit + Framework benchmark
P3: Parallel chain + Gatekeeper auto
```

## Note sur ClickUp

ClickUp reste differe conformement a la regle etablie dans l'Architecture Canon. Aucun GO enfant ne doit ouvrir ClickUp sans decision explicite du parent.
