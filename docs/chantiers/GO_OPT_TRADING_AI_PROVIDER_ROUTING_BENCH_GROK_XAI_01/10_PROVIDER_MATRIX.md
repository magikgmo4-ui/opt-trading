---
go_id: GO_OPT_TRADING_AI_PROVIDER_ROUTING_BENCH_GROK_XAI_01
doc_type: provider_matrix
repo: opt-trading
status: open
created_at: 2026-05-22
surface: doc-only
---

# 10_PROVIDER_MATRIX

---

## 1_OBJECTIF

Positionner Grok/xAI par rapport aux providers actuels sur les axes qui comptent
pour `opt-trading` : coût, qualité reasoning, latence, stabilité API, accès données
X/web/social, et respect du canon de réponse structurée.

---

## 2_PROVIDERS_EN_SCOPE

| ID | Provider | Modèle(s) cible | Statut actuel |
|----|----------|-----------------|---------------|
| P1 | **Claude** (Anthropic) | claude-sonnet-4-6, claude-opus-4-7 | PRIMARY |
| P2 | **ChatGPT** (OpenAI) | gpt-4o, gpt-4o-mini | ACTIVE |
| P3 | **Gemini** (Google) | gemini-1.5-pro, gemini-2.0-flash | ACTIVE |
| P4 | **OpenRouter** | multi-model | FALLBACK |
| P5 | **Grok** (xAI) | grok-3, grok-3-mini | **CANDIDATE** |

OpenClaw = gateway interne — non un provider, hors comparaison directe.

---

## 3_AXES_DE_COMPARAISON

### 3.1 Coût

| Provider | Modèle | Input $/1M tok | Output $/1M tok | Notes |
|----------|--------|---------------|-----------------|-------|
| Claude | sonnet-4-6 | ~3.00 | ~15.00 | avec cache ≈ 0.30 input |
| Claude | opus-4-7 | ~15.00 | ~75.00 | reasoning lourd |
| ChatGPT | gpt-4o | ~2.50 | ~10.00 | — |
| ChatGPT | gpt-4o-mini | ~0.15 | ~0.60 | volume cheap |
| Gemini | 1.5-pro | ~1.25 | ~5.00 | long-context |
| Gemini | 2.0-flash | ~0.10 | ~0.40 | rapide + cheap |
| OpenRouter | variable | variable | variable | markup ~10-20% |
| **Grok** | grok-3 | ~3.00 | ~15.00 | *à vérifier* |
| **Grok** | grok-3-mini | ~0.30 | ~0.50 | *à vérifier* |

*Les prix Grok sont indicatifs — à confirmer lors du benchmark.*

---

### 3.2 Qualité Reasoning

| Provider | Code | Plan GO | Analyse chart | Résumé news | Recherche X/web |
|----------|------|---------|---------------|-------------|-----------------|
| Claude | ★★★★★ | ★★★★★ | ★★★★ | ★★★★ | ★★★ |
| ChatGPT | ★★★★ | ★★★★ | ★★★★★ | ★★★★ | ★★★ |
| Gemini | ★★★★ | ★★★★ | ★★★ | ★★★★★ | ★★★★ |
| OpenRouter | variable | variable | variable | variable | variable |
| **Grok** | *TBD* | *TBD* | *TBD* | *TBD* | *TBD — avantage X* |

---

### 3.3 Latence

| Provider | P50 (ms) | P95 (ms) | Streaming | Notes |
|----------|----------|----------|-----------|-------|
| Claude | ~800 | ~2000 | oui | via OpenClaw |
| ChatGPT | ~600 | ~1800 | oui | — |
| Gemini | ~500 | ~1500 | oui | — |
| Grok | *TBD* | *TBD* | oui | API xAI |

---

### 3.4 Stabilité API

| Provider | Uptime annoncé | Rate limits | Auth | Notes |
|----------|----------------|-------------|------|-------|
| Claude | 99.9% | tier-based | ANTHROPIC_API_KEY | prompt cache |
| ChatGPT | 99.9% | tier-based | OPENAI_API_KEY | — |
| Gemini | 99.5% | tier-based | GOOGLE_API_KEY | — |
| OpenRouter | 99.0% | model-dep | OPENROUTER_API_KEY | multi |
| **Grok** | *TBD* | *TBD* | XAI_API_KEY | nouveau |

---

### 3.5 Accès données X / web / catalyst

| Provider | Données X (Twitter) | Recherche web live | Catalyst temps-réel |
|----------|--------------------|--------------------|---------------------|
| Claude | non (cutoff) | non (sans tool) | non |
| ChatGPT | non (cutoff) | oui (browsing) | partiel |
| Gemini | non (cutoff) | oui (grounding) | partiel |
| **Grok** | **oui (natif xAI)** | **oui (live X)** | **OUI — avantage clé** |

→ Grok est le seul provider avec accès natif aux données X temps-réel.
C'est l'axe différenciateur principal à tester.

---

### 3.6 Respect du Canon opt-trading

Le canon opt-trading impose des réponses structurées (JSON, YAML, markdown table),
la neutralité sur les ordres (pas de BUY/SELL directs), et la compatibilité
avec les schemas `ObservationEvent`.

| Provider | Structuration JSON | Neutralité ordre | Compat schemas |
|----------|--------------------|-----------------|----------------|
| Claude | ★★★★★ | ★★★★★ | ★★★★★ |
| ChatGPT | ★★★★ | ★★★★ | ★★★★ |
| Gemini | ★★★★ | ★★★★ | ★★★ |
| **Grok** | *TBD* | *TBD* | *TBD* |

---

## 4_POSITIONNEMENT_CANDIDAT

```text
Grok/xAI : CANDIDATE
Avantage différenciateur unique : accès données X/Twitter temps-réel.
Cas d'usage prioritaires à tester :
  - résumé catalyst X (sentiment, news ticker)
  - analyse filing / news
  - recherche web live sur actif tradé
Cas d'usage secondaires :
  - refactor code (Claude domine)
  - plan bundle GO (Claude domine)
```

---

## 5_ROUTING_RULES_CANDIDAT

Si Grok est retenu, les règles de routing proposées sont :

| Tâche | Provider cible | Fallback |
|-------|----------------|----------|
| Catalyst X / social sentiment | Grok | ChatGPT |
| Résumé news / filing | Grok ou Gemini | Claude |
| Analyse screenshot trading | ChatGPT / Claude | — |
| Refactor code | Claude | — |
| Plan GO / architecture | Claude | — |
| Long-context doc | Gemini | Claude |

Ces règles sont conditionnelles au verdict `40_DECISION_RULES.md`.
