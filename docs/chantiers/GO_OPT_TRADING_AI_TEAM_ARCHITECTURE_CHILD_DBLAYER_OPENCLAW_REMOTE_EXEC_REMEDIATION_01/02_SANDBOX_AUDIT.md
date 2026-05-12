---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01_SANDBOX_AUDIT
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

# 02_SANDBOX_AUDIT

## Gap documente

Source : `03_REMOTE_EXEC_STATE.md` — `sandbox.mode = all`, `sandboxed = true` empeche l'agent OpenClaw de joindre `192.168.0.191:22`.

## Etat constate

| Element | Valeur |
|:--------|:-------|
| mode sandbox | `all` |
| sandbox actif | `true` |
| SSH direct `db-layer -> fantome` | PASS (hors sandbox) |
| OpenClaw agent -> SSH fantome | FAIL (`Connection refused`) |
| cause probable | sandbox bloque l'acces network externe |

## Options

| Option | Description | Risque |
|:-------|:------------|:-------|
| A | Desactiver/assouplir sandbox pour le job cible | exposition reseau |
| B | Changer sandbox.mode pour permettre `22` outbound | configuration OpenClaw |
| C | Utiliser wrapper `openclaw -> sudo -> ghost -> ssh` hors sandbox | contourne la restriction |

## Decision

A arbitrer. L'option C est la plus sure car elle ne modifie pas la securite OpenClaw.
