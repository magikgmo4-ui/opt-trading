---
doc_id: GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01_EVIDENCE
doc_type: evidence
go_id: GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01
status: passed_with_evidence
---

# 99_EVIDENCE

## Preuve concrète de validation

### 1. Template du contrat
- `10_CONTRACT_TEMPLATE.md` — 12 champs (app_id, purpose, source_of_truth_rank, allowed_reads, allowed_writes, forbidden_actions, required_env_vars, dry_run_mode, approval_gate, audit_log, rollback, evidence_ref)

### 2. 10 contrats remplis
- `20_BRIDGE_CONTRACTS.md` — Tous les champs requis présents pour les 10 apps :
  - Airtable, ClickUp, Botpress, Google Sheets, Telegram, Gmail, Calendar, Drive, Figma, LocalCMS
  - Chaque contrat a `forbidden_actions` non vide (3+ actions interdites par contrat)
  - Chaque contrat a `evidence_ref` pointant vers sa source

### 3. Validation des actions interdites (10/10 PASS)

```bash
$ python3 scripts/ai/tests/g04_validate_contracts.py
Valid: 10/10
[✓ PASS] airtable     → M21
[✓ PASS] clickup      → M22
[✓ PASS] botpress     → M23
[✓ PASS] google_sheets → M24
[✓ PASS] telegram     → M25
[✓ PASS] gmail        → M26
[✓ PASS] google_calendar → M27
[✓ PASS] google_drive → M28
[✓ PASS] figma        → M29
[✓ PASS] localcms     → M30
```

### 4. Lien vers la capability matrix (G01)
Chaque contrat est lié à sa ligne dans la matrice G01 :
- M21-M30 correspondent aux 10 app_bridge contracts
- Les permissions (`write_gated`, `read`) et gates (`human_approve`, `dry_run`, `none`) sont cohérentes
- Scénario S3 de G01 valide le cas `write_gated` avec `human_approve` pour les app_bridge

### 5. Script de validation
- `scripts/ai/tests/g04_validate_contracts.py` — vérifie automatiquement tous les champs requis, les actions interdites, et le mapping matrix

## Conclusion

Tous les critères de succès sont remplis (10 contrats signés, actions interdites listées, lien vers capability matrix). Statut : PASS_WITH_EVIDENCE.
