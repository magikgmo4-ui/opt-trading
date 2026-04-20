# GO_GIT_KEEP_REFERENCE_CANON_CLOSEOUT_01 — décisions

## Décisions

| branche | ancrage canonique | verdict | justification |
| --- | --- | --- | --- |
| `doc/GO_OPENCLAW_INFRA_BASELINE_01` | `modules/menu_openclaw/docs/GO_OPENCLAW_INFRA_BASELINE_01.md` | `DROP_REMOTE_CANDIDATE` | le document est déjà présent dans le canon courant; l'écart constaté avec la branche de référence est résiduel |
| `feat/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01` | `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`, `docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md`, `docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md`, `docs/governance/AUDIT_IA_ASSISTANTS_WORKFLOW_ROLE_ALIGNMENT_OPT_TRADING.md` | `DROP_REMOTE_CANDIDATE` | la valeur documentaire utile est maintenant ancrée dans le canon; le reste du diff correspond a des versions deja absorbees ou depassees dans `sot/mainline` |
| `integ/trading-dual-stack-doc-pack-01` | `docs/trading/02_ETABLI_TRADING_DUAL_STACK_V1_0.txt`, `docs/trading/03_KANBAN_TRADING_DUAL_STACK_V1_0.txt`, `docs/trading/04_REPRISE_TRADING_DUAL_STACK_V1_0.txt`, `docs/trading/TRADING_DUAL_STACK_V1_0_CLARIFIED.md` | `DROP_REMOTE_CANDIDATE` | les quatre fichiers du pack sont deja identiques dans le canon courant |

## Note

- ce GO ne supprime aucune branche
- tout delete local ou remote doit etre traite dans un passage Git distinct et valide
