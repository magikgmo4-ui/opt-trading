---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01_SSH_ALIAS_AUDIT
doc_type: audit
repo: opt-trading
project: opt-trading
module: ai_team_mvp
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01
parent_go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
status: draft_for_review
lifecycle_stage: audit
surface: chantier
source_kind: canonical_draft
updated_at: 2026-05-09
point_de_reprise: "Section Decision"
---

# 03_SSH_ALIAS_AUDIT

## Gap documente

Source : `03_REMOTE_EXEC_STATE.md` — alias `fantome` absent du `~/.ssh/config` sur `db-layer`.

## Etat constate

| Element | Valeur |
|:--------|:-------|
| alias `fantome` dans `~/.ssh/config` | ABSENT |
| IP documentee | `192.168.0.191` |
| alias presents | `admin-trading`, `db-layer`, `student`, `cursor-ai` |
| host key | pinning TOFU temporaire dans `/tmp/fantome_phase5_known_hosts` |
| fingerprint ED25519 | `SHA256:qPww4rm00lbiaTIS8XixarBxEZznfjc4kMi19zmGZlA` |

## Options

| Option | Description | Risque |
|:-------|:------------|:-------|
| A | Ajouter alias `fantome` canonique dans `~/.ssh/config` avec IP et host key | Changement config SSH |
| B | Utiliser IP directe documentee sans alias | Pas d'alias pour les autres outils |
| C | Recopier alias depuis `reseau_ssh` docs si present | Depend de la source documentaire |

## Decision

A arbitrer. L'option A est recommandee : restaurer ou creer l'alias `fantome` avec host key permanente.

## RISKS

- À qualifier.
