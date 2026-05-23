---
go_id: GO_OPT_TRADING_AI_PROVIDER_ROUTING_BENCH_GROK_XAI_01
doc_type: initial_project_doc
repo: opt-trading
status: open
created_at: 2026-05-22
branch: go/GO_OPT_TRADING_AI_PROVIDER_ROUTING_BENCH_GROK_XAI_01
surface: doc-only
scope: ai provider benchmark — grok/xai
runtime_mutation: false
---

# 00_INITIAL_PROJECT_DOC
## GO_OPT_TRADING_AI_PROVIDER_ROUTING_BENCH_GROK_XAI_01

---

## 1_MASTER_TARGET

```text
Évaluer Grok/xAI dans l'architecture opt-trading comme provider secondaire,
fallback API, ou moteur spécialisé X/web/social/catalyst.

Produire un verdict actionnable : KEEP / FALLBACK_ONLY / API_ONLY / DROP.
```

Grok ne remplace pas le provider principal sans benchmark prouvé.
Ce chantier est doc-only — aucun runtime muté.

---

## 2_INITIAL_NEED

L'architecture opt-trading s'appuie sur plusieurs providers IA :

| Provider | Usage actuel | Rôle |
|----------|-------------|------|
| Claude (Anthropic) | Primary dev + analysis | Reasoning, code, plan |
| ChatGPT (OpenAI) | Secondary | Vision, résumé, code |
| Gemini (Google) | Contextuel | Long-context, doc |
| OpenRouter | Fallback agrégateur | Multi-model routing |
| OpenClaw | Gateway interne | Orchestrateur local |
| Grok (xAI) | **CANDIDATE — non évalué** | X/web/social catalyst |

Grok présente un avantage potentiel sur les données X (Twitter) et les catalysts
temps-réel. Ce chantier évalue si cet avantage justifie une intégration.

---

## 3_SCOPE

**IN SCOPE :**
- Matrice comparative providers (coût, qualité, latence, stabilité)
- 5 tâches de benchmark fixes et reproductibles
- Template de résultats structuré
- Règles de décision vers verdict final

**OUT OF SCOPE :**
- Modification de `modules/` ou `scripts/`
- Intégration API Grok dans le runtime
- Modification des index globaux (`GO_INDEX.md`, `ACTIVE_STREAMS.md`)
- Remplacement du provider principal

---

## 4_CONSTRAINTS

```text
- doc-only : aucun fichier runtime modifié
- aucun index global modifié
- provider principal non remplacé sans preuve benchmark
- mesurer : coût, qualité, latence, stabilité, respect du canon opt-trading
- verdict final parmi : KEEP / FALLBACK_ONLY / API_ONLY / DROP
```

---

## 5_DELIVERABLES

| Fichier | Contenu |
|---------|---------|
| `10_PROVIDER_MATRIX.md` | Matrice comparative providers |
| `20_TEST_PROMPTS.md` | 5 tâches fixes de benchmark |
| `30_RESULTS_TEMPLATE.md` | Template de saisie des résultats |
| `40_DECISION_RULES.md` | Règles de décision + verdict |
| `docs/index/inbox/GO_OPT_TRADING_AI_PROVIDER_ROUTING_BENCH_GROK_XAI_01.md` | Entrée inbox |

---

## 6_CLOSEOUT_CRITERIA

Ce chantier est clos si :
- Les 5 tâches sont exécutées sur Grok et au moins 2 providers de référence
- Le template `30_RESULTS_TEMPLATE.md` est rempli
- Un verdict est inscrit dans `40_DECISION_RULES.md`
- Aucun runtime n'a été muté

---

## 7_INVARIANTS

```text
- Grok ne devient pas provider principal sans score benchmark ≥ référence
- Aucune clé API Grok ne va dans le code — secrets uniquement dans .env
- Ce doc ne déclenche ni ordre, ni Telegram, ni Sheets write
```
