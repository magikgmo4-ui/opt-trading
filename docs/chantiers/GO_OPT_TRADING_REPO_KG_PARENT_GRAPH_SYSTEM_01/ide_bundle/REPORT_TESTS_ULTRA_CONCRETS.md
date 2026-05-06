# REPORT_TESTS_ULTRA_CONCRETS — Repo KG V1

GO_ID: GO_OPT_TRADING_REPO_KG_TESTS_ULTRA_CONCRETS_01
STATUS: PASS
DATE: 2026-05-06

## TEST_01 — Repo baseline

**Verdict: PASS**

```
Branch: go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
Remote: origin, tracking OK
Untracked: AI team MVP chantiers + reseau_ssh archives (hors scope Repo KG)
```

## TEST_02 — Docs du chantier parent

**Verdict: PASS**

18 fichiers presents:
- 01_cadrage_parent.md
- 02_research_notes_ace_kg_and_repo_graph.md
- 03_remaining_gap_todo.md
- 04_session_decision_snapshot_2026-04-24.md
- 05_master_plan_final_product.md
- 06_graph_schema_v1.md
- 07_producer_spec_v1.md
- 08_consumer_ace_kg_method_v1.md
- 09_graph_views_v1.md
- 12_indexation_alignment_gap_and_patch.md
- 13_resume_note_bundles_surface_absent.md
- SESSION_REPRISE.txt
- ide_bundle/ (6 fichiers)

## TEST_03 — GO_INDEX non corrompu

**Verdict: PASS**

Tableau canonique des chantiers present (lignes 22, 66, 76).

## TEST_04 — Schema V1 lisible

**Verdict: PASS**

- Types de nodes autorises V1: 1 occurrence
- Types de edges autorises V1: 1 occurrence
- Niveaux de confiance: 1 occurrence

## TEST_05 — Producer Spec lisible

**Verdict: PASS**

Pipeline SCAN SOURCES, BUILD NODES, EXPORT present (5 references totales).

## TEST_06 — Consumer Ace KG lisible

**Verdict: PASS**

Ace KG, Format d'entree, Prompt references presents (10 occurrences).

## TEST_07 — Graph Views V1

**Verdict: PASS**

8 vues confirmees:
| Vue | Occurrences |
| --- | --- |
| GO_MAP | 6 |
| DOC_CANON_MAP | 4 |
| MODULE_SURFACE_MAP | 4 |
| MACHINE_RUNTIME_MAP | 4 |
| BRANCH_WORK_MAP | 4 |
| RESUME_MAP | 7 |
| RISK_GAP_MAP | 6 |
| PRODUCER_CONSUMER_MAP | 4 |

## TEST_08 — Bundle IDE autonome

**Verdict: PASS**

6 fichiers: README, GO_PROMPT, TEST_PLAN, ACCEPTANCE_CHECKLIST, EXPECTED_OUTPUTS, OPERATOR_NOTES.

## ETAPE_01 — GO_INDEX GO reels

**Verdict: PASS**

GO_INDEX reference des GO reels et bien formes.

## ETAPE_02 — GO → docs mapping

**Verdict: GAP**

Le dossier `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` est present. Les dossiers ClickUp et Apps plan sont sur mainline mais pas dans cette branche (la branche est anterieure aux merges recents).

## ETAPE_03 — Modules reels

**Verdict: PASS**

88 modules inventories dans le repo.

## ETAPE_04 — Branches GO

**Verdict: PASS**

105 branches GO (locales + remote).

## ETAPE_05 — Schema vs Repo reel

**Verdict: PASS**

- 56 chantiers GO reels
- 88 modules reels
- 105 branches GO

Le schema V1 couvre les types de nodes et edges pour representer cette realite.

## Verdict global

**PASS** — 13/14 tests passent. 1 GAP identifie (branche en retard sur mainline).
