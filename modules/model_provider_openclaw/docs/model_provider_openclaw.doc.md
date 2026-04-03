# model_provider_openclaw — doctrine V1

## But
Empêcher la sélection libre et implicite des providers/modèles par les agents OpenClaw.

## Décisions V1
1. Les providers sont explicitement autorisés ou refusés.
2. Chaque agent a un provider primaire, un modèle primaire et un fallback.
3. Chaque agent reçoit des bornes par défaut.
4. Toute configuration invalide doit faire échouer `sanity`.
5. Le module n'exécute aucun appel provider réel en V1 ; il sert de couche de politique et de validation.

## Providers V1
- autorisés : `openrouter`, `openai_compatible_local`
- refusés par défaut : tout provider non listé

## Modèles V1 retenus
Exemples prudents, à ajuster plus tard selon l'inventaire réel des modèles côté OpenClaw :
- orchestrateur : `qwen/qwen3-32b`
- builder : `qwen/qwen3-coder-30b-a3b-instruct`
- reviewer : `deepseek/deepseek-r1`
- lab : `qwen/qwen3-14b`

## Bornes par défaut V1
- temperature bornée
- top_p borné
- max_output_tokens borné
- mode deterministic / strict pour reviewer

## Contrat agent
- orchestrateur : stabilité, arbitrage, faible permissivité
- builder : génération/transformation sous contraintes
- reviewer : vérification stricte
- lab : exploration bornée, hors prod libre

## Fallback policy V1
- fallback dans la liste autorisée seulement
- fallback obligatoire pour chaque agent
- si primaire et fallback invalides : échec explicite

## Suite logique
1. installer le module
2. relier l'installation au flux `install_module_openclaw`
3. brancher ensuite `configure_openclaw` / `doctor_openclaw` si nécessaire
