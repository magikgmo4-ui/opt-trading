# GO_PROMPT — TESTS ULTRA CONCRETS REPO KG

GO_ID:
GO_OPT_TRADING_REPO_KG_TESTS_ULTRA_CONCRETS_01

OBJECTIF:
Valider que le système Repo Knowledge Graph (schema + producer spec + views) est cohérent avec la réalité du repo opt-trading.

MISSION_CLASS:
AUDIT_REALIGNEMENT

CONTRAINTES:
- Repo = source de vérité
- Aucun code runtime modifié
- Lecture seule
- Preuve minimale obligatoire pour chaque test

ETAPES:

ETAPE_01 — VALIDATION GO_INDEX
- INPUT: docs/index/GO_INDEX.md
- OUTPUT: liste GO réels
- PREUVE: extraction réelle

ETAPE_02 — VALIDATION DOCS
- INPUT: docs/chantiers/
- OUTPUT: mapping GO → docs
- PREUVE: chemins existants

ETAPE_03 — VALIDATION MODULES
- INPUT: modules/
- OUTPUT: liste modules + scripts
- PREUVE: présence cmd.sh/menu.sh/sanity

ETAPE_04 — VALIDATION BRANCHES
- INPUT: git branch -a
- OUTPUT: branches réelles
- PREUVE: output git

ETAPE_05 — VALIDATION SCHEMA
- INPUT: graph_schema_v1.md
- OUTPUT: correspondance réelle repo
- PREUVE: mismatch list

SORTIE ATTENDUE:
- REPORT.md
- GAP_REPORT.md
- STATUS: PASS / PARTIAL / FAIL
