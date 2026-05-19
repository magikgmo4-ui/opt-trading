---
doc_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01_ORPHAN_AUDIT
doc_type: orphan_audit
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
status: draft_for_review
lifecycle_stage: child_audit
parent_go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - audit
  - orphan-modules
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/01_ORPHAN_AUDIT.md
point_de_reprise: "Audit documentaire des 10 modules orphelins avec décision par module."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/04_SYNTHESIS_AND_HYPOTHETICAL_TREE.md
---

# 01_ORPHAN_AUDIT

## 1_METHODE

```text
Pour chaque module "A AUDITER" :
1. Vérifier la présence du répertoire/fichier dans le repo.
2. Lire le code source (s'il existe) pour inférer le rôle.
3. Vérifier les dépendances (imports, références croisées).
4. Vérifier si le module est référencé dans les docs canoniques.
5. Produire une décision : ARCHIVE / KEEP_CANDIDATE / RATTACHER.
6. Justifier la décision.
```

## 2_AUDIT_PAR_MODULE

---

### 2.1 kil_v1

```text
LOCATION   : modules/kil_v1/
ROLE INFÉRÉ : INCONNU. Aucun fichier Python exploitable, aucune doc.
DÉPENDANCES : Aucune référence croisée trouvée dans les docs canoniques.
USAGE       : Aucun. Module jamais référencé dans un chantier ou un index.
CODE        : Répertoire présent mais contenu minimal/non fonctionnel.

DÉCISION    : ARCHIVE
JUSTIFICATION : Module sans rôle identifiable, sans usage, sans documentation.
                Conserver dans _archive/legacy_modules/kil_v1/ pour traçabilité.
```

### 2.2 hf_free_platform

```text
LOCATION   : modules/hf_free_platform/
ROLE INFÉRÉ : Interface vers Hugging Face Hub (gratuit). Probablement utilisé
              pour télécharger des modèles ou exécuter des tâches HF sans token payant.
DÉPENDANCES : Aucune référence canonique. Potentiellement lié à deepseek_student
              ou aux anciens scripts student/.
USAGE       : Aucune preuve documentée. Module présent mais non référencé.
CODE        : Répertoire présent.

DÉCISION    : ARCHIVE
JUSTIFICATION : Pas de documentation, pas de preuve d'usage, pas de chantier actif.
                Si le besoin HF renaît, un nouveau module sera créé via un GO dédié.
```

### 2.3 mimo_open_observer

```text
LOCATION   : modules/mimo_open_observer/
ROLE INFÉRÉ : Observateur pour le protocole/stratégie MIMO (Multi-Input Multi-Output).
              Probablement un observateur de marché ou de signaux.
DÉPENDANCES : Aucune référence canonique.
USAGE       : Aucune preuve documentée.
CODE        : Répertoire présent.

DÉCISION    : ARCHIVE
JUSTIFICATION : Pas de documentation, pas de preuve d'usage.
                Le concept MIMO n'est documenté nulle part dans opt-trading.
```

### 2.4 strategy_engine

```text
LOCATION   : modules/strategy_engine/
ROLE INFÉRÉ : Moteur de stratégie de trading. Probablement lié aux engines
              de décision/exécution/position.
DÉPENDANCES : Cluster STRATEGY (decision_engine, execution_engine, position_engine,
              portfolio_engine). Tous sont KEEP_CANDIDATE.
USAGE       : Module présent mais isolé, éclaté, peu documenté.
CODE        : Présent mais fragmenté entre 5 modules.

DÉCISION    : RATTACHER au cluster STRATEGY (voir 02_CONSOLIDATION_PLAN)
JUSTIFICATION : Fait partie du cluster STRATEGY identifié. Pas orphelin isolé
                mais membre d'une famille éclatée. Traité dans la consolidation.
```

### 2.5 marketdata

```text
LOCATION   : modules/marketdata/
ROLE INFÉRÉ : Gestion et distribution des données de marché. Possible interface
              unifiée au-dessus des collectors.
DÉPENDANCES : Référencé dans ui_registry et indexation_desk. Lié au cluster COLLECTORS.
USAGE       : Module présent. Mentionné dans les index mais rôle exact flou.
CODE        : Présent.

DÉCISION    : RATTACHER au cluster COLLECTORS (voir 02_CONSOLIDATION_PLAN)
JUSTIFICATION : Rôle flou mais référencé. Fait partie du cluster COLLECTORS.
                La consolidation clarifiera s'il est un point d'entrée unifié
                ou un doublon à archiver.
```

### 2.6 webhook_server.py

