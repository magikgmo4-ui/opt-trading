---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01_BOUNDARY_MATRIX
doc_type: chantier_boundary_matrix
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: opening
topic_keys:
  - why_lint
  - no_duplication
  - boundary
  - matrix
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/00_CONSOLIDATION_MAP_01.md
---

# 02_NO_DUPLICATION_BOUNDARY_MATRIX_01

## Objet

Matrice de non-duplication : definir pour chaque sujet quel axe est souverain et quels axes ne doivent pas redefinir le sujet.

## Matrice

| Sujet | Gouvernance | Runtime Security | WHY | WHY lint | OpenClaw central |
| --- | --- | --- | --- | --- | --- |
| **permissions** | Definit les regles de permission documentaire | Definit les permissions runtime L0-L8 | Represente les permissions dans le graphe | Detecte les contradictions de permissions | Applique les permissions en execution |
| **WHY** | Exige une section WHY dans tout GO | Exige un WHY pour toute action runtime | Represente le WHY comme graphe explicable | Detecte les gaps de WHY entre axes | Herite du WHY des axes de controle |
| **runtime** | Interdit le runtime non gouverne | Borne et securise le runtime | Represente le runtime dans le graphe | Detecte les gaps de securite runtime | Execute le runtime borne |
| **workers** | Definit la taxonomie documentaire des workers | Definit les permissions workers par surface | Represente les workers dans le graphe | Detecte les gaps worker/owner | Orchestre les workers |
| **Telegram** | Classe Telegram comme surface operateur | Definit les permissions Telegram runtime | Represente Telegram dans le graphe | Detecte les gaps de controle Telegram | Integre Telegram comme canal |
| **memory** | Definit la stratification documentaire de la memoire | Definit le scope de memoire accessible par agent | Represente la memoire dans le graphe | Detecte les gaps de scope memoire | Gerer la memoire operationnelle |
| **CI** | Definit les regles de CI documentaire | Definit les garde-fous CI runtime | Represente la CI dans le graphe | Detecte les gaps CI (sans bloquer) | Execute les pipelines CI autorises |
| **skill registry** | Definit la taxonomie et le nommage du registry | Definit les permissions par skill | Represente le registry dans le graphe | Detecte les gaps de skill registry | Consomme le registry pour l'orchestration |
| **observability** | Definit les exigences de tracabilite documentaire | Definit les logs d'audit runtime | Represente l'observabilite dans le graphe | Detecte les gaps d'observabilite | Emet les signaux d'observabilite |
| **branches** | Definit les regles de branche (MATRICE, GIT_BRANCH_HOUSEKEEPING) | N/A (branche = surface documentaire, pas runtime) | Represente les branches dans le graphe | Detecte les gaps de branche/chantier | N/A (Git gere par gouvernance) |
| **global indexes** | Gouverne GO_INDEX, ACTIVE_STREAMS, NEXT_GO, REPRISE, BRANCH_STATE | N/A (index = surface documentaire) | Represente les index dans le graphe | Detecte les contradictions d'index | N/A (index geres par gouvernance) |

## Regle de lecture

- **Souverain** = l'axe qui definit le sujet de maniere canonique.
- **Ne redefinit pas** = les autres axes peuvent referencer mais pas redefinir.
- **Detecte les contradictions** = role exclusif de WHY lint, toujours en warning-only.

## Invariants de non-duplication

1. Un seul axe est souverain par sujet.
2. Les autres axes referencent le souverain sans le redefinir.
3. WHY lint detecte les ecarts mais ne les corrige pas.
4. Aucun sujet n'est couvert par deux axes en mode souverain concurrent.
5. La gouvernance reste l'arbitre ultime en cas de conflit structurel.
