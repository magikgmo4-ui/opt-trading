# PROJECT_CARD_MODULE_CONTEXTUALS_SHELL_01

Date: 2026-04-14

A documenter ? Oui, fiche.

## Objet
Figer une fiche compacte et uniforme pour module_contextuals_shell.

## Besoin initial
Retrouver en un seul point pourquoi ce socle existe, quelle cible finale a ete retenue, quel plan valide a ete suivi, ce qui est deja etabli et quel est le prochain GO utile.

## Cible finale / But final
Faire de module_contextuals_shell un socle partage pour les futurs modules shell, afin de standardiser declaration d actions, lecture robuste, menus dynamiques et routage vers les scripts cibles.

## Plan valide
1. Creer un socle generique au lieu de recoder menu et dispatch dans chaque module shell.
2. Passer vers une logique declarative d actions via fichiers .ctx.
3. Fournir lecture, rendu et routage standardises.
4. Permettre a un menu global de scanner les contextuals des modules et d indexer leurs actions.
5. Reduire ensuite la friction d adoption par les futurs modules shell.

## ETABLI
- Le README identifie explicitement le module comme socle partage pour la gestion des actions contextuelles des modules shell.
- La cible declaree est tous les futurs modules shell.
- Le module standardise deja fichiers .ctx, lecture robuste, menus dynamiques et routage des actions.
- La structure du module couvre lib, contextuals, examples et docs.
- Une surface operable existe deja via cmd.sh et sanity.sh.
- Le README explicite deja une integration future avec un menu global capable de scanner les contextuals des modules.

## Gap restant
Le manque principal restant porte sur le gel court de son adoption par les modules aval, plus que sur sa definition architecturale elle-meme.

## Next GO / Reprise
- GO porteur : GO_PROJECT_CARDS_FREEZE_01
- Next GO retenu : GO_MODULE_CONTEXTUALS_SHELL_ADOPTION_FREEZE_01
- Raison : une passe documentaire d adoption est plus utile qu un elargissement artificiel du scope du socle.

## References repo utiles
- modules/module_contextuals_shell/README.md
- modules/module_contextuals_shell/cmd.sh
- modules/module_contextuals_shell/sanity.sh
- modules/module_contextuals_shell/lib/discovery.sh
- modules/module_contextuals_shell/examples/example.ctx
