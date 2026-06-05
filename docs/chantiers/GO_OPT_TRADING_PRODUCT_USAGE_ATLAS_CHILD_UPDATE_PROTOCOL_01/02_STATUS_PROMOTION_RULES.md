---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01_STATUS_PROMOTION_RULES
doc_type: promotion_rules
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01
status: draft_for_review
lifecycle_stage: child_promotion_rules
parent_go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - status
  - promotion
  - subtypes
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/02_STATUS_PROMOTION_RULES.md
point_de_reprise: "Règles de promotion et rétrogradation pour tous les sous-types de statut."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/01_UPDATE_MATRIX_RULES.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01/01_PRODUCT_STATUS_TAXONOMY.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/01_USAGE_VIEW.md
---

# 02_STATUS_PROMOTION_RULES

## 1_OBJECTIF

Définir tous les statuts et sous-types d'un produit dans l'Atlas, leurs conditions de promotion vers le niveau supérieur, et les anti-règles qui empêchent toute promotion implicite.

## 2_BUCKETS_PRINCIPAUX

```text
USABLE_NOW
USABLE_LIMITED
DOC_ONLY
SIMULATED_ONLY
FORBIDDEN_LIVE
```

Précédence prudente :

```text
FORBIDDEN_LIVE > SIMULATED_ONLY > DOC_ONLY > USABLE_LIMITED > USABLE_NOW
```

## 3_SOUS_TYPES_DETAILLES

### 3.1 DOC_ONLY — 4 sous-types

| Sous-type | Définition | Exemple |
|---|---|---|
| `DOC_ONLY_REFERENCE` | Documentation de référence pure, pas de chemin d'implémentation connu | OpenClaw Docs Library |
| `DOC_ONLY_INITIAL_PROJECT` | Projet initial documenté, plan posé, pas encore de code vérifié | BTC COIN-M (parent initial avant SOURCE_LOCK) |
| `DOC_ONLY_IMPLEMENTATION_READY` | Documentation complète, schémas posés, implémentation autorisée mais pas commencée | BACKTEST_DATA_PREP_01 (schémas prêts, code pas écrit) |
| `DOC_ONLY_BLOCKED_BY_DEPENDENCY` | Documentation complète, mais bloqué par un autre produit non finalisé | Airtable Orchestration (bridge non prouvé) |

**Règles de promotion pour DOC_ONLY :**

```text
DOC_ONLY_REFERENCE → pas de promotion possible (reste référence)
DOC_ONLY_INITIAL_PROJECT → DOC_ONLY_IMPLEMENTATION_READY après child source lock / spec validée
DOC_ONLY_IMPLEMENTATION_READY → SIMULATED_ONLY_IMPLEMENTATION_READY après premier test simulé PASS
DOC_ONLY_BLOCKED_BY_DEPENDENCY → DOC_ONLY_IMPLEMENTATION_READY une fois la dépendance levée
```

**Promotion interdite :**

```text
DOC_ONLY_REFERENCE → USABLE_NOW (INTERDIT)
DOC_ONLY_INITIAL_PROJECT → USABLE_LIMITED (INTERDIT — pas de preuve d'usage)
DOC_ONLY → USABLE_NOW (INTERDIT sans preuve d'usage réel documentée)
```

### 3.2 SIMULATED_ONLY — 3 sous-types

