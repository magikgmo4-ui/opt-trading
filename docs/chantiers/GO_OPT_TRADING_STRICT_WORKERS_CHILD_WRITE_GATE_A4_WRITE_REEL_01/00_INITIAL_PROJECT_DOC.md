---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_WRITE_REEL_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_WRITE_REEL_01
parent_go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_01
machine: fantome
status: cadrage
lifecycle_stage: opening
topic_keys:
  - strict_workers
  - child
  - write_gate
  - A4
  - write_reel
  - rollback
source_kind: canonical
point_de_reprise: "Tester un write reel minimal avec rollback, approval humain obligatoire avant toute ecriture"
updated_at: 2026-05-14
---

# GO_OPT_TRADING_STRICT_WORKERS_CHILD_WRITE_GATE_A4_WRITE_REEL_01 — INITIAL PROJECT DOC

## 1_MASTER_TARGET

Tester le mode A4 (WRITE_GATED) avec un write reel minimal sur une surface non critique, puis rollback immediat.

## 2_PARENT_HERITAGE

| Heritage | Source |
|----------|--------|
| A4 policy gate | `WRITE_GATE_A4_01` (PASS, merge #370) |
| 8 regles de refus | `A4_WRITE_GATE_POLICY.md` |
| Allowlist | `reports/ai/workers/*`, `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_**/*` |

## 3_CADRE_ULTRABORNE

```text
Surface cible: reports/ai/workers/GO_STRICT_WORKERS_A4_WRITE_REEL_TEST.md
Operation: CREATE_FILE (fichier de test non critique)
Contenu: 5 lignes de texte de test
Rollback: rm du fichier cree
Condition critique: STOP AVANT TOUT WRITE REEL → DEMANDER APPROVAL EXPLICITE
```

## 4_PHASES

### A. Cadrage (ce document)
### B. Dry-run (job packet + rapport dry-run)
### C. Demande approval → ARRET → ATTENDRE
### D. Si approuve: write reel
### E. Verification (git status, existence fichier)
### F. Rollback (suppression du fichier)
### G. Closeout

## 5_CONDITION_ARRET

```text
ARRET OBLIGATOIRE APRES PHASE B (dry-run).
NE PAS EXECUTER LE WRITE REEL SANS APPROBATION EXPLICITE.
Message attendu: "APPROVED: execute write reel phase D"
```

## 6_CRITERES_PASS

```text
PASS si :
- Dry-run produit un diff conforme
- Write reel cree le fichier attendu
- Contenu correspond au dry-run
- Rollback nettoie le fichier
- Git status propre apres rollback
- Aucun effet de bord
```

## 7_INVARIANTS

```text
- A4 policy gate actif (R1-R8)
- explicit_write_approval obligatoire
- dry_run obligatoire avant write reel
- allowlist respectee
- Aucun secret
- Stash branch_arbitration preserve
```
