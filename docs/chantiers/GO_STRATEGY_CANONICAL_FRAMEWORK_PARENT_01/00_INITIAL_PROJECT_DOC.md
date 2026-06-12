---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: initial_project_doc
repo: opt-trading
status: open
created_at: 2026-05-17
branch: go/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
surface: doc-only
scope: canonical strategy framework
runtime_mutation: false
---

# 00_INITIAL_PROJECT_DOC
## GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01

---

## 1_MASTER_TARGET

```text
Creer le cadre canonique durable pour ajouter, observer, comparer,
promouvoir ou retirer des strategies de trading dans opt-trading.
```

Ce document est la reference figee du chantier parent.

Le cadre doit permettre d'ajouter une strategie sans creer de pipeline parallele.
Chaque strategie devient une specification canonique enrichissant `ObservationEvent`,
puis elle est evaluee par les surfaces existantes.

---

## 2_INITIAL_NEED

Ajouter des strategies canoniques durables a l'ecosysteme existant :

| Surface | Role dans ce cadre |
| --- | --- |
| Screener headless | Producteur ou pre-producteur de candidats |
| Telegram screener | Watch signal, jamais ordre direct avant validation |
| Bot Vision OpenAI | Evidence visuelle et enrichissement, jamais decision seule |
| TradingView / webhook / screenshot | Source de signal ou evidence source |
| API market data | Contexte de marche et replay |
| Desk Pro | Surface operateur et synthese decisionnelle |
| Perf Engine | Evaluation et preuve de promotion/retrait |
| Trading Lab | Replay, labelling, review |
| Google Sheets | Export controle, jamais write automatique |
| LocalCMS | Vue read-only strategique et metrics |
| ObservationEvent | Point de passage canonique |

Point d'ancrage prioritaire :

```text
ObservationEvent
```

Le PR #524 pose deja `ObservationEvent` V1 et prevoit l'ajout futur de champs
comme `strategy_id`. Ce parent transforme cette possibilite en regle canonique.

---

## 3_CANONICAL_STATE

```text
No live trade
No Bitget order
No automatic Google Sheets write
No runtime mutation au parent doc-only
No duplicate pipeline
No strategy without strategy_id
No strategy promoted without Perf Engine evidence
No Telegram BUY/SELL direct before validation
No Vision-only decision
```

Les strategies ne remplacent pas le pipeline OpenClaw / daily journal / LocalCMS.
Elles enrichissent les evenements qui y passent deja.

---

## 4_MASTER_PROJECT_PLAN

```text
Strategy Candidate
↓
Canonical Strategy Spec
↓
Signal Enrichment
↓
ObservationEvent
↓
Journal daily
↓
LocalCMS strategy view
↓
Perf Engine evaluation
↓
Telegram watch signal
↓
Trading Lab replay
↓
Phase gate
↓
Paper expansion
↓
Live review only
```

Ce flux est logique et documentaire. Il ne cree aucun runtime nouveau dans ce
parent.

---

## 5_VALIDATED_PLAN

Lifecycle strategie :

```text
CANDIDATE
↓
OBSERVED
↓
PAPER_VALIDATED
↓
MULTI_SIGNAL_ELIGIBLE
↓
LIVE_REVIEW_ONLY
```

Champs minimum :

```text
strategy_id
strategy_version
setup_type
direction
symbol
timeframe
signal_source
evidence_source
confidence
entry_zone
invalidation
target_zone
risk_profile
observation_status
perf_status
promotion_gate
retirement_gate
```

Decision canonique :

| Regle | Decision |
| --- | --- |
| Identification | Toute strategie passe par `strategy_id` + `strategy_version` |
| Evenement | Toute strategie enrichit `ObservationEvent` |
| Demarrage | Toute strategie commence en `CANDIDATE` |
| Execution | Aucune strategie ne declenche de live |
| SMC/ICT | Premier child strategique, pas une exception |

---

## 6_CHILD_GOS_OBLIGATOIRES

| Child GO | Role |
| --- | --- |
| `GO_STRATEGY_CANONICAL_SPEC_SCHEMA_01` | Schema de specification strategie |
| `GO_STRATEGY_LIFECYCLE_GATES_01` | Gates de promotion et retrait |
| `GO_STRATEGY_OBSERVATION_EVENT_EXTENSION_01` | Extension `ObservationEvent` |
| `GO_STRATEGY_LOCALCMS_VIEW_REQUIREMENTS_01` | Vue strategie LocalCMS |
| `GO_STRATEGY_PERF_ENGINE_EVALUATION_01` | Evaluation Perf Engine |
| `GO_STRATEGY_TELEGRAM_WATCH_SIGNAL_PROTOCOL_01` | Signal Telegram watch-only |
| `GO_STRATEGY_TRADING_LAB_REPLAY_PROTOCOL_01` | Replay Trading Lab |
| `GO_STRATEGY_GOOGLE_SHEETS_EXPORT_MAPPING_01` | Mapping export Sheets |
| `GO_STRATEGY_IDE_BUNDLE_01` | Instructions IDE / reprise |

Premier child strategie :

```text
GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
```

---

## 7_FIRST_STRATEGY_CHILD

SMC/ICT est le premier cas d'application du cadre :

```text
strategy_id = SMC_ICT_CHOCH_BOS_RETEST
setup_type  = SWEEP_CHOCH_BOS_FVG_OB_RETEST
```

Il doit produire des champs observables, testables et comparables. Il ne doit
pas produire un module isole ni un flux d'execution autonome.

---

## 8_SCOPE

Inclus :

- Definition documentaire du cadre canonique strategie.
- Mapping des surfaces existantes.
- Schema minimal de `Canonical Strategy Spec`.
- Extension cible de `ObservationEvent`.
- Gates de lifecycle, promotion et retrait.
- Requirements LocalCMS, Perf Engine, Telegram, Trading Lab et Sheets.
- Preparation du child SMC/ICT.

Exclus :

- Code runtime.
- Mutation de modules.
- Activation live.
- Ordres Bitget.
- Ecriture Google Sheets automatique.
- Modification d'index global sans justification explicite.

---

## 9_DELIVERABLES

```text
docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/
├─ 00_INITIAL_PROJECT_DOC.md
├─ 10_PR_AND_EXISTING_SURFACES_CROSSCHECK.md
├─ 20_STRATEGY_CANONICAL_SPEC_SCHEMA.md
├─ 30_STRATEGY_LIFECYCLE_GATES.md
├─ 40_OBSERVATION_EVENT_EXTENSION.md
├─ 50_LOCALCMS_STRATEGY_VIEW_REQUIREMENTS.md
├─ 60_PERF_ENGINE_STRATEGY_EVALUATION.md
├─ 70_TELEGRAM_WATCH_SIGNAL_PROTOCOL.md
├─ 80_TRADING_LAB_REPLAY_PROTOCOL.md
├─ 85_GOOGLE_SHEETS_EXPORT_MAPPING.md
├─ 90_IDE_BUNDLE_INSTRUCTIONS.md
└─ 99_CLOSEOUT_CRITERIA.md
```

Entree locale :

```text
docs/index/inbox/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01.md
```

---

## 10_RESUME_POINT

```text
Reprendre sur :
GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01

Puis creer :
GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
```

---

## 11_EXPECTED_VERDICT

```text
PASS_STRATEGY_CANONICAL_FRAMEWORK_PARENT_DOC_ONLY_OPENED
```

## RISKS

- À qualifier.
