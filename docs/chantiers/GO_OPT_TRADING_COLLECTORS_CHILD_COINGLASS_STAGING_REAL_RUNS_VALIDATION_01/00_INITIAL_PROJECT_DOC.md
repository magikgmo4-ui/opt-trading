---
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_REAL_RUNS_VALIDATION_01
doc_type: initial_project_doc
repo: opt-trading
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
branch: go/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_REAL_RUNS_VALIDATION_01
surface: operational — staging validation réelle
runtime_mutation: false
---

# 00_INITIAL_PROJECT_DOC
## GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_REAL_RUNS_VALIDATION_01

---

## 1_MASTER_TARGET

```text
Valider la stack Coinglass vision headless en conditions staging réelles :
  - 3 captures Playwright successives sur coinglass.com
  - OpenAI Vision produit ≥ 1 detection qualifiée par run
  - Chaque run écrit raw/ + normalized/ + latest.json + events.jsonl
  - --validate exit 0 après les 3 runs
  - Desk Pro /desk/vision retourne ok=true
  - /desk/ui panel "Coinglass Vision" affiche les detections
```

Le parent `GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01`
est ACCEPTED (#719). Ce GO est un child opérationnel — il ne rouvre pas le parent.

---

## 2_CONTEXTE

La stack complète a été construite en 6 child GOs mergés sur sot/mainline :

| Surface | PR | État |
|---|---|---|
| Acceptance parent A1→B2 | #719 | merged |
| A staging activation (Playwright + validator + CLI) | #721 | merged |
| AI extraction réelle (make_ai_extraction_fn) | #722 | merged |
| B Telegram sender | #723 | merged |
| C Desk Pro UI panel (GET /desk/vision) | #725 | merged |

Le stub d'extraction a été remplacé par `make_ai_extraction_fn()` avec provider
`openai`. La gate staging requiert 3 runs PASS consécutifs dans `events.jsonl`
pour déclarer la surface prête à la promotion.

---

## 3_SCOPE

**IN SCOPE :**
- Runbook opératoire staging (prérequis, commandes exactes, séquence)
- Template de preuve des 3 runs (timestamps, detections, fichiers produits)
- Validation `--validate --required 3` exit 0
- Vérification Desk Pro `/desk/vision` et `/desk/ui`
- Rapport d'acceptance documentant les 3 runs réels

**OUT OF SCOPE :**
- Activation prod automatique
- Nouveau adapter API Coinglass
- Modification du contrat `vision_context.coinglass.v1`
- Modification des index globaux
- Modification de `modules/` ou `scripts/`

---

## 4_CONSTRAINTS

```text
- aucun fichier runtime modifié
- VISION_BOT_ENABLED=true requis (gate explicite dans headless_capture.py)
- VISION_AI_PROVIDER=openai requis pour détections qualifiées
- OPENAI_API_KEY requis pour appels réels
- pas d'activation prod avant rapport complet
```

---

## 5_DELIVERABLES

| Fichier | Contenu |
|---|---|
| `10_RUNBOOK_STAGING.md` | Prérequis + commandes séquencées |
| `20_RUN_EVIDENCE.md` | Preuve des 3 runs (à remplir lors des runs) |
| `30_ACCEPTANCE_REPORT.md` | Verdict final (à remplir après --validate PASS) |
| `90_REPRISE_POINT.md` | Point de reprise si session interrompue |
| `docs/index/inbox/...md` | Entrée inbox |

---

## 6_CLOSEOUT_CRITERIA

Ce GO est clos (PASS) si :
- `20_RUN_EVIDENCE.md` contient 3 runs avec timestamps, detections, confidence
- `--validate --required 3` a retourné exit 0
- `/desk/vision` a retourné `ok=true` après les runs
- `30_ACCEPTANCE_REPORT.md` est rempli avec verdict PASS_STAGING_REAL
- aucun runtime muté

---

## 7_INVARIANTS

```text
- Telegram = confirmation read-only uniquement, pas source de vérité
- latest.json = source canonique pour Desk Pro consumer
- events.jsonl = source canonique pour --validate
- 3 runs PASS consécutifs requis — pas d'exception
```
