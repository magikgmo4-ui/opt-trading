---
doc_id: GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_MANUAL_UI_COMPLETION_01_10_MANUAL_STEPS
doc_type: chantier/manual_steps
repo: opt-trading
branch: go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_MANUAL_UI_COMPLETION_01
go_id: GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_MANUAL_UI_COMPLETION_01
machine: fantome
status: open
lifecycle_stage: manual_ui_completion
links:
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/CLICKUP_IMPLEMENTATION_BUNDLE_V1/01_SCHEMA.txt
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/CLICKUP_IMPLEMENTATION_BUNDLE_V1/02_TEMPLATE.txt
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/CLICKUP_IMPLEMENTATION_BUNDLE_V1/05_DASHBOARD.txt
---

# 10_MANUAL_STEPS — Completion manuelle ClickUp UI

## Espaces concernes

Les etapes ci-dessous doivent etre appliquees au Space principal:

- **CANON_GOVERNANCE** (Space ID: `90145495925`)
  - URL: https://app.clickup.com/90141225112/v/s/90145495925

Les autres Spaces (MODULES, MACHINES, TRADING_OPS) pourront etre configures ulterieurement selon le meme schema.

---

## Etape 1 — Activer ClickApp Custom Fields

1. Aller dans CANON_GOVERNANCE: https://app.clickup.com/90141225112/v/s/90145495925
2. Cliquer sur l'avatar/bouton Space settings (⚙️)
3. Dans le menu, trouver **ClickApps**
4. Activer **Custom Fields** (basculer le switch sur ON)
5. Verifier que le toggle est vert/actif

---

## Etape 2 — Creer les 15 champs personnalises

Dans le Space CANON_GOVERNANCE, pour chaque champ ci-dessous:

1. Aller dans Space settings → Custom Fields
2. Cliquer **+ New Custom Field**
3. Creer selon le tableau ci-dessous

### Champs de type Texte court

| Ordre | Nom | Type |
| --- | --- | --- |
| 1 | GO_ID | Text (Short) |
| 2 | GO_TYPE | Dropdown |
| 3 | PARENT_GO | Text (Short) |
| 4 | MODULE | Text (Short) |
| 5 | SURFACE | Text (Short) |
| 6 | MACHINE_OWNER | Text (Short) |
| 7 | BRANCH | Text (Short) |
| 8 | BASE_BRANCH | Text (Short) |
| 9 | DOC_PATH | Text (Short) |
| 10 | PR_URL | Text (Short) |
| 11 | COMMIT_SHA | Text (Short) |
| 12 | VALIDATION_STATUS | Dropdown |
| 13 | NEXT_GO | Text (Short) |
| 14 | RESUME_POINT | Text (Short) |
| 15 | CANON_PROOF_STATUS | Dropdown |

### Options pour GO_TYPE (Dropdown)

- PARENT
- CHILD
- SIMPLE
- DOC_ONLY
- PATCH
- AUDIT
- EXECUTION

### Options pour VALIDATION_STATUS (Dropdown)

- NONE
- PARTIAL
- PASS
- FAIL

### Options pour CANON_PROOF_STATUS (Dropdown)

- MISSING
- DOC_PRESENT
- BRANCH_PRESENT
- COMMIT_PRESENT
- PR_PRESENT
- CLOSEOUT_PRESENT

---

## Etape 3 — Creer les 10 statuses personnalises

Dans le Space CANON_GOVERNANCE:

1. Aller dans Space settings
2. Trouver **Statuses** (ou **Task Statuses**)
3. Creer les statuses suivants dans l'ordre:

| Ordre | Nom | Type | Couleur suggeree |
| --- | --- | --- | --- |
| 1 | BACKLOG | open | gris |
| 2 | CADRAGE | open | bleu clair |
| 3 | READY | open | vert clair |
| 4 | IN_PROGRESS | in progress | orange |
| 5 | BLOCKED | in progress | rouge |
| 6 | REVIEW | in progress | violet |
| 7 | PASS | closed | vert fonce |
| 8 | FAIL | closed | rouge fonce |
| 9 | CLOSED | closed | gris fonce |
| 10 | ARCHIVED | closed | noir |

---

## Etape 4 — Remplir les custom fields sur les 2 taches

