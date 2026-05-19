# Hermes Lab — Overview

## Contexte

Hermes Lab introduit Hermes Agent comme couche cognitive expérimentale dans l'écosystème `opt-trading`.

## Rôles

- `opt-trading` : source de vérité canonique
- `sot/mainline` : branche de continuité
- Hermes : génération, mémoire de travail, orchestration légère
- OpenClaw : exécution système / sandbox / automation d'exécution
- Ollama : moteur local
- Hugging Face : surfaces de publication et de démonstration

## Règle centrale

Aucun artefact produit par Hermes ne devient canonique sans validation humaine et commit Git.

## Périmètre V1

Le lab vise un flux minimal et contrôlé :

1. Hermes génère un artefact
2. un exécuteur lance l'artefact dans un cadre contrôlé
3. le résultat est observé
4. l'humain valide
5. le repo conserve

## Hors périmètre V1

- auto-commit
- auto-merge
- vérité projet déplacée dans Hermes
- publication HF automatique
- gouvernance du projet hors du repo
