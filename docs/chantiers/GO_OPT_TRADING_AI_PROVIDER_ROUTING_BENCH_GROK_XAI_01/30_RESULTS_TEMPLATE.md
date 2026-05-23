---
go_id: GO_OPT_TRADING_AI_PROVIDER_ROUTING_BENCH_GROK_XAI_01
doc_type: results_template
repo: opt-trading
status: open
created_at: 2026-05-22
surface: doc-only
---

# 30_RESULTS_TEMPLATE

---

## 1_METADATA_SESSION

```yaml
date_test: ~
tester: ~
providers_testés: [Grok, Claude, ChatGPT]
modèles:
  Grok: grok-3 / grok-3-mini
  Claude: claude-sonnet-4-6
  ChatGPT: gpt-4o
notes_contexte: ~
```

---

## 2_GRILLE_RÉSULTATS

### Tâche 1 — Analyse Screenshot Trading

| Provider | Qualité (1–5) | Structuration (1–5) | Latence (1–5) | Total | Observations |
|----------|--------------|---------------------|---------------|-------|--------------|
| Claude | | | | | |
| ChatGPT | | | | | |
| Gemini | | | | | |
| Grok | | | | | |

**Réponse brute Grok :**
```
[à remplir]
```

**Réponse brute référence (meilleur score) :**
```
[à remplir]
```

---

### Tâche 2 — Résumé Filing / News

| Provider | Qualité (1–5) | Structuration (1–5) | Latence (1–5) | Total | Observations |
|----------|--------------|---------------------|---------------|-------|--------------|
| Claude | | | | | |
| ChatGPT | | | | | |
| Gemini | | | | | |
| Grok | | | | | |

**Texte source utilisé :**
```
[à remplir — communiqué ou news du jour]
```

**Réponse brute Grok :**
```
[à remplir]
```

---

### Tâche 3 — Refactor Code

| Provider | Qualité (1–5) | Structuration (1–5) | Latence (1–5) | Total | Observations |
|----------|--------------|---------------------|---------------|-------|--------------|
| Claude | | | | | |
| ChatGPT | | | | | |
| Gemini | | | | | |
| Grok | | | | | |

**Réponse brute Grok :**
```python
# [à remplir]
```

---

### Tâche 4 — Plan Bundle GO

| Provider | Qualité (1–5) | Structuration (1–5) | Latence (1–5) | Total | Observations |
|----------|--------------|---------------------|---------------|-------|--------------|
| Claude | | | | | |
| ChatGPT | | | | | |
| Gemini | | | | | |
| Grok | | | | | |

**Réponse brute Grok :**
```
[à remplir]
```

---

### Tâche 5 — Recherche Catalyst X / Web

| Provider | Qualité (1–5) | Structuration (1–5) | Latence (1–5) | Total | Observations |
|----------|--------------|---------------------|---------------|-------|--------------|
| Claude | | | | | |
| ChatGPT | | | | | |
| Gemini | | | | | |
| Grok | | | | | |

**Réponse brute Grok :**
```
[à remplir]
```

**Note :** C'est la tâche où Grok a l'avantage natif (accès X temps-réel).
Comparer explicitement la fraîcheur des données.

---

## 3_SYNTHÈSE_SCORES

| Provider | T1 | T2 | T3 | T4 | T5 | TOTAL /75 | Rang |
|----------|----|----|----|----|----|-----------|----|
| Claude | | | | | | | |
| ChatGPT | | | | | | | |
| Gemini | | | | | | | |
| Grok | | | | | | | |

---

## 4_OBSERVATIONS_QUALITATIVES

### Grok — points forts observés
```
[à remplir]
```

### Grok — points faibles observés
```
[à remplir]
```

### Comportement sur données X / catalyst
```
[à remplir — différence clé vs autres providers]
```

### Respect du canon opt-trading (JSON, neutralité, schemas)
```
[à remplir]
```

---

## 5_COÛT_ESTIMÉ_SESSION

| Provider | Tokens input | Tokens output | Coût estimé ($) |
|----------|-------------|---------------|-----------------|
| Claude | | | |
| ChatGPT | | | |
| Gemini | | | |
| Grok | | | |

---

## 6_VERDICT_PROVISOIRE

```text
À compléter après scores :

Grok verdict provisoire : [ KEEP / FALLBACK_ONLY / API_ONLY / DROP ]
Raison principale :
Cas d'usage retenu si KEEP ou FALLBACK_ONLY :
```

→ Verdict final dans `40_DECISION_RULES.md`.
