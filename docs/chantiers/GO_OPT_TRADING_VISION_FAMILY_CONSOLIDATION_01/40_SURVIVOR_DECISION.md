---
doc_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01_SURVIVOR_DECISION
doc_type: family_decision
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - modules
  - vision
  - survivor
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01/30_RUNTIME_SURFACE_MAP.md
---

# 40_SURVIVOR_DECISION

## Reponses tranchees

### 1. Quel module est reellement consomme aujourd'hui ?

- `bot_vision_step2`: oui, fortement, via supervision runtime et systemd
- `vision_bot`: oui, comme consumer inbox/outbox et host du wrapper unifie
- `bot_vision`: non comme survivant global ; oui partiellement via `headless_capture`

### 2. L'ensemble est-il une lignee versionnee ou une stack complementaire ?

Verdict: **stack complementaire avec reliquat de lignee historique**.

Ce n'est pas un simple `step1 -> step2 -> final`.

- `bot_vision` porte le reliquat de lignee
- `vision_bot` et `bot_vision_step2` forment la paire operatoire courante
- `headless_capture` ajoute un role producteur distinct

### 3. Quel module devient survivant ?

Verdict retenu pour ce GO doc-only:

- **survivant documentaire / owner canonique de famille: `vision_bot`**
- **composant operatoire complementaire requis: `bot_vision_step2`**
- **legacy preserve: `bot_vision`**

## Pourquoi `vision_bot` comme owner canonique

- deja present dans `registry/modules_registry.yaml`
- deja documente comme point d'entree capture / inbox-outbox
- heberge le wrapper unifie `cmd-vision`
- sert d'ancre nominale la moins ambigue pour la paire transitoire

## Pourquoi `bot_vision_step2` n'est pas rabattu en legacy

- service requis dans `machine_runtime_map.yml`
- surface surveillee par `runtime_health`
- porte des fonctions que `vision_bot` ne couvre pas: OpenAI Vision, Telegram, artefacts Desk Pro

## Pourquoi `bot_vision` ne peut pas rester ambigu

- le root est legacy par README et par trajectoire
- mais `headless_capture` y reste utile en production headless
- tant que `headless_capture` n'est pas extrait ou re-rattache, `bot_vision` ne peut etre ni supprime ni archive completement

## Classement final de famille

| Surface | Classement |
| --- | --- |
| `modules/vision_bot` | survivant documentaire + runtime utile |
| `modules/bot_vision_step2` | survivant operatoire complementaire |
| `modules/bot_vision` | legacy preserve |
| `modules/bot_vision/headless_capture` | runtime utile mal heberge sous legacy |
| `modules/bot_vision/bot_vision_step1` | legacy pur |

## Verdict

**PASS**

La famille est clarifiee sans mutation runtime.
Le survivant unique n'est pas encore materialisable physiquement, mais l'owner canonique et les roles distincts sont maintenant explicites.
