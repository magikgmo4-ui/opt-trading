---
doc_id: GO_OPT_TRADING_CURSOR_AI_OPERATOR_BRANCH_CLEANUP_01_30_MANIFEST_CORRECTION
doc_type: chantier/manifest_correction
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/operator-export/EXPORT_MANIFEST.json
---

# 30_MANIFEST_CORRECTION

## Incoherence corrigee

`bundles/operator-export/EXPORT_MANIFEST.json` referencait PR #212 pour operator-export et position C. Le vrai PR est #213.

## Corrections appliquees

| Ligne | Avant | Apres |
| --- | --- | --- |
| `bundles[1].pr` | `#212` | `#213` |
| `go_sequence[7].pr` | `#212` | `#213` |

## Ajout position D

| Position | GO | PR |
| --- | --- | --- |
| D | `GO_OPT_TRADING_CURSOR_AI_OPERATOR_BRANCH_CLEANUP_01` | #214 |

## Verification

```powershell
$manifest = Get-Content "bundles/operator-export/EXPORT_MANIFEST.json" -Raw | ConvertFrom-Json
# Verifier PR operator-export
if ($manifest.bundles[1].pr -eq "#213") { "PASS: bundle pr=#213" }
# Verifier PR position C
if ($manifest.go_sequence[7].pr -eq "#213") { "PASS: position C pr=#213" }
# Verifier position D ajoutee
if ($manifest.go_sequence[8].position -eq "D") { "PASS: position D added" }
```

## RISKS

- À qualifier.
