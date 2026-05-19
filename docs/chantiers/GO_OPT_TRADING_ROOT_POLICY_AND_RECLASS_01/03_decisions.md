---
doc_id: GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01
status: active
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - governance
  - root
  - policy
surface: chantier
source_kind: canonical
updated_at: 2026-04-18
links:
  - docs/governance/REPO_ROOT_POLICY.md
  - docs/ot/trae/06_REPO_BOUNDARY_POLICY_V1.txt
  - docs/governance/REPO_ROLE.md
---

# 03_decisions — GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01

## D1 — Portée de la politique racine
- `REPO_ROOT_POLICY.md` traite la racine canonique interne du repo
- la frontière repo/hors-repo reste portée par `docs/ot/trae/06_REPO_BOUNDARY_POLICY_V1.txt`

## D2 — Règle anti-chevauchement
- pas de duplication des règles “shared/temp/backups”
- `REPO_ROOT_POLICY.md` ne redéfinit pas la doctrine de frontière ; il la référence

## D3 — Périmètre PHASE 2 / LOT 4
- créer `docs/governance/REPO_ROOT_POLICY.md`
- réaligner `docs/INDEX.md` et `docs/governance/REPO_ROLE.md`
- alignement minimal `DOC_LAYERS.md` (NEXT canonique = `docs/index/NEXT_GO_CANDIDATES.md`)

## D4 — Parent actif PHASE 2 (justification continuité)
- `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01` est assumé comme parent actif réel (PHASE 2 / LOT 4)
- cela justifie sa présence dans les index de continuité et contribue au passage de 6 à 8 GO non clos

## REPRISE
Point de reprise unique :
- `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/02_journal_technique.md`