| Sous-type | Définition | Exemple |
|---|---|---|
| `SIMULATED_ONLY_TEST` | Smoke test uniquement, pas de scénario réel | Botpress Adapter (smoke test réussi, pas d'usage Telegram réel) |
| `SIMULATED_ONLY_BACKTEST` | Backtest exécuté sur données historiques, pas d'exécution live | BTC COIN-M après backtest (futur) |
| `SIMULATED_ONLY_IMPLEMENTATION_READY` | Tests passés, prêt pour usage réel une fois credentials/config en place | Botpress avec webhook Telegram configuré (futur) |

**Règles de promotion pour SIMULATED_ONLY :**

```text
SIMULATED_ONLY_TEST → SIMULATED_ONLY_IMPLEMENTATION_READY après closeout de test complet + config prête
SIMULATED_ONLY_BACKTEST → SIMULATED_ONLY_IMPLEMENTATION_READY après backtest PASS sur jeu complet
SIMULATED_ONLY_IMPLEMENTATION_READY → USABLE_LIMITED après premier usage réel documenté (>1 session, >1 utilisateur)
```

**Promotion interdite :**

```text
SIMULATED_ONLY_TEST → USABLE_NOW (INTERDIT — un smoke test n'est pas un usage réel)
SIMULATED_ONLY_BACKTEST → USABLE_LIMITED (INTERDIT — un backtest n'est pas un usage réel)
SIMULATED_ONLY → USABLE_NOW (INTERDIT sans preuve d'usage réel)
```

### 3.3 USABLE_LIMITED — 3 sous-types

| Sous-type | Définition | Exemple |
|---|---|---|
| `USABLE_LIMITED_CONSTRAINED` | Utilisable avec limites documentées | ClickUp Cockpit (limité à la lecture cockpit) |
| `USABLE_LIMITED_NEEDS_EXTERNAL` | Utilisable mais dépend de services externes non garantis | TradingView Alert Pipeline (dépend de TV webhook) |
| `USABLE_LIMITED_PARTIAL_MODULE` | Module partiellement opérationnel, certaines fonctions non validées | Desk Pro (toutes les surfaces pas encore consolidées) |

**Règles de promotion vers USABLE_NOW :**

```text
USABLE_LIMITED_CONSTRAINED → USABLE_NOW après levée des contraintes documentées + preuve
USABLE_LIMITED_NEEDS_EXTERNAL → USABLE_NOW après garantie de disponibilité externe (monitoring)
USABLE_LIMITED_PARTIAL_MODULE → USABLE_NOW après consolidation complète + closeout
```

**Promotion interdite :**

```text
USABLE_LIMITED → USABLE_NOW sans preuve de levée de TOUTES les limites documentées
```

### 3.4 USABLE_NOW — 2 sous-types

| Sous-type | Définition | Exemple |
|---|---|---|
| `USABLE_NOW_FULL` | Produit fini, usage complet, toutes preuves fournies | Repo KG |
| `USABLE_NOW_MONITORED` | Produit fini avec surveillance continue obligatoire | (futur) |

**Promotion :**

```text
USABLE_NOW est le niveau maximal atteignable dans l'Atlas.
PRODUCT_FINISHED est le statut cible de la taxonomy, mais c'est USABLE_NOW dans l'Atlas.
Le label PRODUCT_FINISHED peut être utilisé dans les closeouts uniquement avec preuve complète.
```

### 3.5 FORBIDDEN_LIVE — 1 sous-type

| Sous-type | Définition | Exemple |
|---|---|---|
| `FORBIDDEN_LIVE_ACTIVE_DEVELOPMENT` | Interdit en live car en développement actif | BTC COIN-M Accumulation Engine |

**Promotion interdite :**

```text
FORBIDDEN_LIVE → tout autre bucket (INTERDIT tant que le flag FORBIDDEN_LIVE est actif)
La levée du flag FORBIDDEN_LIVE nécessite :
  - closeout complet du chantier
  - revue de sécurité
  - preuve de non-régression
  - décision opérateur explicite
```

### 3.6 NOT_USABLE_YET (hors Atlas, dans la taxonomy)

Sous-types définis dans `01_PRODUCT_STATUS_TAXONOMY.md` :

```text
NOT_USABLE_YET_UNSTARTED
NOT_USABLE_YET_BLOCKED
NOT_USABLE_YET_NEEDS_PROOF
```

Ces statuts ne sont pas dans l'Atlas (l'Atlas ne liste que les produits avec un usage défini). Ils servent dans la phase d'audit et de classification.

## 4_PREUVES_REQUISES_PAR_PROMOTION

| Promotion | Preuve minimale |
|---|---|
| DOC_ONLY → SIMULATED_ONLY | Closeout de test PASS + logs + captures |
| SIMULATED_ONLY → USABLE_LIMITED | 1+ session d'usage réel documentée |
| USABLE_LIMITED → USABLE_NOW | Toutes limites levées + 5+ sessions d'usage sans échec |
| FORBIDDEN_LIVE → autre | Closeout complet + revue sécurité + décision opérateur |

## 5_RETROGRADATION

La rétrogradation est possible et doit être traitée explicitement :

```text
Triggers :
  - un test de non-régression échoue
  - un service externe devient indisponible
  - un bug bloquant est découvert
  - une dépendance est cassée

Action :
  USABLE_NOW → USABLE_LIMITED (si contrainte documentable)
  USABLE_LIMITED → SIMULATED_ONLY (si plus utilisable en réel)
  SIMULATED_ONLY → DOC_ONLY (si le test n'est plus reproductible)
```

## 6_ANTI_REGLES — Promotions implicites interdites

```text
A1. PASS chantier ≠ USABLE_NOW
A2. Un guide écrit ≠ usage réel prouvé
A3. Un closeout documentaire ≠ preuve d'usage
A4. OpenClaw qui lance un script ≠ produit fini
A5. Une app externe qui fonctionne = projection, pas canon
A6. Un worker qui tourne en simulation ≠ utilisable en réel
A7. Un backtest PASS ≠ stratégie live
A8. Une PR mergée ≠ promotion automatique
A9. Un commentaire "ça marche" dans un chat ≠ preuve
A10. Une absence d'erreur dans les logs ≠ succès validé
```

## 7_MATRICE_DE_TRANSITION

Table complète des transitions autorisées (✓) et interdites (✗) :

```text
                        → DOC_ONLY  → SIMULATED → USABLE_LTD → USABLE_NOW → FORBIDDEN
DOC_ONLY                |    -      |    ✓(1)    |    ✗       |    ✗       |    ✗
SIMULATED_ONLY          |    ✓(r)   |    -       |    ✓(2)    |    ✗       |    ✗
USABLE_LIMITED          |    ✓(r)   |    ✓(r)    |    -       |    ✓(3)    |    ✗
USABLE_NOW              |    ✓(r)   |    ✓(r)    |    ✓(r)    |    -       |    ✗
FORBIDDEN_LIVE          |    ✗      |    ✗       |    ✗       |    ✗       |    -
NOT_USABLE_YET          |    ✓(0)   |    ✗       |    ✗       |    ✗       |    ✓(f)

(0) = après initial project doc + cadrage
(1) = après test simulé PASS + closeout
(2) = après 1+ session d'usage réel documentée
(3) = après levée de toutes les limites + 5+ sessions sans échec
(r) = rétrogradation (autorisée)
(f) = flag FORBIDDEN_LIVE activé explicitement
```

## 17_RESUME_POINT

```text
5 buckets × sous-types détaillés.
Chaque promotion nécessite une preuve minimale explicite.
10 anti-règles contre les promotions implicites.
Matrice de transition complète avec conditions.
Rétrogradation autorisée et documentée.
```

## RISKS

- À qualifier.
