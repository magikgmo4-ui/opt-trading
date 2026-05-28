---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01_REGISTRY_DECISION
doc_type: decision_log
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01
status: open
lifecycle_stage: registry_v1_complete
topic_keys: [code_registry, decision, format, code_ops]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
---

# 20_REGISTRY_DECISION

## Format du registre

**Décision** : Markdown (primaire).

**Fichier** : `docs/registry/CODE_REGISTRY.md`

**Motif** :
- lisible directement sans outil ;
- versionnable via git diff ;
- suffisant pour la v1 (guidance humaine + Cursor/IDE) ;
- JSON possible en dérivé outillé si besoin prouvé.

**JSON différé** à l'ouverture de `tools/code_ops/validate_code_registry.py`
quand la validation automatique deviendra nécessaire.

---

## Périmètre de la v1

Entrées incluses dans cette passe :
- Section 1 : services FastAPI
- Section 2 : moteurs runtime
- Section 3 : trading lab / realtime V1
- Section 4 : desk pro / vision
- Section 5 : collecteurs
- Section 6 : openclaw / agents
- Section 7 : validateurs et schémas
- Section 8 : infra / fleet
- Section 9 : registry readers
- Section 10 : GitHub Actions workflows
- Section 11 : entrées BLOCKED
- Section 12 : DELETE_CANDIDATE
- Section 13 : anomalies

**Entrées non incluses dans v1** (scope LOW — batch suivant) :
- `tools/strategy/` fetch + run scripts (~15 entrées)
- `scripts/ai/workers/` (~10 entrées)
- Modules deepseek, kil_v1, datasheet_writer, learning_feeder, etc.
- 83 `scripts/cmd.sh` des modules

---

## Décisions sur les doublons

Voir `10_DEDUP_QUALIFICATIONS.md` pour le détail.

Résumé :
- D01 : FAUX DOUBLON — perf/engine est wrapper compat
- D02 : FAUX DOUBLON — deux executors deux flux
- D03 : FAUX DOUBLON — engines/router réel, modules/router/ shell vide
- D04 : FAUX DOUBLON — bitget_bridge.py est wrapper entrypoint
- D05 : ANOMALIE — scripts doublés execution_engine → batch dédié
- D06 : DELETE_CANDIDATE — .bak/ → batch nettoyage

---

## Validateur futur

```text
tools/code_ops/validate_code_registry.py
```

Critères futurs :
- identifiants uniques dans CODE_REGISTRY.md ;
- chemins existants vérifiés (`git ls-files`) ;
- rôles et statuts dans les valeurs contrôlées ;
- pas de DELETE_CANDIDATE sans champ `preuve_requise` ;
- tests référencés existants.

Ce validateur sera créé dans un batch dédié (hors ce child GO).

---

## Verdict

```text
PASS_REGISTRY_V1_COMPLETE

Registre v1 livré : docs/registry/CODE_REGISTRY.md
~70 entrées (HIGH + MEDIUM priorités).
6 doublons suspects qualifiés.
5 entrées BLOCKED identifiées.
2 DELETE_CANDIDATE documentées.
6 anomalies listées.

NEXT_GO = GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01
```
