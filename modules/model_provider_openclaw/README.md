# model_provider_openclaw

Module V1 de politique provider/modèle pour OpenClaw.

## Objectif
Centraliser et borner la sélection des providers, modèles, paramètres par défaut et fallbacks pour les agents OpenClaw.

## Périmètre V1
- providers autorisés
- modèles autorisés
- mapping agent -> provider/modèle primaire
- mapping agent -> fallback
- bornes par agent
- commandes `status` et `sanity`

## Agents couverts
- orchestrateur
- builder
- reviewer
- lab

## Structure
- `app/model_provider_openclaw.py` : logique de lecture/validation/export
- `config/providers_policy.yaml` : politique globale des providers
- `config/agent_model_matrix.yaml` : matrice agent -> provider/modèle/bornes/fallback
- `docs/model_provider_openclaw.doc.md` : doctrine et règles V1
- `scripts/*.sh` : exécution standardisée

## Commandes
```bash
bash scripts/cmd.sh status
bash scripts/cmd.sh sanity
bash scripts/cmd.sh show-agent orchestrateur
bash scripts/cmd.sh export-json
```

## Intégration visée
Ce module doit être installable via `install_module_openclaw` comme les autres modules standards.

## Règle V1
Aucun agent OpenClaw ne choisit directement son provider/modèle.
Toute résolution passe par `model_provider_openclaw`.
