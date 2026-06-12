# GO_SECURITY_CREDENTIAL_HARDENING_SCAN_01

## Objectif

Scan initial de hardening credentials — history git, permissions fleet, least privilege.

## Périmètre

- Scan gitleaks 3102 commits (history + working tree)
- Audit permissions  et  sur 5 machines
- Least privilege : comparaison `machines.yaml` vs fichiers role déployés

## Résultats

| Check | Statut |
|-------|--------|
| History scan (3102 commits) | PASS — 0 vrai leak |
| Static grep fichiers trackés | PASS |
| Permissions fleet post-fix | PASS — .env 600, roles/ 700 |
| Least privilege | PASS — 0 excess, machines.yaml aligné |

## Faux positifs documentés

- `pro_desk_data_inventory.json:404` — generic-api-key FP (code SEC 13f_holdings)
- `GO_MASTER.md:30` — private-key FP (template placeholder)
- `FIXTURE_CORPUS_01.md:1166` — private-key FP (lint test fixture)

## Corrections appliquées

- permissions fleet : 664/644/660 → 600, roles dir 755 → 700
- machines.yaml : db-layer + student eligible_roles mis à jour
- fantome : stale .bak supprimé
