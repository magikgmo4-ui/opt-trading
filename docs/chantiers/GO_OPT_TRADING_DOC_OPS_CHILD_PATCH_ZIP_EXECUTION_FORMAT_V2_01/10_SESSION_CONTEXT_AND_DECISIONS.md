---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01_SESSION_CONTEXT_AND_DECISIONS
doc_type: session_context
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01
status: draft_canonical
lifecycle_stage: opening
surface: chantier
source_kind: canonical
updated_at: 2026-05-22
topic_keys:
  - session_context
  - decisions
  - patch
  - zip
---

# 10_SESSION_CONTEXT_AND_DECISIONS

## 1_MASTER_TARGET

Documenter la session qui a conduit au format V2 `.patch` / `.zip`.

## 2_SESSION_SUMMARY

La session a demarre par une verification des souvenirs et de la matrice. Deux regles ont ete considerees importantes :

- `PLAN_VALIDE_CHAIN` : plan valide -> target + master_target -> bundle + patch -> utilisateur depose patch -> IDE applique/valide/commit/push/PR/review -> evaluation target/master_target.
- `GLOBAL_INDEX_RULE` : les index globaux changent seulement si master target, horizon ou statut global changent vraiment ; sinon parent local + inbox + target status.

La discussion a ensuite clarifie que le `.patch` pouvait porter plus que du code : il peut aussi porter les docs, plans, prompts, job packets, checklists et directives destines au repo.

## 3_DECISIONS_VALIDATED

### Decision 1 — `.patch` principal

Le `.patch` est l'artefact canonique d'execution Git.

### Decision 2 — `.zip` optionnel

Le `.zip` n'est pas produit par defaut. Il sert aux payloads lourds, temporaires ou hors repo.

### Decision 3 — docs dans patch

Si une documentation doit rester dans le repo, elle va dans le `.patch`.

### Decision 4 — job graph dans patch

Le `.patch` doit decrire les jobs a deleguer aux strict workers, workers externes et modeles forts.

### Decision 5 — OpenClaw E2E

OpenClaw doit pouvoir lire le patch et executer le chantier via runbook, preflight, gates et evidence.

### Decision 6 — workers existants avant creation

Avant de creer de nouveaux jobs, reutiliser les tasks existantes : READ_INVENTORY, FAST_TRIAGE, PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, ENDPOINT_AUDIT, WRITE_GATED.

### Decision 7 — app external workers sous contrat

Airtable, ClickUp, Botpress, Sheets, Telegram, Gmail, Calendar, Drive, Figma et LocalCMS doivent etre utilises seulement selon les contrats existants.

## 4_CORRECTIONS_DE_FORMULATION

Formulation utilisateur convertie en regle operatoire :

> Un patch de chantier doit contenir le plan final valide, le prompt de lancement, les steps operatoires, les jobs et workers a deleguer, les directives OpenClaw, les checklists, les preuves attendues, les gaps, le closeout cible et les job packets strict workers. Un zip sidecar peut accompagner le patch seulement pour les scripts lourds, payloads, logs, captures, prompts longs ou instructions humaines hors repo.

## 5_INVARIANTS_DE_SESSION

- Ne pas produire un zip par habitude.
- Ne pas laisser les docs importantes hors Git.
- Ne pas creer de couche worker parallele.
- Ne pas utiliser un modele absent du registry.
- Ne pas modifier les index globaux pour une ouverture locale.

## 6_RESUME_POINT

La prochaine action logique est d'appliquer ce patch d'ouverture, puis de tester le format V2 sur un chantier reel avec sidecar zip seulement si le besoin le justifie.
