---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01_GAP_MATRIX
doc_type: gap_matrix
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01
status: open
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - doc_ops
  - continuity
  - gap_matrix
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01/00_cadrage.md
point_de_reprise: "Tableau de gap"
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/index/BRANCH_STATE.md
---

# 01_gap_matrix

| Surface | Etat lu | Ecart | Action proposee | A modifier ? |
| --- | --- | --- | --- | --- |
| `GO_INDEX.md` | Le parent `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` est bien `OPEN`, mais le sous-go `GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01` n'etait pas encore liste dans le tableau canonique ni dans les entrees. | La verite de liste ne refletait pas encore le chantier materialise. | Ajouter une ligne de sous-go sous le parent et une entree descriptive, sans changer la priorite operatoire globale des 14 GO non clos retenus. | oui |
| `NEXT_GO_CANDIDATES.md` | Le parent pointe deja vers le bon next GO primaire, mais le resume parlait encore de PR #161 et un bloc orphelin sur `GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01` restait en bas du fichier. | Le cadrage du next GO et le texte de reprise etaient stale par rapport a PR #166, PR #177 et PR #178. | Raffraichir le resume du parent et supprimer le bloc orphelin. | oui |
| `ACTIVE_STREAMS.md` | Le parent etait toujours en "prochaine action : closeout seed arbitration", alors que le seed closeout est deja publie et que `OPEN_WORK_CONTROL` est clos. | La prochaine action active du parent ne refletait pas le present GO de continuite. | Remplacer la prochaine action par l'execution du present GO et rappeler que `PRIMARY_RESTART` reste differe. | oui |
| `REPRISE.md` | La ligne du parent disait encore d'executer `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01`, puis `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`. La ligne seed pointait directement vers `GO_OPT_TRADING_DOC_OPS_CHILD_PRIMARY_RESTART_01`. | La matrice de reprise etait stale sur la chaine effective du parent. | Recaler le point de reprise sur le present GO et repousser `PRIMARY_RESTART` apres PASS du lot d'alignement. | oui |
| `BRANCH_STATE.md` | Snapshot branches au `2026-04-28` sur `origin/sot/mainline@9791516`, avec rappel explicite que la fiche est canonique pour la surface branches seulement. | Aucun ecart bloquant de surface branches n'a ete observe pour ce GO ; les mentions `OPEN_WORK_CONTROL` restantes relevent du journal de housekeeping, pas du point de reprise parent. | Laisser le fichier inchange ; documenter qu'il reste branche-only et hors gouvernance de continuite produit. | non |

## Conclusion

Le patch strictement necessaire porte sur `GO_INDEX.md`, `NEXT_GO_CANDIDATES.md`, `ACTIVE_STREAMS.md` et `REPRISE.md`. `BRANCH_STATE.md` reste lu, qualifie et conserve tel quel.
