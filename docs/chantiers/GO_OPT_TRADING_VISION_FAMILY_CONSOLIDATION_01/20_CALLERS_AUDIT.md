---
doc_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01_CALLERS_AUDIT
doc_type: callers_audit
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - vision
  - callers
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/10_FAMILY_INVENTORY.md
---

# 20_CALLERS_AUDIT

## Regle de lecture

Ce lot distingue :

- callers directs non-documentaires
- ancrages canonico-documentaires de reprise

## 1. Callers de `bot_vision`

### Directs non-documentaires constates

| Caller | Type | Preuve | Lecture |
| --- | --- | --- | --- |
| `scripts/run_bot_vision_headless_capture.sh` | runtime wrapper | pointe `modules/bot_vision/headless_capture` | caller actif mais borne a `headless_capture`, pas au `step1` |
| `scripts/tmux/sessions/screeners.sh` | ops legacy | lance `bash modules/bot_vision/cmd.sh run` | caller historique residuel, non aligne avec la paire canonique |
| `modules/bot_vision/headless_capture/scripts/install_systemd.sh` | install runtime | installe les unites `bot-vision-headless-capture.*` | auto-reference de sous-surface active |

### Conclusion

- aucun caller direct non-documentaire ne prouve `bot_vision` comme survivant famille complet
- les callers actifs visent soit `headless_capture`, soit un flux legacy encore non nettoye

## 2. Callers de `bot_vision_step2`

### Directs non-documentaires constates

| Caller | Type | Preuve | Lecture |
| --- | --- | --- | --- |
| `config/machine_runtime_map.yml` | canon runtime fleet | `bot_vision_step2.service`, timers, venv, env | runtime primaire reconnu sur `admin-trading` |
| `modules/runtime_health/config/runtime_health.yml` | supervision | surveille service/timers/venv/logs | surface sante active |
| `modules/runtime_health/healthcheck.py` | supervision executable | service/timers/env/logs `bot_vision_step2` | caller operatoire actif |
| `deploy/systemd/opt-trading-runtime-health.service` | integration systemd | charge `modules/bot_vision_step2/config/bot_vision.env` | dependance indirecte de supervision |
| `modules/vision_bot/scripts/vision_runtime_cmd.sh` | wrapper unifie | `analyze-latest`, `send-latest`, `prune-old` delegues a `bot_vision_step2` | compose la paire canonique |
| `modules/vision_bot/scripts/vision_runtime_sanity.sh` | wrapper unifie | verifie aussi `bot_vision_step2` | paire canonique explicite |

### Conclusion

- `bot_vision_step2` est le module le plus fortement consomme par la supervision runtime
- il est operatoire aujourd'hui, mais comme composant d'analyse, pas comme survivant unique autosuffisant

## 3. Callers de `vision_bot`

### Directs non-documentaires constates

| Caller | Type | Preuve | Lecture |
| --- | --- | --- | --- |
| `registry/modules_registry.yaml` | canon registry | seul module de la famille inscrit | ancrage canonique documentaire actuel |
| `modules/vision_bot/systemd/vision_bot.service` | systemd | `ExecStart=...vision_bot.py watch` | consumer runtime autonome |
| `modules/vision_bot/scripts/vision_runtime_cmd.sh` | wrapper unifie | host des commandes `cmd-vision` | point d'entree de la paire |
| `modules/vision_bot/scripts/install_shortcuts.sh` | ops install | installe `cmd-vision` et `cmd-vision_bot` | surface operateur canonique |

### Conclusion

- `vision_bot` est bien consomme aujourd'hui
- sa consommation est moins visible dans la supervision fleet que `bot_vision_step2`, mais il reste le point d'entree nominal de la paire canonique et le seul module de la famille deja porte en registry

## 4. Ancrages documentaires canoniques

Les documents suivants convergent vers la meme lecture :

- `docs/status/bot_vision_canonique.md`: paire transitoire `vision_bot` + `bot_vision_step2`
- `docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`: `vision_bot` reception ; `bot_vision_step2` analyse
- `docs/product/guides/BOT_VISION.md`: paire canonique stable, `bot_vision` legacy preserve
- `docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01/01_VISION_CLUSTER_INVENTORY.md`: stack complementaire deja constatee

## Reponse aux questions callers

1. `bot_vision` est appele surtout via sous-surface `headless_capture` et un reste TMUX legacy.
2. `bot_vision_step2` est appele par la supervision runtime, la machine map, ses unites systemd et le wrapper unifie.
3. `vision_bot` est appele par son service, ses wrappers et la registry ; il sert aussi de host au wrapper unifie.
