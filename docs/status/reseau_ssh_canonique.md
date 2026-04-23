---
doc_id: OPT_TRADING_STATUS_RESEAU_SSH_CANONIQUE
doc_type: family_status
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id:
status: reference
lifecycle_stage: continuity
topic_keys:
  - opt-trading
  - status
  - reseau_ssh
  - family
surface: continuity
source_kind: derived
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# RESEAU_SSH — STATUT CANONIQUE

## Role aligne avec la matrice maitre

- role actuel : fiche courte de lignee `reseau_ssh*`
- role cible : surface derivee de qualification famille
- cette fiche ne remplace ni la matrice maitre, ni la doctrine Git, ni l'arbitrage final de reclassement physique

## Objet
Fiche courte de lignée pour la famille `reseau_ssh*`, en complément de l’audit famille.

## ETABLI
- famille step-by-step confirmée (`reseau_ssh`, `reseau_ssh_step1b`, `reseau_ssh_step2`)
- cible canonique déjà retenue dans la continuité : `reseau_ssh_step2`
- runtime alignment clos sur `admin-trading`, `student`, `db-layer` : les entrypoints courts convergent vers `scripts/reseau_ssh/`
- LAN actif observé depuis `cursor-ai` : `192.168.0.0/24`
- ancien LAN `192.168.16.0/24` : historique / ancien routeur, à ne plus lire comme LAN actif par défaut

## Inventaire LAN actif
| Machine | LAN actif | WG |
|---|---:|---:|
| admin-trading | 192.168.0.111 | 10.66.66.1 |
| student | 192.168.0.142 | 10.66.66.3 |
| db-layer | 192.168.0.100 | 10.66.66.2 |
| cursor-ai | 192.168.0.177 | 10.66.66.4 |

## Survivant / Transition / Legacy / Archive
- survivant : `reseau_ssh_step2`
- transition : `reseau_ssh_step1b` (prérequis intermédiaire)
- legacy : `reseau_ssh` (selon arbitrage final de consolidation)
- archive : non figé dans ce lot

## Liens de preuve
- `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`
- `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md`

## Reprise
- reprendre dans `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` pour arbitrage final de reclassement physique
