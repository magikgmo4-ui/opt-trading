---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01_OPENCLAW_WORKER_ORCHESTRATION_RULES
doc_type: external_rules
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01
status: draft_for_review
lifecycle_stage: child_external_rules
parent_go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - openclaw
  - worker
  - orchestration
  - canonical
  - external-apps
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/03_OPENCLAW_WORKER_ORCHESTRATION_RULES.md
point_de_reprise: "Règles pour OpenClaw, workers et orchestration : aucune couche externe ne devient source canonique."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/01_UPDATE_MATRIX_RULES.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/02_STATUS_PROMOTION_RULES.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
---

# 03_OPENCLAW_WORKER_ORCHESTRATION_RULES

## 1_OBJECTIF

Définir le statut exact d'OpenClaw, des workers, des apps externes et des couches d'orchestration dans la chaîne canonique `opt-trading`. Ces couches sont des **projections d'usage**, pas des sources de vérité.

## 2_PRINCIPE_FONDAMENTAL

```text
REPO = SOURCE CANONIQUE UNIQUE

Toute autre couche (OpenClaw, worker, app externe, orchestrateur, UI)
est une PROJECTION de la source canonique, pas une source indépendante.

Une projection peut :
  - exposer un usage
  - faciliter un accès
  - automatiser une action

Une projection ne peut PAS :
  - définir l'état d'un produit
  - servir de preuve de promotion
  - remplacer un closeout documentaire
  - devenir la référence primaire d'une fonction ou d'une formule
```

## 3_OPENCLAW

### 3.1 Définition canonique

```text
OpenClaw = agent runtime / couche d'orchestration.

Dans opt-trading, OpenClaw :
  - lit les documents canoniques (chantiers, guides, matrices)
  - exécute des commandes validées par le repo
  - projette l'état courant pour l'opérateur
  - suggère des actions basées sur les règles du repo
```

### 3.2 Ce qu'OpenClaw EST

```text
- Un lecteur privilégié des couches produit.
- Un exécuteur de procédures documentées.
- Une interface opérateur repo-first.
- Un agent qui applique des règles (pas qui les crée).
```

### 3.3 Ce qu'OpenClaw N'EST PAS

```text
- OpenClaw n'est pas une source canonique.
- OpenClaw ne valide pas un produit (le closeout le fait).
- OpenClaw ne promeut pas un produit (les preuves le font).
- OpenClaw ne remplace pas un guide (le guide est la source).
- OpenClaw ne définit pas les formules (les chantiers le font).
- OpenClaw ne décide pas des changements de bucket (les règles + preuves le font).
```

### 3.4 Règles d'interaction

```text
R1. Quand OpenClaw applique le UPDATE_PROTOCOL après une PR :
    - OpenClaw suit la checklist (04_PR_CHECKLIST.md).
    - OpenClaw propose, l'opérateur valide.
    - Le commit de mise à jour est fait par l'opérateur, pas par OpenClaw.

R2. Quand OpenClaw lit l'état d'un produit :
    - La source est PRODUCT_USAGE_MATRIX.md + PRODUCT_USAGE_ATLAS.md.
    - OpenClaw ne dérive pas l'état depuis autre chose.

R3. Quand OpenClaw suggère un NEXT_GO :
    - OpenClaw lit la matrice NEXT_GO_BY_PRODUCT.
    - OpenClaw ne crée pas de GO de sa propre initiative.

R4. OpenClaw ne modifie jamais un fichier canonique sans décision opérateur explicite.
```

## 4_WORKERS

### 4.1 Définition canonique

```text
Worker = composant d'exécution (script, daemon, service).

Un worker :
  - implémente une spécification documentée dans un chantier
  - s'exécute dans un environnement défini
  - produit des logs / sorties vérifiables
```

### 4.2 Ce qu'un worker EST

```text
- Une implémentation d'une spec validée.
- Un producteur de preuves (logs, résultats, métriques).
- Un composant testable et reproductible.
```

### 4.3 Ce qu'un worker N'EST PAS

```text
- Un worker n'est pas un produit fini sans closeout.
- Un worker qui tourne n'est pas une preuve de succès (les logs doivent être vérifiés).
- Un worker en simulation ne prouve pas l'usage réel.
- Un worker sans spec documentée = code orphelin.
```

### 4.4 Règles d'interaction

