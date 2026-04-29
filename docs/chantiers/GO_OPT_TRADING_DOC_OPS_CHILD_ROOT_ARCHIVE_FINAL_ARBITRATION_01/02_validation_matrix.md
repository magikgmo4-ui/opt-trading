---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_ROOT_ARCHIVE_FINAL_ARBITRATION_01_VALIDATION
doc_type: chantier_validation
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_ROOT_ARCHIVE_FINAL_ARBITRATION_01
status: open
lifecycle_stage: validation
topic_keys:
  - opt-trading
  - governance
  - root
  - archive
  - validation
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/REPO_ROOT_POLICY.md
point_de_reprise: "Tableau de validation"
updated_at: 2026-04-29
links:
  - docs/governance/REPO_ROOT_POLICY.md
  - docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/02_journal_technique.md
  - modules/simex_bitget_bridge/README.md
---

# 02_validation_matrix

## Tableau de validation

| GO | etat index | etat reel lu | artefact livre | gap restant | decision | justification |
| --- | --- | --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01` | `ACTIVE` | audit suffisant, matrice v1 produite, lots appliques documentes dans le journal et les decisions | oui | non | `CLOSE_NOW` | les reliquats root/archive sont soit deja traites, soit explicitement qualifies ; aucun move/delete/archive supplementaire n'est requis dans ce lot |
| `GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01` | `ACTIVE` | `REPO_ROOT_POLICY.md` stabilise la racine reelle, y compris metadata Git, bundles locaux ignores et shim `bitget_bridge.py` | oui | non | `CLOSE_NOW` | le dernier gap de politique racine est absorbe par une qualification explicite de compatibilite legacy, sans arbitrage ouvert residuel |

## Preuves synthetiques

### ROOT_POLICY_AND_RECLASS

- `README.md`, `.gitignore`, `.gitattributes`, `requirements.txt`, `.env.example`, `webhook_server.py` et `bitget_bridge.py` sont qualifies comme objets racine recevables
- `bitget_bridge.py` est un shim minimal vers `modules.simex_bitget_bridge.app.simex_bitget_bridge:main`
- aucun caller repo direct de `bitget_bridge.py` n'est prouve
- `modules/simex_bitget_bridge/README.md` conserve explicitement la disponibilite du shim
- les bundles locaux ignores a la racine sont qualifies comme artefacts de transit non canoniques

### OBSOLETE_RECLASS_ARCHIVE_AUDIT

- la matrice de qualification est publiee dans `02_journal_technique.md`
- les lots deja executes sont documentes :
  - retrait journal
  - reclassement root minimal
  - deplacement documentaire Bot Vision
  - reclassement workflow legacy
  - relocalisation `trae_pack_texts/`
- le reliquat de politique racine sur `bitget_bridge.py` est absorbe dans `REPO_ROOT_POLICY.md`
