---
go_id: GO_OPT_TRADING_AI_PROVIDER_ROUTING_BENCH_GROK_XAI_01
doc_type: test_prompts
repo: opt-trading
status: open
created_at: 2026-05-22
surface: doc-only
---

# 20_TEST_PROMPTS

---

## 1_OBJECTIF

5 tâches fixes et reproductibles, exécutables sur n'importe quel provider.
Chaque tâche produit un score 1–5 sur : qualité, structuration, latence perçue.

Les prompts sont stables — ne pas les modifier entre providers.

---

## 2_PROTOCOLE

1. Exécuter le prompt tel quel sur chaque provider testé.
2. Saisir le résultat brut dans `30_RESULTS_TEMPLATE.md`.
3. Scorer immédiatement (pas de révision a posteriori).
4. Ne pas relancer si la réponse est mauvaise — noter le score et passer.

---

## 3_TÂCHE_1 — Analyse Screenshot Trading

**Catégorie :** vision / analyse chart

**Prompt :**

```
Tu es un analyste technique senior. Voici un screenshot d'un graphique XAUUSD 15min.

Identifie :
1. La structure de marché dominante (HH/HL/LH/LL ou range)
2. Les niveaux clés visibles (support, résistance, OB, FVG si présents)
3. Le biais directionnel actuel (bullish / bearish / neutre)
4. Un setup potentiel si visible (entrée, SL, TP approximatifs)

Réponds en JSON avec les clés : structure, key_levels, bias, setup.
Si aucun setup clair : setup = null.
```

**Image à fournir :** capture d'écran XAUUSD 15min (à prendre au moment du test).

**Évaluation :**
- Qualité : pertinence de la lecture de marché
- Structuration : JSON valide, clés respectées
- Latence : temps de réponse perçu (rapide / moyen / lent)

---

## 4_TÂCHE_2 — Résumé Filing / News

**Catégorie :** résumé texte / catalyst

**Prompt :**

```
Résume ce filing/communiqué en 5 bullet points maximum, orienté trading.

Pour chaque point, indique :
- le fait clé
- l'impact probable sur le cours (positif / négatif / neutre)
- le délai d'impact estimé (immédiat / court terme / long terme)

Format : liste markdown. Ne pas ajouter de commentaire général.

TEXTE :
[insérer le texte d'un communiqué ou d'une news récente au moment du test]
```

**Texte à insérer :** extrait d'un communiqué SEC / earnings / macro release du jour.

**Évaluation :**
- Qualité : précision des impacts identifiés
- Structuration : bullet points markdown, format impact/délai respecté
- Latence : temps de réponse perçu

---

## 5_TÂCHE_3 — Refactor Code

**Catégorie :** code / engineering

**Prompt :**

```python
# Refactore cette fonction Python pour la rendre plus lisible et robuste.
# Garde la même signature et le même comportement observable.
# Ne pas ajouter de logging. Ne pas changer les types de retour.

def calc_position_size(capital, risk_pct, entry, sl):
    r = abs(entry - sl)
    if r == 0:
        return 0
    risk_amount = capital * (risk_pct / 100)
    size = risk_amount / r
    return round(size, 4)
```

Fournis uniquement le code refactoré, sans explication.

**Évaluation :**
- Qualité : lisibilité, robustesse (edge cases), idiomaticité Python
- Structuration : code seul, pas de blabla
- Latence : temps de réponse perçu

---

## 6_TÂCHE_4 — Plan Bundle GO

**Catégorie :** architecture / planning

**Prompt :**

```
Tu travailles sur opt-trading, un système de trading algorithmique Python/FastAPI.

Je veux créer un chantier doc-only pour auditer les endpoints REST non-documentés
du service webhook_server.py (port 8000).

Génère un plan de chantier structuré avec :
- 3 à 5 fichiers à créer (noms + rôle en une ligne)
- contraintes à respecter (no runtime, no index global)
- critères de fermeture (definition of done)

Format : markdown, sections H2, listes à puces.
```

**Évaluation :**
- Qualité : pertinence du plan, respect des contraintes opt-trading
- Structuration : markdown propre, sections claires
- Latence : temps de réponse perçu

---

## 7_TÂCHE_5 — Recherche Catalyst X / Web

**Catégorie :** recherche web / social / catalyst — **axe différenciateur Grok**

**Prompt :**

```
Recherche les 3 catalysts les plus récents sur XAUUSD (Gold) publiés
dans les dernières 24 heures sur X (Twitter) et les sources financières web.

Pour chaque catalyst :
1. Source (X / Reuters / Bloomberg / autre)
2. Résumé en 1 phrase
3. Sentiment de marché associé (bullish / bearish / neutre)
4. Fiabilité estimée (haute / moyenne / faible)

Format : tableau markdown avec colonnes Source, Résumé, Sentiment, Fiabilité.
```

**Note :** cette tâche est conçue pour mettre en valeur l'avantage natif de Grok
(accès X temps-réel). Les providers sans accès web live répondront sur données statiques.

**Évaluation :**
- Qualité : fraîcheur des données, pertinence des catalysts
- Structuration : tableau markdown valide
- Latence : temps de réponse perçu

---

## 8_GRILLE_DE_SCORING

Pour chaque tâche × provider :

| Critère | 1 | 2 | 3 | 4 | 5 |
|---------|---|---|---|---|---|
| Qualité | Hors sujet | Partiel / erreurs | Correct | Bon | Excellent |
| Structuration | Format ignoré | Partiel | Conforme | Propre | Parfait |
| Latence | >10s | 5–10s | 3–5s | 1–3s | <1s |

Score final par provider = moyenne des 3 critères × 5 tâches (max 75 points).
