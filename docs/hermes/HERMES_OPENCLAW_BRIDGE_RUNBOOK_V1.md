# HERMES OPENCLAW BRIDGE RUNBOOK V1

## But

Décrire un runbook borné pour une première preuve Hermes -> OpenClaw -> validation humaine -> repo, sans surestimer l état réel du bridge.

## Etat réel de départ

A ce stade, le repo porte déjà un cadrage documentaire du bridge dans `docs/hermes/03_bridge_openclaw.md`.

Ce cadrage établit seulement :
- un flux cible simple ;
- une structure visée `tools/hermes_bridge/` ;
- des garde-fous minimaux ;
- aucune preuve ici n établit encore l existence d un bridge exécutable complet dans `sot/mainline`.

## Flux visé

1. Hermes produit un script ou un patch borné
2. OpenClaw exécute ou relit ce script dans un cadre contrôlé
3. le résultat est observé
4. la validation humaine décide de l intégration ou du rejet

## Garde-fous non négociables

- pas d auto-commit
- pas d exécution non contrôlée
- validation humaine obligatoire avant intégration
- pas de confusion entre preuve de bridge et autorisation de production large

## Préconditions minimales

- chaîne OpenClaw documentaire déjà relue
- `GO_OPENCLAW_EVIDENCE_01` clos côté preuves
- `GO_OPENCLAW_SYNC_02` clos côté sync documentaire
- `GO_OPENCLAW_CHAIN_03` clos côté chaîne opérateur
- `GO_OPENCLAW_PROVIDER_POLICY_04` clos côté policy provider/model

## Cas de preuve recommandé

Choisir un cas court, lisible et réversible, par exemple :
- génération d un patch texte simple ;
- relire le patch ;
- exécuter une action bornée ;
- observer le résultat ;
- décider explicitement d intégrer ou non.

Le cas choisi doit rester :
- petit ;
- non destructif ;
- sans exposition réseau nouvelle ;
- sans mutation système large.

## Livrables minimaux attendus

- un prompt ou ordre Hermes borné
- l artefact produit par Hermes
- la preuve de lecture ou d exécution côté OpenClaw
- la validation humaine finale
- un court compte-rendu de résultat

## Condition de close

Le bridge est considéré prouvé pour ce GO seulement si :
- un cas borne a été exécuté de bout en bout ;
- la validation humaine est explicitement tracée ;
- aucun auto-commit ni exécution non contrôlée n a eu lieu ;
- la preuve reste locale, lisible et limitée à ce cas.

## Hors périmètre

- pas de framework bridge complet déclaré comme établi
- pas d orchestration générale multi-cas
- pas de runtime large déduit d une seule preuve
- pas de migration de ce bridge dans le repo `openclaw`

## RISKS

- À qualifier.
