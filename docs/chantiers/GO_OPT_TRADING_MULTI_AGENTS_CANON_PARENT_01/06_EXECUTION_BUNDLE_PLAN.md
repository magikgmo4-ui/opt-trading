---
doc_id: OPT_TRADING_MULTI_AGENTS_EXECUTION_BUNDLE_PLAN_01
doc_type: bundle_plan
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: bundle_plan
topic_keys:
  - opt-trading
  - multi_agents
  - bundle
  - execution_pack
  - prompt_factory
  - workflow_ai
  - indexation
search_tags:
  - surface:chantier
  - doc_role:bundle_plan
  - bundle:execution
  - execution:doc_only
  - governance:multi_agents_doctrine
  - integration:validated_prompt_factory
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "BUNDLE_EXECUTION_PROMPT.txt"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/01_EXISTING_SOCLE_READOUT.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/02_AGENT_SKILL_PROVIDER_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/03_FRONTMATTER_SEARCH_TAGS_NAMING_DOCTRINE.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/05_OPERATIONAL_MATRIX_INTEGRATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/GAP_INDEXATION.md
---

# 06_EXECUTION_BUNDLE_PLAN — Multi-agents

## 1. Objet

Definir le bundle d'execution doc-only pour poursuivre le chantier multi-agents sans dependance a la session ChatGPT.

Ce bundle doit transporter :

- le contexte canonique ;
- les documents produits ;
- les consignes d'execution ;
- les interdits ;
- la checklist de validation ;
- le plan de propagation index ;
- le point de reprise.

## 2. Nom de bundle recommande

```text
GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01_execution_bundle.zip
```

Emplacement recommande si produit sur machine :

```text
/srv/sftp/shared_files/shared/documents/doc-workflow/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01_execution_bundle.zip
```

Ou, si production locale repo uniquement :

```text
bundles/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01_execution_bundle.zip
```

Rappel : le bundle reste support secondaire. Le repo Git reste source de verite.

## 3. Contenu minimal du bundle

Inclure :

```text
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/01_EXISTING_SOCLE_READOUT.md
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/02_AGENT_SKILL_PROVIDER_MATRIX.md
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/03_FRONTMATTER_SEARCH_TAGS_NAMING_DOCTRINE.md
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/05_OPERATIONAL_MATRIX_INTEGRATION_PLAN.md
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/06_EXECUTION_BUNDLE_PLAN.md
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/BRANCH_STATE.md
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/GAP_INDEXATION.md
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/BUNDLE_EXECUTION_PROMPT.txt
```

Inclure en reference, si disponible localement :

```text
workflow_ai/WORKFLOW.md
modules/validated_prompt_factory/README.md
docs/deploy_module_multi_machine_continuity.md
docs/product_targets/OPENCLAW_TARGET_CANON.md
docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md
docs/ot/trae/04_SKILLS_V1.txt
docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt
modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md
modules/model_provider_openclaw/docs/GO_OPENCLAW_PROVIDER_POLICY_04.md
```

## 4. Commande Linux recommandee

Depuis la racine du repo :

```bash
set -Eeuo pipefail
trap 'echo "ERR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

GO_ID="GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01"
OUT_DIR="/srv/sftp/shared_files/shared/documents/doc-workflow"
OUT_ZIP="$OUT_DIR/${GO_ID}_execution_bundle.zip"

mkdir -p "$OUT_DIR"
rm -f "$OUT_ZIP"

zip -r "$OUT_ZIP" \
  "docs/chantiers/$GO_ID" \
  workflow_ai/WORKFLOW.md \
  modules/validated_prompt_factory/README.md \
  docs/deploy_module_multi_machine_continuity.md \
  docs/product_targets/OPENCLAW_TARGET_CANON.md \
  docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md \
  docs/ot/trae/04_SKILLS_V1.txt \
  docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt \
  modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md \
  modules/model_provider_openclaw/docs/GO_OPENCLAW_PROVIDER_POLICY_04.md

test -s "$OUT_ZIP"
ls -lh "$OUT_ZIP"
```

## 5. Commande PowerShell recommandee

Depuis la racine du repo :

```powershell
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

$GO_ID = 'GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01'
$OutDir = Join-Path $PWD 'bundles'
$OutZip = Join-Path $OutDir "$GO_ID`_execution_bundle.zip"

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
if (Test-Path $OutZip) { Remove-Item $OutZip -Force }

$paths = @(
  "docs/chantiers/$GO_ID",
  'workflow_ai/WORKFLOW.md',
  'modules/validated_prompt_factory/README.md',
  'docs/deploy_module_multi_machine_continuity.md',
  'docs/product_targets/OPENCLAW_TARGET_CANON.md',
  'docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md',
  'docs/ot/trae/04_SKILLS_V1.txt',
  'docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt',
  'modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md',
  'modules/model_provider_openclaw/docs/GO_OPENCLAW_PROVIDER_POLICY_04.md'
)

Compress-Archive -Path $paths -DestinationPath $OutZip -Force
Get-Item $OutZip | Select-Object FullName, Length, LastWriteTime
```

## 6. Checklist de validation bundle

Le bundle est valide si :

- le zip existe ;
- le zip contient le dossier chantier complet ;
- le zip contient le prompt d'execution ;
- les references socle principales sont incluses ou explicitement absentes ;
- aucune config runtime n'est modifiee ;
- aucune cle ou secret n'est inclus ;
- le bundle peut etre lu par Trae / Claude / ChatGPT / Codex comme contexte transportable.

## 7. Instructions d'execution du bundle

Le bundle doit servir a :

1. poursuivre la lecture ;
2. patcher proprement l'indexation globale ;
3. produire un closeout ;
4. preparer eventuellement une promotion vers `docs/governance/` ou `docs/architecture/`.

Il ne doit pas servir a :

- modifier OpenClaw runtime ;
- exposer gateway ;
- ouvrir tools/channels/nodes ;
- lancer trading live ;
- merger automatiquement ;
- remplacer le repo.

## 8. Prompt a inclure

Le fichier `BUNDLE_EXECUTION_PROMPT.txt` doit etre inclus et utiliser le mode suivant :

- role : agent doc-only ;
- contexte : chantier multi-agents ;
- mission : poursuivre indexation globale et closeout ;
- hors-scope : runtime, trading live, config OpenClaw, merge auto.

## 9. Point de reprise

Prochaine action : creer `BUNDLE_EXECUTION_PROMPT.txt`, puis appliquer eventuellement les patchs d'indexation globale en environnement local non tronque.

## RISKS

- À qualifier.
