---
doc_id: GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01_MATRIX
doc_type: capability_matrix
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01
status: draft_for_review
lifecycle_stage: child_matrix
topic_keys:
  - opt-trading
  - automation
  - matrix
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01/01_AUTOMATION_MATRIX.md
point_de_reprise: "Matrice complète des surfaces d'automation."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01/00_CADRAGE.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
---

# 01_AUTOMATION_MATRIX

## 1_DESK PRO AUTOMATION

```text
trigger      : systemd timer → desk_pro_orchestrator
cadence      : configurable (historique 15-60 min)
state        : active (USABLE_LIMITED)
dependencies : venv, modules desk_pro_*, data/desk_runs/
failure_mode : run suivant échoue silencieusement, log dans data/desk_runs/
monitoring   : desk_pro_runner dashboard, sanity checks
human_gate   : non (timer), oui (interprétation dashboard)
gaps         : alerting en cas d'échec, reprise automatique
do_not_auto  : passage d'ordre réel sans validation
```

## 2_BOT VISION

```text
trigger      : watch loop (vision_bot) + timer (bot_vision_step2 send/analyze)
cadence      : polling 2s (vision_bot), 10 min (step2 send), /analyze on-demand
state        : active (USABLE_LIMITED, paire canonique)
dependencies : sftp/inbox, OpenAI API, Telegram token
failure_mode : inbox vide → rien à traiter, API down → analyse muette
monitoring   : systemctl status, Telegram outputs, vision_outbox
human_gate   : non (automatique sauf /analyze Telegram)
gaps         : pas de fallback si OpenAI down, pas d'alerte si pipeline bloqué
do_not_auto  : envoi Telegram automatique sans contrôle de contenu
```

## 3_TRADINGVIEW / WEBHOOK PIPELINE

```text
trigger      : webhook HTTP (TradingView alert)
cadence      : à la demande (déclenché par alerte TV)
state        : active (USABLE_LIMITED)
dependencies : webhook server, webhook_to_perf adapter, desk_pro
failure_mode : webhook silencieux si service down, pas de retry
monitoring   : webhook logs, /perf/event endpoint
human_gate   : non (traitement automatique du signal)
gaps         : retry si échec, confirmation de réception, rate limiting
do_not_auto  : exécution d'ordre réel
```

## 4_OPENCLAW RUNTIME

```text
trigger      : agent (invocation par opérateur ou tâche planifiée)
cadence      : à la demande
state        : active (USABLE_LIMITED, agent/projection)
dependencies : Ollama local, repo opt-trading, permissions SSH
failure_mode : agent bloqué → pas de réponse, erreur silencieuse
monitoring   : logs agent, sanity checks
human_gate   : oui (invocation explicite, validation des actions)
gaps         : pas de supervision autonome, pas de circuit breaker
do_not_auto  : écriture non supervisée dans le repo, accès secret non borné
```

## 5_DEEPSEEK STUDENT

```text
trigger      : manual (cmd-deepseek_*) ou post_change workflow
cadence      : à la demande (daily-ai-report timer possible)
state        : active (transition, KEEP_CANDIDATE)
dependencies : Ollama local, _student_archive/
failure_mode : génération vide, modèle non disponible
monitoring   : logs dans _student_archive/, sanity_deepseek
human_gate   : oui (lecture humaine des roadmaps/reports)
gaps         : pas de scheduling automatique fiable, scripts legacy scripts/student/
do_not_auto  : publication automatique sans relecture
```

## 6_PERF RUNTIME

```text
trigger      : uvicorn service (port 8010), ingestion par POST /perf/event
cadence      : continu (listener) + timer Telegram alerts
state        : active (USABLE_LIMITED)
dependencies : perf.db (modules/perf/data/), desk_pro mount, Telegram token
failure_mode : DB locked → retry, service down → perte d'ingestion
monitoring   : /perf/summary, /perf/ui, Telegram no-activity alerts
human_gate   : non (tracking automatique), oui (interprétation)
gaps         : pas de backup DB automatique, pas de reprise sur crash
do_not_auto  : décision de trading basée uniquement sur PERF
```

## 7_COLLECTORS (DERIVATIVES + SPOT)

```text
trigger      : manual (cmd.sh) ou subprocess (desk_pro_orchestrator)
cadence      : à la demande (pas de timer autonome confirmé)
state        : active (USABLE_LIMITED / KEEP_CANDIDATE)
dependencies : API externes (Coingecko, Binance, Bitget), collectors_core
failure_mode : API rate limit → données manquantes, pas de retry automatique
monitoring   : status.json, manifest.json, sanity checks
human_gate   : oui (lancement manuel ou via desk_pro pipeline)
gaps         : pas de scheduling autonome, pas de retry, pas de fallback provider
do_not_auto  : trading basé sur données non validées
```

## 8_REPO KG

```text
trigger      : manual (cmd.sh) ou via CI
cadence      : à la demande
state        : active (USABLE_NOW, seul produit full)
dependencies : graphe bundle, producer_repo_kg_v1.py
failure_mode : graphe désynchronisé, données manquantes
monitoring   : sanity checks, graph_bundle.json
human_gate   : oui (régénération manuelle)
gaps         : pas de régénération automatique, pas d'incrémental
do_not_auto  : écriture automatique dans le graphe sans validation
```

## 9_SIMEX BITGET BRIDGE

```text
trigger      : manual (cmd.sh) ou subprocess
cadence      : à la demande
state        : active (KEEP_CANDIDATE)
dependencies : venv, Bitget API, PERF runtime
failure_mode : API rate limit, credentials invalides
monitoring   : sanity checks, logs
human_gate   : oui (exécution supervisée)
gaps         : pas de reconnexion automatique, pas de circuit breaker
do_not_auto  : exécution d'ordre réel
```

## 10_OPS MENU HUB

```text
trigger      : manual (menu.sh)
cadence      : à la demande
state        : active (USABLE_LIMITED)
dependencies : aucun (shell uniquement)
failure_mode : shortcut cassé → menu inaccessible
monitoring   : sanity checks
human_gate   : oui (interactif)
gaps         : pas de version non-interactive, pas d'API
do_not_auto  : exécution batch sans confirmation
```
