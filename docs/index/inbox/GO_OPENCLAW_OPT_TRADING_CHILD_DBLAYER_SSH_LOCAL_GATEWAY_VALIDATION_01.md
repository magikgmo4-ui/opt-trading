---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01_INBOX
doc_type: inbox
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01
status: open
lifecycle_stage: inbox
surface: index
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_REPORT_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/90_CLOSEOUT.md
---

# GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01

- statut : `OPEN`
- objet : valider `SSH` comme transport controle vers `db-layer`, puis verifier `OpenClaw` localement sur `db-layer`
- point cle : stop sur toute installation `openclaw` sur `fantome`
- controles attendus : identite machine, repo, `git status`, CLI `openclaw`, `Gateway V2`, orchestrateur, dry-run builder local
- stop condition : si CLI absent sur `db-layer`, produire `NEEDS_APPROVAL_INSTALL_DB_LAYER`, afficher la commande exacte retenue, puis stopper
