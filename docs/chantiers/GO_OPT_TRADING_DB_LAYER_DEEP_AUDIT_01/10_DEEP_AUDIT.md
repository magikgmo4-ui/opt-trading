---
doc_id: DB_LAYER_DEEP_AUDIT_01_TABLE
doc_type: audit_table
repo: opt-trading
go_id: GO_OPT_TRADING_DB_LAYER_DEEP_AUDIT_01
status: active
surface: chantier
source_kind: derived
updated_at: 2026-05-14
---

# 10_DEEP_AUDIT - Preuves et decision

| Branche | Ancien statut | Etat Git reel | Preuves trouvees | Nouvelle classification | Justification |
| --- | --- | --- | --- | --- | --- |
| `go/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01` | `A_VERIFIER` | remote, `DIVERGED`, `ahead 1`, `behind 814`, `merged:no`, `7 files` | `git show` du remote `90_CLOSEOUT.md` : verdict `PASS`, inbox dediee, `NEXT_GO -> GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01` | `KEEP_REFERENCE` | chantier doc-only materialise sur la branche, closeout distant present et clos ; branche a conserver comme trace de review |
| `go/GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01` | `A_VERIFIER` | remote, `DIVERGED`, `ahead 1`, `behind 814`, `merged:no`, `7 files` | `git show` du remote `90_CLOSEOUT.md` : verdict `PASS`, inbox dediee, `NEXT_GO -> GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_CLOSEOUT_01` | `KEEP_REFERENCE` | chantier doc-only clos, sans runtime modifie, conserve comme trace de realignement |
| `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01` | `A_VERIFIER` | remote, `DIVERGED`, `ahead 1`, `behind 926`, `merged:no`, `1 file` | `git show` du remote `00_cadrage_parent.md` : `status: open`, plan parent complet, TODO restants, point de reprise explicite | `KEEP_ACTIVE` | parent documentaire encore ouvert, avec cadrage actif et suite de travail explicite |

## Resultat

- vers `KEEP_REFERENCE` : 2
- vers `KEEP_ACTIVE` : 1
- `DROP_MERGED` : 0
- `A_VERIFIER` restant : 0

## Notes de preuve

- Les preuves manquantes n'etaient pas visibles sur la ligne locale, mais bien presentes sur les branches distantes.
- Le deep audit confirme qu'il fallait lire directement le contenu distant avant tout verdict final.

## RISKS

- À qualifier.
