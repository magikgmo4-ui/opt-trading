---
doc_id: INBOX_GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
doc_type: index_inbox_entry
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
status: draft
lifecycle_stage: opening
surface: docs/index/inbox
source_kind: canonical_local_inbox
updated_at: 2026-05-09
topic_keys:
  - openclaw
  - runtime_security
  - parent
  - why
  - inbox
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01

## Objet

Entree courte d'indexation locale pour le parent OpenClaw runtime security.

## Etat

- Statut : `OPENING_DRAFT`
- Branche : `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01`
- Scope : documentation uniquement
- Runtime : non modifie
- Index globaux : non modifies

## FINAL_TARGET

Produire une specification canonique de securite runtime OpenClaw pour `opt-trading`, couvrant les permissions, chemins, actions dangereuses, audit logs, separation agent / worker / machine, modele de confiance, anti prompt-injection, anti auto-fix destructif et integration future avec un skill registry.

## WHY

Eviter qu'OpenClaw devienne un orchestrateur puissant sans garde-fous. Les actions IA doivent rester explicables, tracables, bornees, reversibles quand possible et non destructives par defaut.

## Fichier principal

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
```

## Point de reprise

Reprendre dans la spec parent, section `17_RESUME_POINT`.

Suite logique forte proposee :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01
```
