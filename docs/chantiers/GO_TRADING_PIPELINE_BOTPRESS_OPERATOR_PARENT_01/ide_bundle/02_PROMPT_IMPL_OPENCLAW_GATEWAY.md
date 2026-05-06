# PROMPT — ADAPTER LE GATEWAY OPENCLAW EXISTANT POUR BOTPRESS

## OBJECTIF

Adapter l'integration Botpress vers le Gateway OpenClaw deja existant.

Ce prompt ne doit pas creer un nouveau gateway.

## ETAT CANONIQUE

- OpenClaw Gateway existe deja.
- Botpress doit l'appeler comme surface d'orchestration.
- Le travail porte sur le contrat d'appel, l'adapter Botpress, la securite et les tests.

## A FAIRE

1. Identifier l'endpoint OpenClaw reel deja disponible.
2. Documenter :
   - URL locale ou reseau
   - methode HTTP
   - auth ou token si present
   - payload accepte
   - format de reponse
   - erreurs connues
3. Creer seulement si necessaire un adapter mince cote Botpress.
4. Ajouter un smoke test Botpress -> OpenClaw existant.
5. Journaliser la trace dans opt-trading si le contrat le permet.

## A NE PAS FAIRE

- ne pas recreer OpenClaw Gateway
- ne pas dupliquer le gateway
- ne pas deplacer la logique OpenClaw
- ne pas ajouter de trade reel
- ne pas ajouter de push Git automatique

## CONTRAT CIBLE A DOCUMENTER

Le contrat exact doit venir du gateway existant.

Si un wrapper d'adaptation est necessaire, il doit rester minimal :

- recevoir une intention Botpress
- convertir vers le payload attendu par OpenClaw
- appeler OpenClaw
- retourner une reponse normalisee a Botpress

## SORTIE ATTENDUE

Produire un rapport avec :

- endpoint OpenClaw reel identifie
- ecart entre payload Botpress et payload OpenClaw
- adapter requis ou non
- smoke test propose
- limites restantes
- prochain GO logique