### Tache 1: GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01
URL: https://app.clickup.com/t/86b9tqe3y

| Champ | Valeur |
| --- | --- |
| GO_ID | GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01 |
| GO_TYPE | PARENT |
| MODULE | gouvernance |
| MACHINE_OWNER | admin-trading |
| BRANCH | go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01 |
| BASE_BRANCH | sot/mainline |
| DOC_PATH | docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01 |
| VALIDATION_STATUS | PASS |
| CANON_PROOF_STATUS | PR_PRESENT |
| NEXT_GO | GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_MANUAL_UI_COMPLETION_01 |
| RESUME_POINT | docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/CLICKUP_IMPLEMENTATION_BUNDLE_V1/ |

Statut a mettre: **PASS**

### Tache 2: GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01
URL: https://app.clickup.com/t/86b9tqe46

| Champ | Valeur |
| --- | --- |
| GO_ID | GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01 |
| GO_TYPE | EXECUTION |
| PARENT_GO | GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01 |
| MODULE | gouvernance |
| MACHINE_OWNER | fantome |
| BRANCH | go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01 |
| BASE_BRANCH | sot/mainline |
| DOC_PATH | docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01 |
| VALIDATION_STATUS | PASS |
| CANON_PROOF_STATUS | PR_PRESENT |
| NEXT_GO | GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_MANUAL_UI_COMPLETION_01 |
| RESUME_POINT | docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/ |

Statut a mettre: **PASS**

---

## Etape 5 — Creer les Dashboards

Dans le workspace Ghost's Workspace: https://app.clickup.com/90141225112

1. Aller dans le menu lateral → **Dashboards**
2. Cliquer **+ New Dashboard**
3. Creer les 5 dashboards suivants:

| Dashboard | Widget principal | Espace(s) |
| --- | --- | --- |
| GO actifs | Task List (filtre: status != CLOSED, ARCHIVED) | CANON_GOVERNANCE |
| GO bloques | Task List (filtre: status = BLOCKED) | CANON_GOVERNANCE |
| GO sans preuve | Task List (filtre: CANON_PROOF_STATUS = MISSING) | CANON_GOVERNANCE |
| GO par machine | Task List (groupe par: MACHINE_OWNER) | Tous |
| NEXT_GO | Task List (tri par: NEXT_GO) | CANON_GOVERNANCE |

---

## Etape 6 — Creer le template GO_TASK_TEMPLATE

Dans le Space CANON_GOVERNANCE:

1. Aller dans la list **GO_ACTIVE**
2. Trouver l'option **Templates** (ou dans Space settings)
3. Cliquer **+ New Template**
4. Nom: `GO_TASK_TEMPLATE`
5. Description par defaut:

```
GO_ID: [a remplir]
GO_TYPE: [PARENT|CHILD|SIMPLE|DOC_ONLY|PATCH|AUDIT|EXECUTION]
PARENT_GO: [si applicable]
MODULE: [obligatoire si module impacte]
MACHINE_OWNER: [machine responsable]
BRANCH: go/<GO_ID>
BASE_BRANCH: sot/mainline
DOC_PATH: docs/chantiers/<GO_ID>/
VALIDATION_STATUS: NONE
NEXT_GO: [obligatoire]
RESUME_POINT: [obligatoire]
CANON_PROOF_STATUS: MISSING
```

6. Pre-remplir les custom fields avec les valeurs par defaut ci-dessus
7. Sauvegarder

---

## Etape 7 — Verification cockpit utilisable

Checklist finale:

- [ ] Espaces CANON_GOVERNANCE, MODULES, MACHINES, TRADING_OPS visibles
- [ ] Custom Fields actifs et remplis sur les 2 taches
- [ ] Statuses personnalises disponibles
- [ ] Task 86b9tqe3y en statut PASS avec champs remplis
- [ ] Task 86b9tqe46 en statut PASS avec champs remplis
- [ ] Dashboard GO actifs affiche les 2 taches
- [ ] Template GO_TASK_TEMPLATE disponible pour nouvelles taches
- [ ] Navigation fluide entre Spaces

## Apres completion

Mettre a jour le closeout (90_CLOSEOUT.md) avec le verdict final, puis merger.
