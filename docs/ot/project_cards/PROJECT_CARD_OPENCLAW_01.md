# PROJECT_CARD_OPENCLAW_01

Date: 2026-04-14

A documenter ? Oui, fiche.

## Objet
Figer une fiche compacte et uniforme pour OpenClaw.

## Besoin initial
Retrouver en un seul point pourquoi OpenClaw existe dans opt-trading, quelle cible finale a ete retenue, quel plan valide a ete suivi, ce qui est deja etabli et quel est le prochain GO utile.

## Cible finale / But final
Fixer OpenClaw, dans opt-trading, comme un cockpit operateur local sur db-layer, centre sur installation, configuration, gateway locale, diagnostic, export de preuves et policy provider/model.

## Plan valide
1. Documenter le perimetre reel.
2. Outiller le poste operateur local sur db-layer.
3. Stabiliser la chaine install -> config -> gateway -> doctor -> evidence -> policy.
4. Garder explicites les frontieres de non-perimetre.
5. N ouvrir un chantier plus large que sur besoin operatoire reel et verifiable.

## ETABLI
- Projet cible reel deja fixe comme cockpit operateur local sur db-layer.
- Chaine deja documentee : install -> config -> gateway -> configure -> doctor -> evidence -> policy.
- Usages prouves : menu, policy provider/model, validation config, diagnostic runtime, gateway locale, export de preuves.
- Frontieres explicites : pas de serving expose, pas de runtime multi-machine generalise, pas de migration runtime deja decidee vers le repo openclaw.

## Gap restant
Le manque principal restant est une feuille de route compacte de maturite plus qu une redefinition du perimetre reel.

## Next GO / Reprise
- GO porteur : GO_PROJECT_CARDS_FREEZE_01
- Next GO retenu : GO_OPENCLAW_STATE_DIR_READ_09
- Raison : reprise documentaire / diagnostique prudente tant qu aucun besoin operatoire reel ne justifie un elargissement produit.

## References repo utiles
- modules/menu_openclaw/docs/GO_OPENCLAW_USAGE_EXAMPLES_09.md
- modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md
- modules/menu_openclaw/docs/README.md
- modules/menu_openclaw/docs/RUNBOOK.txt
