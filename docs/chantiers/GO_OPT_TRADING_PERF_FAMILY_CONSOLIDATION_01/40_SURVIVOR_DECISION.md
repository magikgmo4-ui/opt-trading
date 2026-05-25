---
doc_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01_SURVIVOR_DECISION
doc_type: family_decision
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: decision
topic_keys:
  - opt-trading
  - modules
  - perf
  - survivor
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_FAMILY_CONSOLIDATION_01/30_RUNTIME_SURFACE_MAP.md
---

# 40_SURVIVOR_DECISION

## Reponses tranchees

### 1. `perf_engine` est-il bien le survivant canonique ?

Verdict: **non, pas comme survivant canonique unique de famille**.

`perf_engine` reste :

- le noyau logique historique reel
- un composant runtime utile
- un chemin encore consomme par wrappers, tests et compatibilite

Mais la canonicalite de chemin de famille a deja bascule vers `modules/perf/*`.

### 2. Quel est le survivant canonique de famille ?

Verdict retenu pour ce GO doc-only:

- **owner canonique documentaire + facade canonique de famille: `perf`**
- **composant moteur historique encore actif: `perf_engine`**

### 3. `perf` est-il legacy, compat, doc/gouv ou runtime utile ?

Verdict: **runtime utile + compat canonique**, pas legacy, pas doc/gouv.

Pourquoi :

- les launchers actifs utilisent `modules.perf.app:app`
- `modules.perf.engine.app.perf_engine` est le chemin canonique choisi par l'orchestrateur
- `modules/perf` heberge les shims Python, les wrappers et l'outillage DB de la famille

## Classement final de famille

| Surface | Classement |
| --- | --- |
| `modules/perf/` | survivant canonique documentaire + runtime utile |
| `modules/perf_engine/` | composant historique actif / compat moteur |

## Implication cle

La famille `perf` est moins proche du cas `vision` que du cas d'une facade consolidee avec implementation differee.

Le point de tension n'est pas un doublon nominal pur.
Le point de tension est un **split entre facade canonique et implementation moteur**.

## Verdict

**PASS**

La famille peut etre clarifiee sans mutation runtime :

- `perf` = owner canonique de famille
- `perf_engine` = moteur historique encore utile
