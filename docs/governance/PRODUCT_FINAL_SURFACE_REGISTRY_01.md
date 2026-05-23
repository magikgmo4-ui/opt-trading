---
doc_id: PRODUCT_FINAL_SURFACE_REGISTRY_01
doc_type: product_final_surface_registry
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01
status: reference
lifecycle_stage: governance
surface: governance
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
topic_keys:
  - opt-trading
  - product_final_surface
  - master_target
  - final_surface
  - close_gate
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/PRODUCT_FINAL_TARGET_REGISTRY_01.md
  - docs/governance/PRODUCT_FINAL_SURFACE_CLOSE_GATE_AUDIT_01.md
  - docs/chantiers/GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01/00_INITIAL_PROJECT_DOC.md
---

# PRODUCT_FINAL_SURFACE_REGISTRY_01

## Objectif

Séparer explicitement les produits finaux utilisables, les chaînes produit complètes, les surfaces opérables, les supports critiques et les surfaces de gouvernance/transport.

Ce registre corrige la lecture trop étroite où seuls `Desk Pro`, `Trading Dual Stack V1` et `Bot Vision` étaient visibles comme centres de gravité. Il ne supprime pas ces centres ; il ajoute une couche de lecture plus utile pour fermer ou rouvrir les chantiers selon le `MASTER_TARGET` réel.

## Règle de fermeture

Un parent produit ne peut être fermé que si la surface finale associée est utilisable, testable ou reprenable sans gap bloquant. Une PR, un patch, un bundle, un closeout de phase ou un GO livré ne suffit pas.

## Chaîne canonique target

```text
PF_* -> 1_MASTER_TARGET -> 4_MASTER_PROJECT_PLAN -> 6_FINAL_TARGET -> BUNDLE_TARGET -> GO_ID -> NEXT_GO / CLOSE_GATE
```

- `PF_*` = produit/surface finale utilisable ou chaîne produit complète.
- `1_MASTER_TARGET` = objectif final utilisable de cette surface.
- `4_MASTER_PROJECT_PLAN` = checklist complète de fermeture du parent.
- `6_FINAL_TARGET` = cible de phase.
- `BUNDLE_TARGET` = livrable child/bundle.
- `GO_ID` = unité d'exécution.

## Niveaux

| Niveau | Nom | Définition |
|---|---|---|
| P0 | Produit final total | Écosystème opt-trading utilisable de bout en bout |
| P1 | Produit final utilisable | Surface ou chaîne directement utile à l’opérateur |
| P2 | Surface opérable / transverse | Surface utile et partageable, mais pas toujours produit autonome final |
| P3 | Support critique | Infrastructure, machine, worker, wrapper, collector, gouvernance |
| P4 | Transport / preuve | Bundle, patch, zip, PR, closeout, index |

## Registre des produits et surfaces finales

| ID | Niveau | Produit / surface finale | Master target / rattachement | Usable when | Statut subjectif |
|---|---:|---|---|---|---|
| `PF_OPT_TRADING_TOTAL_SYSTEM` | P0 | Produit final total opt-trading | `MT_OPT_TRADING_TOTAL_SYSTEM` | signal -> analyse -> décision -> suivi -> learning est lisible, opérable et reprenable | À formaliser |
| `PF_DESK_PRO` | P1 | Desk Pro opérationnel | `MT_DESKPRO_UI` | cockpit opérateur stable avec snapshots, score, perf, décision, synthèse, reprise | Actif |
| `PF_DATA_CENTER` | P1 | Data Center | `MT_DATA_CENTER_NORMALIZED_REGISTRY` | producteurs et consommateurs partagent les mêmes contrats de données normalisées | À créer / promouvoir |
| `PF_TELEGRAM_SCREENER` | P1 | Telegram Screener opérationnel | `MT_TELEGRAM_SCREENER_OPERATIONAL` | channels/screener lisibles, watch-only, latence connue, filtrage/routage clair | À promouvoir |
| `PF_TELEGRAM_INGESTION` | P1 | Telegram Ingestion opérationnel | `MT_TELEGRAM_INGESTION_OPERATIONAL` | messages/channels Telegram deviennent des `signal_event` normalisés et stockés | À promouvoir |
| `PF_BOT_VISION_HEADLESS` | P1 | Bot Vision / Headless Screener opérationnel | `MT_BOT_VISION_HEADLESS_OPERATIONAL` | screenshots -> vision_context -> artefacts exploitables par Desk Pro/strategy | Actif à stabiliser |
| `PF_SIGNAL_CHAIN_PRODUCT` | P1 | Signal Chain Product complet | `MT_SIGNAL_CHAIN_PRODUCT` | TradingView/webhook/Telegram/API -> signal_event -> Desk Pro -> score -> Telegram/Sheets/Perf fonctionne en dry-run contrôlé | Actif |
| `PF_OPENCLAW_ORCHESTRATOR_FULL` | P1 | OpenClaw Orchestrator FULL | `MT_OPENCLAW_ORCHESTRATOR_FULL` | jobs, workers, review, build, evaluate, logs et gates sont orchestrés de bout en bout | À promouvoir |
| `PF_OPERATOR_RUNTIME` | P1 | OpenClaw / OpenCode Operator Runtime | `MT_OPERATOR_RUNTIME` | phone/SSH/tmux/OpenCode/OpenClaw/repo opérable à distance avec reprise | À promouvoir |
| `PF_LOCALCMS_COCKPIT` | P1 | LocalCMS cockpit système | `MT_LOCALCMS_COCKPIT` | lecture read-only stratégie, métriques, journal, navigation, reprise | À promouvoir |
| `PF_STRATEGY_FRAMEWORK_REGISTRY` | P1 | Strategy Framework + Registry | `MT_STRATEGY_FRAMEWORK` | stratégies ajoutables, observables, comparables, promouvables/retirables par `strategy_id` | Actif |
| `PF_PERF_ENGINE_TRADING_LAB` | P1 | Perf Engine / Trading Lab | `MT_PERF_ENGINE_TRADING_LAB` | replay, labelling, backtest, perf evidence, promotion/retrait et reporting sont disponibles | À consolider |
| `PF_GOOGLE_SHEETS_CONSUMER` | P2 | Google Sheets global consumer | `MT_GOOGLE_SHEETS_GLOBAL_CONSUMER` | export contrôlé, suivi quotidien, journal/reporting, sans write automatique non validé | Support final / consumer |
| `PF_STRICT_WORKERS_AI_TEAM` | P2 | Strict Workers Runner / AI Team orchestration | `MT_STRICT_WORKERS_RUNNER` | workers bornés, job registry, logs, no write sans validation | Actif |
| `PF_FIGMA_FINANCIAL_COCKPIT` | P2 | Figma Financial Cockpit | `MT_FIGMA_FINANCIAL_COCKPIT` | vue visuelle marché -> analyse -> décision -> exécution -> résultat -> learning | Optionnel à confirmer |
| `PF_MULTI_MACHINE_SURFACES` | P3 | Machines admin-trading/db-layer/student/cursor/fantome | support machines | responsabilités, anti-conflits et surfaces d’exécution clairs | Support |
| `PF_GOVERNANCE_TRANSPORT` | P4 | Governance / bundles / patch / zip / memory bricks | product governance | continuité, transport, audit et reprise sans confusion avec produit fini | Support obligatoire |

