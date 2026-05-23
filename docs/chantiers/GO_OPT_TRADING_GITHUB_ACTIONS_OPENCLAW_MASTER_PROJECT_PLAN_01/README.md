# GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01

## 1_MASTER_TARGET

`github_actions_openclaw`

## 4_MASTER_PROJECT_PLAN

GitHub Actions prépare, valide et expose les jobs CI.
Le repo conserve le registre canonique.
OpenClaw orchestre ensuite via GitHub API / `workflow_dispatch`, sans exécuter directement la logique de validation.

## 7_CANONICAL_STATE

État d'ouverture :

- workflows GitHub Actions existants détectés :
  - `.github/workflows/strict-workers-validate.yml`
  - `.github/workflows/strict-workers-smoke.yml`
  - `.github/workflows/openclaw-mcp-policy-static-validator.yml`
- registre non-trading existant détecté :
  - `docs/chantiers/GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01/10_NON_TRADING_JOBS_REGISTER.md`
- risque de doublon confirmé sur :
  - strict worker job packet validation
  - strict worker readonly smoke
  - repo diff check / static validator checks

## 8_VALIDATED_PLAN

1. Ne pas créer de CI parallèle.
2. Construire d'abord l'inventaire et le registre.
3. Réutiliser les workflows existants si leur scope couvre déjà un job.
4. Ajouter uniquement les jobs manquants.
5. Tester Actions avant orchestration.
6. Ouvrir child GO OpenClaw seulement après PASS.

## 11_KEY_DECISIONS

- GitHub Actions = exécution CI.
- OpenClaw = orchestration.
- Registry repo = contrat entre les deux.
- `workflow_dispatch` = premier point d'entrée orchestrable.
- Aucun self-hosted runner au départ.
- Aucun runtime trading dans ce master plan.
- Aucun merge/apply automatique.

## 12_INVARIANTS

- PASS CI ne vaut pas merge.
- Patch draft ne vaut pas apply.
- Child GO ne ferme pas master target.
- OpenClaw ne déclenche que des jobs déclarés dans le registre.
- Toute écriture sensible reste HITL.

## 17_RESUME_POINT

Reprendre depuis :

1. appliquer le patch d'ouverture sur branche dédiée ;
2. relire `GITHUB_ACTIONS_WORKFLOWS_INVENTORY_01.yml` ;
3. valider `GITHUB_ACTIONS_JOBS_REGISTRY_01.yml` ;
4. produire les jobs manquants dans un child GO séparé.
