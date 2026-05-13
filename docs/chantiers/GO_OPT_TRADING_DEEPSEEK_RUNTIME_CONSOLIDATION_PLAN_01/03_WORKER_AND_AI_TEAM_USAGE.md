---
doc_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01_WORKER_AND_AI_TEAM_USAGE
doc_type: usage_doc
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01
status: draft_for_review
lifecycle_stage: child_usage
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01
topic_keys:
  - opt-trading
  - deepseek
  - openclaw
  - workers
  - ai-team
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01/03_WORKER_AND_AI_TEAM_USAGE.md
point_de_reprise: "Documenter l'usage DeepSeek par OpenClaw, AI Team et workers."
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01/02_RUNTIME_CONSOLIDATION_PLAN.md
---

# 03_WORKER_AND_AI_TEAM_USAGE

## 1_CE QUE DEEPSEEK PEUT FAIRE

```text
- generer des roadmaps par module (thinking + response)
- produire des rapports AI quotidiens (daily-ai-report)
- repondre a des prompts via Ollama local
- analyser du contenu documentaire (post_change workflow)
- servir de backend LLM pour OpenClaw (mode agent)
- archiver les sorties dans _student_archive/
```

## 2_CE QUI RESTE MANUEL

```text
- lancement des roadmaps
- lecture et interpretation des rapports
- validation des analyses produites
- installation et configuration du hub (admin-trading)
- application des patches deepseek_hub
```

## 3_CE QUI EST INTERDIT

```text
- execution non supervisee d'actions destructives
- modification du repo sans validation humaine
- acces aux secrets/credentials
- publication automatique de rapports sans relecture
- remplacement d'un operateur humain pour les decisions
```

## 4_LIEN AVEC OPENCLAW

```text
OpenClaw peut utiliser DeepSeek comme backend LLM local :
- deepseek_hub fournit les commandes unifiees
- OpenClaw invoque cmd-deepseek_hub pour les roadmaps
- les sorties sont archivees et lisibles par l'operateur

Regle : OpenClaw est un consommateur de DeepSeek, pas son controleur.
DeepSeek reste un service independant appele par l'agent.
```

## 5_LIEN AVEC AI TEAM / WORKERS

```text
post_change workflow :
  - declenche cmd-deepseek_response roadmap_module
  - declenche cmd-deepseek_thinking roadmap_module
  - les sorties alimentent la documentation automatique

Workers AI Team :
  - peuvent utiliser DeepSeek pour generer des analyses
  - doivent respecter le modele d'appel : cmd-* > menu-* > sanity-*
  - les sorties doivent etre validees avant usage
```

## 6_LIEN AVEC LA MATRICE AUTOMATION

```text
DeepSeek est cartographie dans la matrice automation (#327) :
  trigger      : manual + workflow
  state        : active (transition, KEEP_CANDIDATE)
  human_gate   : oui (lecture humaine obligatoire)
  gaps         : scheduling non fiable, scripts legacy
  do_not_auto  : publication automatique sans relecture
```
