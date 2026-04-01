# Validated Prompt Factory

## Description
Ce module transforme une synthèse validée (format texte structuré) en un prompt final spécialisé, prêt à être utilisé avec une IA ou pour un transfert.

## Nouvelle règle de posture / rôles
À partir de maintenant, les prompts générés par ce module doivent intégrer une étape initiale obligatoire :
1. proposer les rôles / postures pertinents pour la demande ;
2. donner un exemple bref du type de sortie attendu pour chaque rôle ;
3. recommander une posture par défaut ;
4. ensuite seulement démarrer le travail.

Cette règle s’applique aux modes de génération du module et doit être traitée comme un comportement canonique du Prompt Factory.

## Runbook opérateur (canonique, minimal)
### Quand utiliser
- Quand tu as une synthèse structurée (sections complètes) et que tu veux produire un prompt final standardisé.
- Quand tu veux exécuter le workflow nominal via wrappers globaux (`/usr/local/bin/*`) sur Linux cible.

### Quand ne pas utiliser
- Si tu n’as pas la synthèse complète : la validation bloque volontairement (ne pas contourner).
- Si tu veux un nouveau mode / une API : hors mission de ce module.

### Parcours nominal (Linux cible)
Depuis le repo root :
```bash
cd /opt/trading

# 1) Vérifier les modes
cmd-validated_prompt_factory list-modes

# 2) Générer le prompt (cas nominal)
cmd-validated_prompt_factory generate trae_patch modules/validated_prompt_factory/inputs/synthesis_registry_central.txt

# 3) Générer le prompt bundle
cmd-validated_prompt_factory generate bundle_transfer modules/validated_prompt_factory/inputs/synthesis_bundle_transfer.txt

# 4) Vérifier l’intégrité (help + génération + échec attendu)
sanity-validated_prompt_factory
```

### Où récupérer les outputs
- Dossier : `modules/validated_prompt_factory/output/`
- Fichiers : `prompt_<mode>.txt` (écrasé à chaque génération pour un même mode)

## Modes de génération
1. **chatgpt_session** : Prompt conversationnel pour ChatGPT (Expert Senior).
2. **trae_module** : Prompt structuré pour créer un nouveau module durable dans Trae.
3. **trae_patch** : Prompt strict pour appliquer un patch correctif dans Trae.
4. **bundle_transfer** : Prompt pour préparer une archive ZIP de transfert.

## Cas standard retenus (2–3 maximum)
- Patch Trae (cas nominal) :
  - Entrée : `modules/validated_prompt_factory/inputs/synthesis_registry_central.txt`
  - Mode : `trae_patch`
  - Output : `modules/validated_prompt_factory/output/prompt_trae_patch.txt`
- Bundle transfer (cas nominal) :
  - Entrée : `modules/validated_prompt_factory/inputs/synthesis_bundle_transfer.txt`
  - Mode : `bundle_transfer`
  - Output : `modules/validated_prompt_factory/output/prompt_bundle_transfer.txt`
- Session ChatGPT (optionnel, si besoin de cadrage) :
  - Entrée : `modules/validated_prompt_factory/inputs/synthesis_example.txt`
  - Mode : `chatgpt_session`
  - Output : `modules/validated_prompt_factory/output/prompt_chatgpt_session.txt`

## Validation d’entrée
La synthèse d’entrée doit contenir toutes les sections requises. Si une section manque, la génération échoue avec un message explicite “Missing sections”.

Les en-têtes peuvent être fournis en texte brut ou sous forme de titres Markdown (ex: `## CONTEXTE`).

Sur Windows, l’exécution nominale passe par Python :
```bash
python modules/validated_prompt_factory/app/validated_prompt_factory.py --input <file> --mode <mode> --output-dir <dir>
```

## Sorties
- Par défaut via wrappers globaux et `cmd.sh` : fichiers écrits dans `modules/validated_prompt_factory/output/`.
- Le fichier `prompt_<mode>.txt` est écrasé à chaque génération pour un même mode.

## Erreurs attendues / lecture rapide
- `Error: Missing sections in synthesis: ...` : synthèse incomplète (corriger l’input).
- `Error: Input file not found: ...` : mauvais chemin ou fichier absent sur la machine (vérifier `modules/validated_prompt_factory/inputs/`).
- `/usr/bin/env: 'bash\r': ...` : scripts `.sh` en CRLF (revenir à LF ; `.gitattributes` force `*.sh eol=lf`).
- `menu-validated_prompt_factory` : interactif (à tester manuellement côté opérateur, pas en non-interactif SSH).

## Smoke wrappers (Linux)
- Le smoke nominal des wrappers (`cmd.sh`, `sanity.sh`) se fait sur une machine Linux cible (bash).
- Sur poste Windows, un bash type Git Bash peut exécuter les wrappers, mais ce n’est pas une preuve “Linux cible”.
- Pré-requis : line endings LF pour les `.sh` (bash). Le repo force `*.sh text eol=lf` via `.gitattributes`.

## Structure
- `app/` : Logique Python.
- `inputs/` : Exemples de synthèses.
- `output/` : Prompts générés.
- `cmd.sh` : Wrapper CLI.
- `menu.sh` : Wrapper Menu.
- `sanity.sh` : Script de validation.
