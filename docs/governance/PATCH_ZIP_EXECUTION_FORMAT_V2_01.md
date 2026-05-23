---
doc_id: OPT_TRADING_PATCH_ZIP_EXECUTION_FORMAT_V2_01
doc_type: governance_rule
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01
status: draft_canonical
lifecycle_stage: opening
surface: governance
source_kind: canonical
updated_at: 2026-05-22
topic_keys:
  - opt-trading
  - patch
  - zip
  - openclaw
  - strict_workers
  - external_apps
  - evidence
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
  - docs/chantiers/GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01/20_BRIDGE_CONTRACTS.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01/00_INITIAL_PROJECT_DOC.md
---

# PATCH_ZIP_EXECUTION_FORMAT_V2_01

## 1_MASTER_TARGET

Fixer un format canonique d'artefacts pour les chantiers `opt-trading` qui doivent etre executables par IDE, OpenClaw, strict workers, workers app externes et operateur humain.

Le format V2 retient :

- `.patch` : artefact principal, autoporteur, applicable a la racine du repo avec `git apply` ;
- `.zip` : sidecar optionnel reserve aux charges lourdes, temporaires ou hors repo.

## 2_INITIAL_NEED

Les anciens bundles pouvaient separer inutilement le `.patch` et la documentation dans un `.zip`. Cela ajoutait du bruit et rendait moins clair ce qui devait etre commite.

Besoin corrige :

- maximiser ce qui entre dans le `.patch` quand c'est durable ;
- garder le `.zip` seulement pour ce qui n'a pas vocation immediate a entrer dans Git ;
- rendre le tout executable end-to-end par OpenClaw ;
- integrer les strict workers deja presents avant de creer des jobs nouveaux ;
- documenter les gates, preuves, apps externes, checklists humaines et statut target.

## 3_SELECTED_SOLUTION

### 3.1 `.patch` canonique

Le `.patch` contient tout ce qui doit entrer dans le repo :

```text
docs/chantiers/<GO_ID>/00_INITIAL_PROJECT_DOC.md
docs/chantiers/<GO_ID>/05_LAUNCH_PROMPT.md
docs/chantiers/<GO_ID>/10_SESSION_CONTEXT_AND_DECISIONS.md
docs/chantiers/<GO_ID>/20_OPENCLAW_E2E_RUNBOOK.md
docs/chantiers/<GO_ID>/30_WORKER_JOB_GRAPH.md
docs/chantiers/<GO_ID>/40_EXTERNAL_APPS_WORKERS.md
docs/chantiers/<GO_ID>/50_EVIDENCE_CONTRACT.md
docs/chantiers/<GO_ID>/60_HUMAN_CLAUDE_COWORK_CHECKLIST.md
docs/chantiers/<GO_ID>/70_TARGET_STATUS_GAPS_CLOSEOUT.md
docs/index/inbox/<GO_ID>.md
scripts/ai/workers/job_packets/<GO_ID>_*.json
```

### 3.2 `.zip` sidecar optionnel

Le `.zip` est cree seulement si le chantier exige :

- scripts lourds temporaires ;
- payloads volumineux ;
- captures d'ecran ;
- logs bruts ;
- prompts tres longs pour IA lourde ;
- plan d'execution UI par Claude cowork ;
- navigation live souris/clavier ;
- preuves externes non destinees a Git.

Le `.zip` ne doit pas devenir une deuxieme source canonique.

## 4_ARTIFACT_LEVELS

| Niveau | Artefacts | Usage |
| --- | --- | --- |
| LEVEL_1_PATCH_ONLY | `<GO_ID>.patch` | GO simple, doc-only, plan canonique, specs |
| LEVEL_2_PATCH_PLUS_ZIP | `<GO_ID>.patch` + `<GO_ID>__sidecar.zip` | GO avec payloads lourds ou prompts externes |
| LEVEL_3_OPENCLAW_E2E | patch + zip optionnel + job packets + runbook | GO multi-worker, multi-app, multi-surface |

## 5_GLOBAL_RULES

- Si un fichier doit etre commite, il va dans le `.patch`.
- Si un fichier est temporaire ou lourd, il va dans le `.zip`.
- Le `.patch` doit etre comprehensible sans la session ChatGPT.
- Le `.patch` doit inclure les preuves attendues, pas seulement le changement.
- Le `.patch` doit pouvoir etre lu par IDE, OpenClaw, strict workers et humain.
- Le `.zip` peut etre reference par nom et hash dans le `.patch` si present.
- Aucun secret, `.env`, token, credential, cle privee ou payload sensible ne doit etre inclus dans patch ou zip.
- Les index globaux ne changent que si le master target, l'horizon, le statut global ou un batch d'agregation le justifie.

## 6_STRICT_WORKERS_REUSE

Avant de creer un nouveau job IA, verifier les tasks existantes :

- `READ_INVENTORY`
- `FAST_TRIAGE`
- `PATCH_DRAFT`
- `DOC_DRAFT`
- `TESTPLAN`
- `CHERRY_PICK_INVENTORY`
- `ENDPOINT_AUDIT`
- `WRITE_GATED`

Le nouveau format doit produire des job packets alignes avec `scripts/ai/workers/tasks.index.json` et les modeles verifies dans `scripts/ai/workers/models.registry.json`.

## 7_EXTERNAL_APP_WORKERS

Les workers app externes doivent respecter les contrats existants :

- reads/writes autorises ;
- actions interdites ;
- dry-run ;
- approval gate ;
- audit log ;
- rollback ou compensation ;
- `evidence_ref`.

Apps connues : Airtable, ClickUp, Botpress, Google Sheets, Telegram, Gmail, Google Calendar, Google Drive, Figma, LocalCMS.

## 8_OPENCLAW_EXECUTION_RULE

OpenClaw agit comme orchestrateur et gatekeeper :

1. lire le `GO_ID` ;
2. verifier preflight Git et repo ;
3. verifier les tasks workers et modeles disponibles ;
4. router les jobs vers workers existants ;
5. appliquer les gates ;
6. bloquer tout write non autorise ;
7. collecter les preuves ;
8. produire closeout et target status ;
9. ne modifier les index globaux que si la regle globale est declenchee.

## 9_VERDICT

Cette regle ouvre le format V2 : `PATCH_FIRST + ZIP_OPTIONAL + OPENCLAW_E2E + STRICT_WORKERS_MAX_REUSE + EVIDENCE_CONTRACT`.
