---
doc_id: GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01_SCOPE
doc_type: chantier_scope
repo: opt-trading
project: opt-trading
module: web3_data_adapters
go_id: GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01
status: draft
lifecycle_stage: opened
topic_keys:
  - skyai
  - web3_ai_data
  - openclaw
  - opt_trading
  - mcp
  - onchain_data
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-29
links:
  - docs/chantiers/GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01/10_VENDOR_MATRIX.md
  - docs/chantiers/GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01/20_INTEGRATION_PLAN.md
  - docs/chantiers/GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01/30_SESSION_CAPTURE.md
  - docs/index/inbox/GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01.md
---

# GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01 — Scope parent

## 1_MASTER_TARGET

Comparer les solutions `AI x Web3 data` pour décider lesquelles peuvent alimenter `OpenClaw + opt-trading` sans créer de dépendance fragile ni d'appel direct depuis le runtime trading.

## 2_INITIAL_PROJECT_DOC

Document initial de référence du chantier :

- `docs/chantiers/GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01/00_SCOPE.md`

Ce document fige le cadrage initial. Les documents dérivés du chantier détaillent la matrice fournisseur, l'architecture d'intégration et la capture de session.

## 3_INITIAL_NEED

Demande initiale :

- analyser `https://skyai.pro/#/`
- identifier les produits similaires
- comparer `SkyAI / Chainbase / Covalent-GoldRush / Cookie DAO / Arkham / Nansen / The Graph`
- préparer une intégration éventuelle dans `OpenClaw + opt-trading`
- documenter les deux premières réponses de cadrage pour ne plus dépendre de la session ChatGPT

## 4_MASTER_PROJECT_PLAN

Plan maître retenu :

1. Qualifier les fournisseurs par rôle réel.
2. Séparer les couches : data brute, MCP/agents, signaux trading, analytics humains.
3. Ne pas choisir SkyAI par défaut.
4. Évaluer d'abord les options techniquement exploitables.
5. Proposer une couche `web3_data_adapters` interne à `opt-trading`.
6. Interdire les appels directs fournisseur depuis `OpenClaw`, `risk_engine`, `probability_engine` ou `desk_pro`.

## 5_GO_PLAN

Workstream documentaire initial :

- `10_VENDOR_MATRIX.md` : comparaison des fournisseurs.
- `20_INTEGRATION_PLAN.md` : architecture d'intégration prudente.
- `30_SESSION_CAPTURE.md` : capture consolidée des réponses précédentes.
- `docs/index/inbox/GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01.md` : entrée atomique d'indexation.

## 6_FINAL_TARGET

Livrable attendu de cette phase :

- matrice comparative claire ;
- verdict d'intégration par fournisseur ;
- plan de module `modules/web3_data_adapters/` ;
- point de reprise opératoire pour tests futurs ;
- aucun patch runtime.

## 7_CANONICAL_STATE

État établi au démarrage :

- SkyAI est lu comme fournisseur potentiel `AI x Web3 data / MCP` à valider.
- Chainbase est le candidat le plus proche en zone `MCP + data blockchain pour agents`.
- Covalent / GoldRush est un candidat prioritaire pour data/API structurée.
- The Graph est un socle d'indexation stable, mais moins agent-first.
- Cookie DAO est utile pour signaux narratifs/social/agents crypto.
- Arkham et Nansen sont plus proches de l'intelligence trading et wallet intelligence que d'une infra MCP ouverte.

## 8_VALIDATED_PLAN

Étapes validées :

1. Ouvrir un chantier parent documentaire.
2. Créer une branche dédiée.
3. Documenter les réponses précédentes.
4. Préparer la matrice comparative.
5. Préparer un plan d'intégration `OpenClaw + opt-trading`.
6. Conserver SkyAI en watchlist tant que l'API, les limites, le coût et la stabilité ne sont pas validés.

## 9_SELECTED_SOLUTION

Solution provisoire :

```text
OpenClaw
  ↓
Data Adapter Layer opt-trading
  ↓
[Chainbase MCP] + [Covalent/GoldRush API] + [The Graph]
  ↓
risk_engine / probability_engine / desk_pro
```

## 10_SELECTED_SETUP

Branche dédiée :

```text
go/GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01
```

Dossier chantier :

```text
docs/chantiers/GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01/
```

## 11_KEY_DECISIONS

- Ne pas intégrer SkyAI directement au runtime trading.
- Passer par une couche interne d'adapters.
- Prioriser les fournisseurs avec API/documentation concrète.
- Séparer les fournisseurs d'infra data des plateformes d'analyse/trading.

## 12_INVARIANTS

- Aucun appel fournisseur direct depuis le runtime trading.
- Aucun secret/API key dans la documentation.
- Aucun choix de fournisseur avant test réel.
- Aucun autotrading déclenché par ce chantier.
- Aucun patch runtime dans cette phase documentaire.

## 13_ESTABLISHED

- Le besoin est un cadrage fournisseur + architecture d'intégration.
- Le chantier est documentaire au démarrage.
- L'intégration éventuelle doit être indirecte via adapter layer.

## 14_HYPOTHESIS

À valider :

- SkyAI dispose d'une API/MCP réellement utilisable hors marketing.
- Chainbase MCP est directement exploitable par OpenClaw ou un worker adjacent.
- Covalent / GoldRush offre les meilleurs endpoints pour data structurée production.
- The Graph peut servir aux requêtes ciblées quand un subgraph fiable existe.

## 15_REMAINING_GAP

- Vérifier docs officielles et limites actuelles.
- Identifier coûts, rate limits, auth, formats JSON.
- Tester un fetch minimal par fournisseur prioritaire.
- Définir le schéma interne normalisé.

## 16_TODO

- Compléter la matrice fournisseur.
- Documenter les endpoints/API réellement utilisables.
- Proposer le squelette `modules/web3_data_adapters/`.
- Préparer un GO enfant d'implémentation si un fournisseur est retenu.

## 17_RESUME_POINT

Reprise :

```text
GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01
Branche : go/GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01
État : chantier parent documentaire ouvert.
Prochaine étape : compléter la matrice fournisseur et préparer le plan de test adapters.
```
