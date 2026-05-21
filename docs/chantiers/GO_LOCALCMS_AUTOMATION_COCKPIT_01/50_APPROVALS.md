---
doc_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01_APPROVALS
doc_type: cockpit_page
go_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01
status: draft
---

# 50_APPROVALS.md

## Page: Approvals

URL: `/cockpit/automation/approvals`

### Propositions en attente

| ID | Action | Surface | Niveau | Soumis par | Il y a | Actions |
|---|---|---|---|---|---|---|
| P001 | WRITE_RECORDS | Airtable | L6 | specialist | 5 min | [APPROVE] [REJECT] [VIEW] |
| P002 | PATCH_CONFIG | repo | L5 | specialist | 12 min | [APPROVE] [REJECT] [VIEW] |

### Historique

| ID | Décision | Approver | Date |
|---|---|---|---|
| P000 | approved | human_01 | 2026-05-20 23:00 |
| P00A | rejected | team_ai_manager | 2026-05-20 22:30 |

### Boutons safe

| Bouton | Action | Confirmation |
|---|---|---|
| [APPROVE] | Approuve la proposition | Oui (modal) |
| [REJECT] | Rejette avec raison | Oui (modal + champ raison) |
| [VIEW] | Voir le packet complet | Non |
