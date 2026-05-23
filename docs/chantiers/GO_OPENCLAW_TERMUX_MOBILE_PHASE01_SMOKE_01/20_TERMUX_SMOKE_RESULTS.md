---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01_TERMUX_SMOKE_RESULTS
doc_type: termux_smoke_results
go_id: GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01
status: pending
updated_at: 2026-05-23
---

# 20_TERMUX_SMOKE_RESULTS

## Environnement de test

- **Système** : Android / Termux (AArch64)
- **Status** : EN ATTENTE (À valider sur un terminal physique)

## Résultats attendus

| Commande | Statut attendu | Note |
|---|---|---|
| `status` | PASS | Vérifie la présence de Python3 et Git dans Termux. |
| `list-jobs` | PASS | Liste les jobs autorisés. |
| `preflight` | PASS | Vérifie les permissions d'écriture dans le dossier de rapports Termux. |
| `run-dry` | PASS | Test `git status`. |

## Verdict Termux

```text
PENDING_PHYSICAL_VALIDATION
```
