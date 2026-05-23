---
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_PROD_PROMOTION_DECISION_01
doc_type: initial_project_doc
repo: opt-trading
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
branch: go/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_PROD_PROMOTION_DECISION_01
surface: doc-only — décision opérationnelle
runtime_mutation: false
---

# 00_INITIAL_PROJECT_DOC
## GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_PROD_PROMOTION_DECISION_01

---

## 1_MASTER_TARGET

```text
Décider comment activer Coinglass Vision en production continue sur admin-trading.

Verdict parmi trois options :
  A. Timer systemd dédié bot-vision-coinglass-capture.timer
  B. Intégration au pipeline Bot Vision historique (timer + wrappers existants)
  C. Runner manuel / staging uniquement (pas de promotion prod immédiate)
```

---

## 2_CONTEXTE

La stack Coinglass Vision headless a été validée en staging réel (#730, PASS_STAGING_REAL) :
- 3 runs PASS consécutifs, 5 détections/run, confidence=1.00
- `--validate --required 3` exit 0
- `/desk/vision ok=true`, panel UI présent

La stack existante sur admin-trading :
- `bot-vision-headless-capture.timer` — capture périodique (Node.js + JS)
- `bot_vision_step2` — analyse OpenAI Vision via pipeline historique
- `desk_bridge.timer` — bridge vers `/shared/desk_pro/latest/`
- Wrappers : `cmd-bot_vision`, `menu-bot_vision`, `sanity-bot_vision`

La nouvelle voie Coinglass :
- `scripts/run_vision_capture.py` — entry point Python
- `data/vision/coinglass/` — stockage dédié
- `data/deskpro/inputs/vision_context/coinglass/latest.json` — input Desk Pro
- Gate : `VISION_BOT_ENABLED=true`, `VISION_AI_PROVIDER=openai`, `OPENAI_API_KEY`

---

## 3_OPTIONS

### Option A — Timer systemd dédié

```text
Créer : /etc/systemd/system/bot-vision-coinglass-capture.timer
        /etc/systemd/system/bot-vision-coinglass-capture.service

Avantages :
  - indépendant du pipeline historique
  - fréquence configurable séparément
  - logs dédiés

Inconvénients :
  - nécessite droits root pour systemd
  - un timer de plus à maintenir
  - OPENAI_API_KEY à injecter dans le service (EnvironmentFile)

Prérequis :
  - OPENAI_API_KEY stable dans /opt/trading/.env ou EnvironmentFile dédié
  - Playwright + openai installés dans venv système
```

### Option B — Intégration pipeline historique

```text
Brancher run_vision_capture.py dans le timer bot-vision-headless-capture.timer existant
OU créer un post-hook appelé depuis bot_vision_step2.

Avantages :
  - réutilise l'infra existante
  - monitoring/wrappers existants (sanity-bot_vision)

Inconvénients :
  - couplage avec pipeline Node.js historique
  - risque d'interférence sur vision_inbox/vision_processed
  - deux stacks hétérogènes (JS + Python) dans le même timer
```

### Option C — Runner manuel / staging uniquement

```text
Ne pas activer de timer. Lancer run_vision_capture.py manuellement
ou via cron ponctuel selon besoin opérationnel.

Avantages :
  - zéro risque infra
  - contrôle explicite des runs

Inconvénients :
  - pas de donnée fraîche en continu pour Desk Pro
  - Desk Pro affiche des données périmées entre les runs manuels
```

---

## 4_CONSTRAINTS

```text
- doc-only : aucun runtime muté dans ce GO
- OPENAI_API_KEY ne doit pas être dans le code
- timer systemd nécessite root (à valider avec l'opérateur)
- ne pas casser le pipeline Bot Vision historique (bot-vision-headless-capture.timer)
- verdict = A / B / C
```

---

## 5_DELIVERABLES

| Fichier | Contenu |
|---|---|
| `10_DECISION_MATRIX.md` | Comparaison détaillée A/B/C |
| `20_ACCEPTANCE_REPORT.md` | Verdict + justification + prochaine étape |
| `docs/index/inbox/...md` | Entrée inbox |

---

## 6_CLOSEOUT_CRITERIA

Ce GO est clos si :
- Un verdict A/B/C est inscrit dans `20_ACCEPTANCE_REPORT.md`
- La prochaine étape opérationnelle est documentée
- Aucun runtime muté

---

## 7_INVARIANTS

```text
- OPENAI_API_KEY ne va jamais dans le code ni dans git
- Pipeline Bot Vision historique non cassé
- Desk Pro = surface read-only, pas source de vérité
- Verdict final est actionnable immédiatement
```