```text
R5. Un worker ne peut être promu USABLE_NOW qu'avec :
    - closeout complet du chantier parent
    - preuves d'exécution documentées (logs, captures, tests)
    - guide d'usage écrit
    - décision opérateur explicite

R6. Un worker en simulation reste SIMULATED_ONLY.
    Même s'il tourne 24/7, sans usage réel, il ne monte pas.

R7. Les logs d'un worker sont des preuves uniquement si :
    - le scénario de test est documenté
    - les résultats attendus sont définis en amont
    - un humain a vérifié la cohérence
```

## 5_APPS_EXTERNES

### 5.1 Définition

```text
App externe = tout service hors repo opt-trading :
  - ClickUp (project management)
  - Telegram (messaging)
  - Airtable (database)
  - TradingView (charting / alerting)
  - Bitget (exchange)
  - GitHub (repo hosting)
```

### 5.2 Règles

```text
R8. Une app externe est une interface d'usage, pas une source canonique.

R9. Un produit qui dépend d'une app externe doit être marqué
    USABLE_LIMITED_NEEDS_EXTERNAL.

R10. Les credentials / clés API / tokens pour les apps externes sont des gaps.
    Ils sont listés dans remaining_gaps du produit.
    Ils ne bloquent pas la documentation mais bloquent la promotion.

R11. Une capture d'écran d'une app externe (ClickUp, Telegram)
    n'est pas une preuve suffisante de succès.
    Elle doit être accompagnée d'un closeout documentaire dans le repo.
```

## 6_ORCHESTRATION

### 6.1 Définition

```text
Orchestration = couche qui coordonne plusieurs workers / apps / produits.
Exemples : Desk Pro (orchestrateur), OpenClaw (agent), workflow_ai (scripts).
```

### 6.2 Règle clé

```text
R12. L'orchestration ne remplace pas la preuve individuelle de chaque produit.
    Un orchestrateur qui "lance tout et n'affiche pas d'erreur"
    ne prouve pas que chaque produit fonctionne.
    Chaque produit doit avoir ses propres preuves.
```

## 7_GRAPHE_DE_CONFIANCE

Qui fait autorité sur quoi :

```text
Niveau 1 (source canonique) :
  - Chantiers GO_OPT_TRADING_* (dans docs/chantiers/)
  - Closeouts (90_CLOSEOUT.md)
  - Preuves repo (logs, tests, captures)

Niveau 2 (lecture structurée) :
  - PRODUCT_USAGE_MATRIX.md
  - PRODUCT_USAGE_ATLAS.md
  - FINAL_TARGET_GAPS.md
  - PRODUCT_USAGE_GRAPH.mmd

Niveau 3 (usage documenté) :
  - Guides (docs/product/guides/*)
  - UPDATE_PROTOCOL.md
  - PR Checklist

Niveau 4 (projection / exécution) :
  - OpenClaw (agent)
  - Workers (exécutants)
  - Apps externes (interfaces)

Niveau 5 (non canonique) :
  - Messages chat (Discord, Telegram)
  - Commentaires oraux
  - Captures sans closeout
  - Logs non vérifiés
```

```text
Un niveau supérieur (1 > 5) fait autorité sur un niveau inférieur.
Aucune information du niveau 4 ou 5 ne peut contredire le niveau 1 sans closeout.
```

## 8_VIOLATIONS_TYPIQUES

```text
V1. "OpenClaw a dit que ça marchait" → VIOLATION. OpenClaw n'est pas source.
V2. "Le worker tourne sans erreur depuis 3 jours" → VIOLATION sans closeout.
V3. "J'ai testé sur Telegram, ça a marché une fois" → VIOLATION sans closeout + logs.
V4. "Le graph montre que tout est vert" → VIOLATION. Le graph est niveau 2, pas preuve.
V5. "C'est dans l'Atlas donc c'est bon" → VIOLATION. L'Atlas reflète l'état, ne le crée pas.
```

## 17_RESUME_POINT

```text
Repo = source canonique unique (niveau 1).
OpenClaw = agent lecteur/exécuteur, pas source (niveau 4).
Workers = composants d'exécution, pas produits finis sans closeout (niveau 4).
Apps externes = interfaces, pas preuves (niveau 4).
Orchestration = coordination, pas validation (niveau 4).
Graphe de confiance à 5 niveaux établi.
```

## RISKS

- À qualifier.
