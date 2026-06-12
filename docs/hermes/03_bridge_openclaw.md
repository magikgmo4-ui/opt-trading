# Bridge Hermes ↔ OpenClaw

## Objectif

Permettre un flux simple :

Hermes -> generation
OpenClaw -> execution
Validation -> repo

## Structure

tools/hermes_bridge/
- generate.sh
- exec.sh
- prompt.txt

## Workflow

1. generate.sh produit un script via Hermes
2. exec.sh execute le script
3. resultat observe
4. validation humaine

## Regles

- pas d'auto-commit
- pas d'execution non controlee
- validation obligatoire avant integration

## RISKS

- À qualifier.