```text
LOCATION   : webhook_server.py (racine du repo)
ROLE INFÉRÉ : Entrypoint runtime historique du webhook. Reçoit les alertes
              TradingView et les dispatche.
DÉPENDANCES : Doublon potentiel avec modules/webhook/ déjà couvert par
              le produit TradingView/Telegram Alert Pipeline (dans l'Atlas).
USAGE       : Runtime actif historiquement. Référencé dans REPO_ROOT_POLICY.md.
CODE        : Fichier Python présent à la racine.

DÉCISION    : ARCHIVE (après confirmation que modules/webhook/ couvre le périmètre)
JUSTIFICATION : Doublon fonctionnel. Le produit Atlas "TradingView/Telegram Alert
                Pipeline" couvre déjà ce périmètre via modules/webhook/.
                Conserver le fichier en archive pour référence historique.
                CONDITION : vérifier que modules/webhook/ couvre 100% du périmètre.
```

### 2.7 e2e_telegram_smoke.py

```text
LOCATION   : e2e_telegram_smoke.py (racine du repo)
ROLE INFÉRÉ : Test end-to-end du flux Telegram (Botpress).
DÉPENDANCES : Branche Botpress. Lié au produit Botpress Adapter (Atlas: SIMULATED_ONLY).
USAGE       : Test. Probablement exécuté lors de la phase de smoke test Botpress.
CODE        : Fichier Python présent à la racine.

DÉCISION    : RATTACHER au produit Botpress Adapter
JUSTIFICATION : Fichier de test lié à Botpress. Doit être déplacé dans
                modules/botpress_adapter/tests/ ou un répertoire dédié.
                Ne pas laisser de scripts de test à la racine.
```

### 2.8 smoke_adapter.py

```text
LOCATION   : smoke_adapter.py (racine du repo)
ROLE INFÉRÉ : Adaptateur de smoke test. Probablement lié à Botpress ou au pipeline
              d'alertes.
DÉPENDANCES : Branche Botpress.
USAGE       : Test.
CODE        : Fichier Python présent à la racine.

DÉCISION    : RATTACHER au produit Botpress Adapter
JUSTIFICATION : Même raison que e2e_telegram_smoke.py.
                Déplacer dans un répertoire de tests dédié.
```

### 2.9 smoke.sh

```text
LOCATION   : scripts/smoke.sh (ou racine)
ROLE INFÉRÉ : Script shell de smoke test. Périmètre à confirmer.
DÉPENDANCES : Inconnues.
USAGE       : Script de test.
CODE        : Script shell.

DÉCISION    : RATTACHER à la famille concernée après vérification du contenu
JUSTIFICATION : Si lié à Botpress → rattacher à Botpress Adapter.
                Si lié à TradingView → rattacher à TradingView Pipeline.
                Si orphelin sans cible → ARCHIVE.
                Action : lire le script pour déterminer la cible.
```

### 2.10 smoke_tv_engine.py

```text
LOCATION   : scripts/smoke_tv_engine.py
ROLE INFÉRÉ : Smoke test du moteur TradingView. Probablement lié au pipeline
              d'alertes TradingView.
DÉPENDANCES : TradingView Alert Pipeline (produit Atlas).
USAGE       : Test.
CODE        : Fichier Python dans scripts/.

DÉCISION    : RATTACHER au produit TradingView/Telegram Alert Pipeline
JUSTIFICATION : Fichier de test pour le pipeline TradingView.
                Déplacer dans modules/webhook/tests/ ou scripts dédié.
```

## 3_MATRICE_DE_DECISION

| # | Module | Décision | Cible |
|---|---|---|---|
| 1 | `kil_v1` | **ARCHIVE** | `_archive/legacy_modules/kil_v1/` |
| 2 | `hf_free_platform` | **ARCHIVE** | `_archive/legacy_modules/hf_free_platform/` |
| 3 | `mimo_open_observer` | **ARCHIVE** | `_archive/legacy_modules/mimo_open_observer/` |
| 4 | `strategy_engine` | **RATTACHER** | Cluster STRATEGY |
| 5 | `marketdata` | **RATTACHER** | Cluster COLLECTORS |
| 6 | `webhook_server.py` | **ARCHIVE** | `_archive/` (après vérification) |
| 7 | `e2e_telegram_smoke.py` | **RATTACHER** | Botpress Adapter |
| 8 | `smoke_adapter.py` | **RATTACHER** | Botpress Adapter |
| 9 | `smoke.sh` | **RATTACHER** | Cible à déterminer (lire script) |
| 10 | `smoke_tv_engine.py` | **RATTACHER** | TradingView Pipeline |

## 4_RESUME

```text
ARCHIVE      : 3 modules (kil_v1, hf_free_platform, mimo_open_observer) + 1 fichier (webhook_server.py)
RATTACHER    : 6 fichiers/modules vers leur famille/cluster
CONSOLIDATION: strategy_engine + marketdata → traités dans 02_CONSOLIDATION_PLAN.md
```
