---
go_id: GO_OPT_TRADING_AI_PROVIDER_ROUTING_BENCH_GROK_XAI_01
doc_type: decision_rules
repo: opt-trading
status: open
created_at: 2026-05-22
surface: doc-only
---

# 40_DECISION_RULES

---

## 1_RÈGLES_DE_VERDICT

### KEEP — Intégration complète recommandée

Conditions requises (toutes) :
- Score Grok ≥ 55/75 sur le benchmark complet
- Score Tâche 5 (catalyst X) ≥ 4/5 qualité
- Coût session Grok ≤ 1.5× coût Claude équivalent
- Structuration JSON conforme sur ≥ 4/5 tâches
- Latence P50 perçue ≤ Claude

→ Action : ouvrir un child GO d'intégration API (`XAI_API_KEY` dans `.env`, routing rules dans un module dédié).

---

### FALLBACK_ONLY — Fallback catalyst X uniquement

Conditions :
- Score global Grok 40–54/75
- **OU** score Tâche 5 (catalyst X) ≥ 4/5 mais score global < 55
- Structuration conforme ≥ 3/5 tâches

→ Action : documenter Grok comme fallback pour la tâche 5 uniquement.
Intégration minimale : variable `.env` + routing conditionnel dans un script dédié.
Pas de remplacement du provider principal.

---

### API_ONLY — Usage programmatique ponctuel uniquement

Conditions :
- Score global Grok 25–39/75
- **OU** structuration non conforme sur ≥ 3/5 tâches
- **ET** accès X live prouvé et utile (T5 ≥ 3)

→ Action : documenter l'endpoint API Grok pour usage manuel ponctuel.
Aucune intégration automatique dans le runtime.

---

### DROP — Ne pas intégrer

Conditions (une suffit) :
- Score global Grok < 25/75
- Structuration non conforme sur 5/5 tâches
- Instabilité API constatée pendant le test
- Coût Grok > 2× coût Claude pour qualité inférieure

→ Action : fermer ce chantier PASS_DROP. Aucune intégration. Ré-évaluer si Grok sort une nouvelle version majeure.

---

## 2_RÈGLES_ANTI_REMPLACEMENT

```text
INVARIANT : Grok ne devient jamais provider principal sans :
  1. Score ≥ 65/75 sur les 5 tâches
  2. Test de stabilité sur 30 jours consécutifs
  3. Validation explicite d'un GO dédié à la migration
```

Ces conditions ne sont pas atteignables dans ce chantier — elles nécessitent un GO séparé.

---

## 3_RÈGLES_DE_ROUTING_CONDITIONNELLES

Ces règles s'appliquent uniquement si verdict = KEEP ou FALLBACK_ONLY.

| Tâche | Trigger | Provider cible | Fallback |
|-------|---------|----------------|----------|
| Catalyst X / sentiment social | `task_type == "catalyst_x"` | Grok | ChatGPT |
| News filing résumé | `task_type == "news_summary"` | Grok ou Gemini | Claude |
| Analyse chart / vision | `task_type == "chart_analysis"` | ChatGPT | Claude |
| Refactor code | `task_type == "code"` | Claude | — |
| Plan GO / architecture | `task_type == "planning"` | Claude | — |

Ces règles sont doc-only — elles ne modifient aucun module runtime.

---

## 4_VERDICT_FINAL

```text
Date décision : ~
Exécuteur : ~

VERDICT : [ KEEP / FALLBACK_ONLY / API_ONLY / DROP ]

Score global Grok : __ /75
Score T5 (catalyst X) : __ /5

Justification :


Prochaine étape :
```

---

## 5_CLOSEOUT_CONDITIONS

Ce chantier est clos (PASS) si :
- `30_RESULTS_TEMPLATE.md` est entièrement rempli (5 tâches × ≥ 2 providers)
- Le verdict final est inscrit dans la section `4_VERDICT_FINAL` ci-dessus
- Aucun runtime n'a été muté
- Aucun index global n'a été modifié

Verdict de closeout attendu :
```text
PASS_AI_PROVIDER_BENCH_GROK_XAI_[KEEP|FALLBACK_ONLY|API_ONLY|DROP]
```