## Data Center — règle canonique

```text
producer <> registry data <> consumer <> registry data <> producer
```

`PF_DATA_CENTER` représente un registre data normalisé : peu importe l’outil utilisé pour collecter les données, les sorties doivent être normalisées, stockées et rendues compatibles selon les mêmes contrats d’entrée/sortie.

### MASTER_TARGET recommandé

```text
1_MASTER_TARGET:
Data Center opérationnel capable de recevoir, normaliser, stocker et redistribuer les données trading depuis plusieurs producteurs vers plusieurs consommateurs avec contrats d’entrée/sortie compatibles.
```

### 4_MASTER_PROJECT_PLAN minimal

```text
- définir les contrats producer
- définir les contrats consumer
- normaliser les schémas data
- stocker dans un registre commun
- versionner datasets/events
- valider la compatibilité par tests
- fournir lecture aux surfaces : Desk Pro, Strategy, Perf, Telegram, Sheets, LocalCMS
- documenter reprise, gaps, qualité et latence
```

## Supports critiques non promus automatiquement

Ces surfaces restent nécessaires, mais ne sont pas des produits finaux par défaut. Elles doivent être rattachées dans les `4_MASTER_PROJECT_PLAN` comme `required_surfaces`, `support_surfaces`, `dependencies` ou `evidence_sources`.

| Support | Rôle |
|---|---|
| Webhook server | entrée d’événements externe |
| Signal router | routage interne des signaux |
| Proposition engine | génération de propositions |
| Validation gate | approbation, risk gate, no-live-without-gate |
| Notification dispatcher | notification structurée |
| Trade executor dry-run / simex | exécution simulée ou contrôlée |
| Market data collectors | producteurs de données |
| API collectors | producteurs de données |
| Machine split | surfaces d’exécution admin-trading/db-layer/student/cursor/fantome |
| GitHub / bundles / patch / zip / governance docs | transport, preuve, reprise, gouvernance |

## Distinction canonique

```text
Produit final utilisable ≠ worker
Produit final utilisable ≠ patch
Produit final utilisable ≠ PR mergée
Produit final utilisable ≠ index mis à jour
Produit final utilisable = surface testable, opérable, reprenable, sans gap bloquant d’usage réel
```

## Règles de rattachement des GO

Tout nouveau GO doit rattacher son `PRODUCT_OR_SURFACE` à un des cas suivants :

1. un `PF_*` du présent registre ;
2. un support critique explicitement nommé ;
3. une surface de gouvernance/transport si le lot est doc-only ;
4. un nouveau `PF_*` à ajouter avant ouverture si la surface est réellement nouvelle.

Chaque surface finale promue doit avoir son `1_MASTER_TARGET`. Chaque `1_MASTER_TARGET` doit avoir son `4_MASTER_PROJECT_PLAN` avant fermeture parent.

## Correction cible des index globaux

Les index globaux doivent afficher les parents produits actifs en tenant compte de ce registre. Les surfaces support ne doivent pas être promues en produit final sauf décision explicite.

## NEXT_GO recommandé

```text
GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_GAP_REMEDIATION_01
```

Objectif : appliquer la remédiation des écarts entre `MASTER_TARGET`, `PF_*`, supports critiques et plans parent.
