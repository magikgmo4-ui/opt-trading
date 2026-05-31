---
doc_id: GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01
parent_go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
status: open
lifecycle_stage: pending_eligibility
topic_keys:
  - opt-trading
  - strategy
  - smc_ict
  - observation
  - semiauto_pilot
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-28
eligibility_gate: "2026-05-30 — Phase 1 : runs≥30, fail_count=0, jours≥14"
working_branch: go/GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01
links:
  - docs/chantiers/GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01/10_STRATEGY_SPEC_SMC_ICT_CHOCH_BOS_RETEST.md
  - docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/95_STRATEGY_REGISTRY.md
  - modules/automation_ops/semiauto_pilot/pilot_runner.py
---

# GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01

## 1_OBJECTIF

Premier run semi-auto contrôlé sur un GO produit réel : activer la phase d'observation paper
de la stratégie `SMC_ICT_CHOCH_BOS_RETEST` (`v0.1.0`).

Le pilote semi-auto v1 prépare le handoff opérateur — spec observée, ObservationEvents à
logger, scoring initial. Gate humain décide de l'activation.

## 2_CONTEXTE

`MASTER_TARGET_AUTOMATION_OPS_SEMIAUTO_V1` est fermé/prouvé (PR #929, 2026-05-28).
La stratégie `SMC_ICT_CHOCH_BOS_RETEST` est en statut `CANDIDATE` dans le registry
(`GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/95_STRATEGY_REGISTRY.md`, entrée #1).

La spec est complète — 12 fichiers posés dans
`GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01` (CLOSED/PASS, 2026-05-19) :
règles CHOCH/BOS, Sweep Liquidity, FVG/OB, ObservationEvent mapping, scoring initial,
Telegram watch signal, perf engine metrics.

Ce GO est le **premier GO produit réel** passant par la boucle semi-auto v1 avec gate
humain obligatoire.

## 3_GATE_ELIGIBILITÉ

```
NE PAS OUVRIR avant 2026-05-30.

Conditions requises (vérifier le 2026-05-30) :
  - Phase 1 runs  ≥ 30
  - Phase 1 jours ≥ 14
  - fail_count    = 0
  - kill switch   testé = oui

Source : modules/automation_ops/semiauto_pilot/pilot_runner.py (dry_run)
         + vérification manuelle état Phase 1.
```

## 4_CAS_RÉEL

Le pilote semi-auto lit le GO_PROMPT JSON suivant :

```json
{
  "go_id": "GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01",
  "action": "activate_paper_observation",
  "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
  "strategy_version": "0.1.0",
  "target_lifecycle": "ACTIVE_PAPER",
  "observation_window_days": 14,
  "human_gate_required": true
}
```

Actions en scope (lecture seule avant gate humain) :
- Lire `10_STRATEGY_SPEC_SMC_ICT_CHOCH_BOS_RETEST.md` — règles d'entrée/sortie
- Lire `50_OBSERVATION_EVENT_MAPPING.md` — champs ObservationEvent attendus
- Lire `60_SCORING_INITIAL.md` — critères de scoring
- Produire un résumé d'activation : signaux à surveiller, ObservationEvents à poster,
  seuils de promotion vers `ACTIVE_LIVE`

Aucun ordre envoyé. Aucune modification du registry. Dry_run uniquement.

## 5_CONTRAINTES

- Mode paper/observation uniquement — `dry_run: true`, aucun ordre Bitget.
- `human_gate_required: true` — l'opérateur valide le résumé d'activation avant
  tout changement de statut dans le registry.
- Phase 1 gate obligatoire avant ouverture de branche.
- Pas de modification automatique de `95_STRATEGY_REGISTRY.md`.
- `secrets/` non touché.

## 6_LIVRABLES

```
docs/chantiers/GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01/
  00_INITIAL_PROJECT_DOC.md              ← ce fichier
  10_ELIGIBILITY_CHECK.md                ← vérification Phase 1 le 2026-05-30
  20_SEMIAUTO_RUN_REPORT.md              ← rapport de run pilote + handoff
  30_ACTIVATION_SUMMARY.md              ← résumé gate humain : signaux, ObsEvents, seuils
  40_GAPS_AND_NEXT_GO.md                 ← gaps identifiés + GO suivant (ex. ACTIVE_LIVE)

artifacts/automation_ops/semiauto_pilot/pilot_<run_id>/
  proof.json
  proof_summary.md
```

## 7_CRITÈRES_DE_FERMETURE

```
- Phase 1 eligibility vérifiée et documentée dans 10_ELIGIBILITY_CHECK.md
- run_id généré, proof.json PASS_DRY_RUN présente
- 30_ACTIVATION_SUMMARY.md complété
- Gate humain documenté : opérateur a lu et validé le résumé d'activation
- strategy_id SMC_ICT_CHOCH_BOS_RETEST promu ACTIVE_PAPER dans le registry
  (seule mutation autorisée, après gate humain)
- 17/17 tests pilote PASS
```

## 8_HORS_PÉRIMÈTRE

- Ordres live ou paper-trading avec exécution réelle.
- Modification des règles SMC_ICT (spec figée depuis OBSERVATION_SIGNAL_ENRICHMENT_01).
- Enrichissement de `pilot_runner.py`.
- Activation d'autres stratégies du registry dans ce GO.
- Chaînage automatique vers `ACTIVE_LIVE`.
