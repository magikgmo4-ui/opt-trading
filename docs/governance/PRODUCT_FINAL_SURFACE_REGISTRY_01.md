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
  - docs/chantiers/GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_FINAL_REGISTRY_01/00_INITIAL_PROJECT_DOC.md
---

# PRODUCT_FINAL_SURFACE_REGISTRY_01

## Objectif

Séparer explicitement les produits finaux utilisables, les chaînes produit complètes, les surfaces opérables, les supports critiques et les surfaces de gouvernance/transport.

Ce registre corrige la lecture trop étroite où seuls `Desk Pro`, `Trading Dual Stack V1` et `Bot Vision` étaient visibles comme centres de gravité. Il ne supprime pas ces centres ; il ajoute une couche de lecture plus utile pour fermer ou rouvrir les chantiers selon le `MASTER_TARGET` réel.

## Règle de fermeture

Un parent produit ne peut être fermé que si la surface finale associée est utilisable, testable ou reprenable sans gap bloquant. Une PR, un patch, un bundle ou un GO livré ne suffit pas.

## Niveaux

| Niveau | Nom | Définition |
|---|---|---|
| P0 | Produit final total | Écosystème opt-trading utilisable de bout en bout |
| P1 | Produit final utilisable | Surface ou chaîne directement utile à l’opérateur |
| P2 | Surface opérable / transverse | Surface nécessaire mais pas toujours produit autonome |
| P3 | Support critique | Infrastructure, machine, worker, wrapper, collector, gouvernance |
| P4 | Transport / preuve | Bundle, patch, zip, PR, closeout, index |

## Registre des produits et surfaces finales

| ID | Niveau | Produit / surface finale | Master target / rattachement | Usable when | Statut subjectif |
|---|---:|---|---|---|---|
| `PF_OPT_TRADING_TOTAL_SYSTEM` | P0 | Produit final total opt-trading | umbrella produit global | signal → analyse → décision → suivi → learning est lisible et opérable | À formaliser |
| `PF_SIGNAL_CHAIN_PRODUCT` | P1 | Signal Chain Product | `MT_SIGNAL_CHAIN_PRODUCT` | TradingView/webhook → signal_event → Desk Pro → score → Telegram/Sheets/Perf fonctionne en dry-run contrôlé | Actif |
| `PF_DESK_PRO` | P1 | Desk Pro fonctionnel | `MT_DESKPRO_UI` | cockpit opérateur stable avec snapshots, score, perf, synthèse, reprise | Actif |
| `PF_TELEGRAM_SCREENER` | P1 | Telegram Screener opérationnel | Signal Chain / Telegram inbound | channels/screener lisibles, watch-only, latence connue, routage clair | À promouvoir |
| `PF_BOT_VISION_HEADLESS` | P1 | Bot Vision / Headless Screener | Bot Vision / collectors vision | screenshots → vision_context → Desk Pro artefacts exploitables | Actif mais à stabiliser |
| `PF_OPERATOR_REMOTE_RUNTIME` | P1 | Runtime opérateur distant | OpenClaw/OpenCode/tmux runtime | phone/SSH/tmux/OpenCode/OpenClaw/repo opérable à distance | À promouvoir |
| `PF_OPENCLAW_OPERATOR` | P1 | OpenClaw / OpenCode Operator Runtime | strict workers / orchestrator | ask/build/evaluate/review contrôlés avec logs et gates | À promouvoir |
| `PF_LOCALCMS_COCKPIT` | P1 | LocalCMS cockpit système | LocalCMS / UI consumer | lecture read-only stratégie, métriques, journal, reprise | À promouvoir |
| `PF_STRATEGY_FRAMEWORK` | P1 | Strategy Framework + Registry | `MT_STRATEGY_FRAMEWORK` | stratégies ajoutables, observables, comparables, promouvables/retirables | Actif |
| `PF_PERF_ENGINE_TRADING_LAB` | P1 | Perf Engine + Trading Lab | Strategy / evaluation | replay, labelling, perf evidence, promotion gate | À consolider |
| `PF_GOOGLE_SHEETS_CONSUMER` | P2 | Google Sheets global consumer | reporting / journal | export contrôlé, suivi quotidien, no auto-write non validé | Support final |
| `PF_MARKET_DATA_COLLECTORS` | P2 | Market/API/Data collectors | collectors | données market/derivatives/ticks normalisées et fiables | Support critique |
| `PF_NOTIFICATION_DISPATCHER` | P2 | Telegram outbound dispatcher | notification surface | events structurés : signal, score, approval, erreur, résultat | Support opérable |
| `PF_VALIDATION_RISK_GATE` | P2 | Validation Gate / Risk Gate | risk/live guard | no live without gate ; risk limits, kill switch, approval | Critique |
| `PF_TRADE_EXECUTOR_SIMEX` | P2 | Trade Executor / Simex bridge | execution dry-run | proposition approuvée → trade simulé contrôlé | Non-live |
| `PF_STRICT_WORKERS_RUNNER` | P2 | Strict Workers Runner / AI Team orchestration | `MT_STRICT_WORKERS_RUNNER` | workers bornés, jobs registry, logs, no write sans validation | Actif |
| `PF_FIGMA_FINANCIAL_COCKPIT` | P2 | Figma financial cockpit | visual synthesis | vue visuelle marché → analyse → décision → résultat → learning | Optionnel à confirmer |
| `PF_MULTI_MACHINE_SURFACES` | P3 | Machines admin-trading/db-layer/student/cursor/fantome | satellite machines | responsabilités et anti-conflits clairs | Support |
| `PF_GOVERNANCE_TRANSPORT` | P4 | Governance / bundles / patch / zip / memory bricks | product governance | continuité, transport, audit et reprise sans confusion avec produit fini | Support obligatoire |

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

## Correction cible des index globaux

Les index globaux doivent afficher les parents produits actifs en tenant compte de ce registre. Les surfaces support ne doivent pas être promues en produit final sauf décision explicite.

## NEXT_GO recommandé

```text
GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_CLOSE_GATE_AUDIT_01
```

Objectif : relire les parents actifs et vérifier si leur `MASTER_TARGET` pointe bien vers un `PF_*` testable ou s’il reste trop abstrait.
