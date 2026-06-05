---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01_20_PROCEDURE
doc_type: chantier/test_procedure
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01
machine: cursor-ai
status: active
lifecycle_stage: real_usage_test
links:
  - bundles/claude-artifacts/README.md
  - bundles/claude-artifacts/PROMPT_TEMPLATES.md
  - bundles/claude-artifacts/REPRISE_TEMPLATE.md
  - bundles/claude-artifacts/NO_COMMIT_RULES.md
  - bundles/claude-artifacts/CHECKLIST_EXECUTION.md
  - bundles/claude-artifacts/bundle_meta/manifest.json
---

# 20_REAL_USAGE_PROCEDURE — Procedure de test d'usage reel operateur

## Contexte

Ce test simule l'arrivee d'un nouvel operateur cursor-ai qui suit le handoff de `bundles/operator-export/HANDOFF.md` et utilise le pack Claude artifacts pour ses operations.

## Etape 1 — Reprise operateur (HANDOFF)

> Simulation : l'operateur lit `bundles/operator-export/HANDOFF.md` et execute les commandes de demarrage.

```bash
git fetch origin --prune
git checkout sot/mainline
git pull --rebase origin sot/mainline
git log --oneline -5
```

**Resultat** : OK — `sot/mainline` est a jour, les commandes sont executables.

## Etape 2 — Lecture de l'ordre de lecture (HANDOFF)

> L'operateur suit l'ordre de lecture prioritaire decrit dans HANDOFF.md.

| Ordre | Document | Accessible | Lisible | Complet |
| --- | --- | --- | --- | --- |
| 1 | `bundles/operator-export/README.md` | OUI | OUI | OUI |
| 2 | `bundles/operator-export/EXPORT_MANIFEST.json` | OUI | OUI — JSON valide | OUI |
| 3 | `bundles/CURSOR_AI_OPERATOR_REPRISE_PACKET.md` | OUI | OUI | OUI |
| 4 | `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` | OUI | OUI | OUI |
| 5 | `bundles/claude-artifacts/README.md` | OUI | OUI | OUI |

**Resultat** : OK — tous les documents de l'ordre de lecture sont accessibles et lisibles.

## Etape 3 — Utilisation du pack Claude artifacts (actions standard)

> L'operateur suit les actions standard du HANDOFF pour utiliser le pack.

### 3.1 — Creation d'un GO (Template 1 — Prompt de reprise)

> L'operateur lit `bundles/claude-artifacts/PROMPT_TEMPLATES.md` > Template 1.

- **Template present** : OUI
- **Structure du template** : ROLE, REPO, ETAT VALIDE, OBJECTIF, A NE PAS FAIRE, ETAPES, VERDICT PASS SI
- **Completude** : OUI — 7 sections avec commandes Git explicites
- **Invariants couverts** : no admin-trading, no runtime, no secrets, alert_webhook preserve, Bundles produit preserve
- **Utilisabilite** : Template directement copiable et parametrable avec `<GO_ID>`, `<inserer ...>` pour customisation

**Verdict** : PASS

### 3.2 — Merge d'un GO (Template 3 — Prompt de merge doc-only)

> L'operateur lit `bundles/claude-artifacts/PROMPT_TEMPLATES.md` > Template 3.

- **Template present** : OUI
- **Etapes** : gh pr create → verifier diff → gh pr merge → sync local
- **Completude** : OUI — cycle merge complet
- **Precautions** : verification doc-only avant merge

**Verdict** : PASS

### 3.3 — Verification securite (CHECKLIST_EXECUTION.md)

> L'operateur execute la checklist de verification rapide.

Verifications pre-commit executees :

```
=== Pre-commit checks ===
Branch: go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01
Non-doc files: (none)
Secrets: (none)
```

- **Commandes executables** : OUI (scripts bash fonctionnels)
- **Sections couvertes** : pre-commit, pre-push, pre-PR, post-merge
- **Liste de verification rapide** : 5 verifications pre-commit, 3 pre-push, 5 pre-PR, 4 post-merge

**Verdict** : PASS

## Etape 4 — Utilisation du template de reprise (REPRISE_TEMPLATE.md)

> L'operateur lit `bundles/claude-artifacts/REPRISE_TEMPLATE.md`.

- **Template present** : OUI
- **Structure** : 7_CANONICAL_STATE, 13_ESTABLISHED, 14_HYPOTHESIS, 15_REMAINING_GAP, 16_TODO, 17_RESUME_POINT
- **Completude** : OUI — toutes les sections de reprise standard
- **Utilisabilite** : Sections avec `<inserer>` pour customisation, commandes de reprise bash

**Verdict** : PASS

## Etape 5 — Verification des regles de non-commit (NO_COMMIT_RULES.md)

> L'operateur lit `bundles/claude-artifacts/NO_COMMIT_RULES.md`.

- **Interdictions couvertes** : secrets, .env, tokens, outputs live, captures sensibles, payloads reels, chemins locaux prives (7 categories)
- **Chemins acceptables** : anonymises, relatifs, variables (3 patterns)
- **Commandes de verification** : `grep` sur diff avecge pour secrets et chemins prives
- **Sanctions documentees** : revert, token rotation, documentation incident

**Verdict** : PASS — couverture complete des regles de securite

## Etape 6 — Verification du manifest technique

> L'operateur verifie le manifest du bundle : `bundles/claude-artifacts/bundle_meta/manifest.json`.

- **Schema** : `opt_trading_bundle_manifest_v1` — identifie
- **bundle_id** : `BUNDLE_CLAUDE_ARTIFACTS_OPERATOR_PACK_01` — coherent avec le README
- **bundle_type** : `operator_pack` — coherent
- **machine** : `cursor-ai` — correct
- **fichiers declares (6)** : tous existent, roles definis
- **dependances (4)** : toutes resolues
- **invariants** : doc_only, no_runtime, no_secrets, no_admin_trading, machine cursor-ai — coherents

**Verdict** : PASS

## Etape 7 — Test du flow handoff complet

> Simulation : un operateur reprend l'etat cursor-ai via le handoff, utilise le pack, et reproduit un cycle standard.

| Cycle | Action | Faisable |
| --- | --- | --- |
| Demarrage | Lire `operator-export/README.md` puis `HANDOFF.md` | OUI |
| Relire etat | Lire `EXPORT_MANIFEST.json` + `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` bloc CURSOR_AI | OUI |
| Pack | Lire `claude-artifacts/README.md` | OUI |
| Template | Utiliser `PROMPT_TEMPLATES.md` Template 1 pour creer un GO | OUI |
| Checklist | Suivre `CHECKLIST_EXECUTION.md` avant commit/push | OUI |
| Securite | Verifier `NO_COMMIT_RULES.md` | OUI |
| Reprise | Produire une fiche avec `REPRISE_TEMPLATE.md` | OUI |
| Handoff | Produire un handoff IDE (Template 5) | OUI |
| Merge | Utiliser Template 3 pour merger | OUI |
| Safety | Utiliser Template 4 pour safety check | OUI |

**Resultat** : OK — le flow complet est executable par un operateur cursor-ai.

## Resume de la procedure

**Tous les artefacts du pack Claude artifacts sont utilisables en conditions reelles par un operateur cursor-ai.** Aucun blocage, aucune dependance manquante, aucune etape inexecutable.

## RISKS

- À qualifier.
