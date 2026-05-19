# GO_GITHUB_PARK_AUDIT_EXPANSION_01 — 01_plan

## Classification

diagnostic ponctuel — audit repo-first élargi

## Besoin initial

Étendre l’audit GitHub park sans casser le canon repo-first :
partir du repo canonique et du cadrage validé, puis exploiter les bundles et inventaires externes uniquement comme supports secondaires.

## Cible finale parent

Obtenir une cartographie croisée repo / branches / trunk / rôle de fichiers permettant de statuer proprement sur le parc GitHub, sans promouvoir les artefacts externes au rang de canon.

## Plan validé

1. Reprendre le cadrage parent `GO_GITHUB_PARK_AUDIT_EXPANSION_01`.
2. Garder `opt-trading` comme source canonique d’exécution.
3. Utiliser les supports externes comme entrées secondaires :
   - `github_park_file_role_cartography_01_bundle.zip`
   - `github_repo_inventory_full.md`
   - `github_repo_inventory_full.json`
   - `github_repo_inventory_from_zips_v2.md`
4. Exécuter le sous-GO immédiat : `GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01`.
5. Produire un verdict borné : ETABLI / HYPOTHESE / CONTRADICTION / TODO.
6. Écrire le résultat dans le repo sous le chantier parent.

## ETABLI

- Repo canonique : `opt-trading`
- Branche canonique de continuité : `sot/mainline`
- `GO_GITHUB_PARK_AUDIT_EXPANSION_01` : statut `open`
- Les bundles / inventaires hors repo sont des supports secondaires, non canoniques
- Sous-GO immédiat retenu : `GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01`

## Séparation des rôles

### Repo / product role

Porter le canon, les décisions validées, les points de reprise et les verdicts.

### IA role

Lire le cadrage, croiser les supports, distinguer ETABLI vs HYPOTHESE, consolider le verdict.

### Machine / IDE role

Ouvrir les supports secondaires, extraire les constats utiles, écrire uniquement dans le repo cible.

## Gap restant

Le parent est cadré mais l’audit croisé branches / trunk n’est pas encore exécuté.

## Next GO

`GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01`

## Sortie attendue

- un audit repo-first borné
- un verdict PASS/FAIL ou OPEN clairement justifié
- un point de reprise canonique
- aucun élargissement hors périmètre sans décision explicite

Prompt IDE prêt à exécuter

Ce prompt est aligné avec le cadrage actuel, avec opt-trading comme repo canonique, les inventaires ZIP comme supports secondaires, et un audit borné sur le sous-GO GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01.

GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01

Classification
- diagnostic ponctuel
- repo-first
- forward-only
- docs-only sauf nécessité explicite contraire

Rôle recommandé
- Auditeur repo-first

Canon à respecter
- repo canonique: opt-trading
- branche canonique de continuité: sot/mainline
- l’état réel du repo et de la session prime
- les bundles et inventaires hors repo sont des supports secondaires, jamais la source canonique

Entrées autorisées
- docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md
- github_park_file_role_cartography_01_bundle.zip
- github_repo_inventory_full.md
- github_repo_inventory_full.json
- github_repo_inventory_from_zips_v2.md

Objectif
Exécuter un audit croisé trunk / branches / rôle de fichiers du GitHub park, en partant du cadrage parent et en utilisant les supports externes uniquement comme matériaux de vérification secondaire.

Méthode imposée
1. Vérifier d’abord l’état Git réel du repo local opt-trading.
2. Lire le cadrage parent du GO.
3. Extraire depuis les supports secondaires uniquement les informations utiles au sous-GO:
   - rôle des repos
   - trunk inspecté
   - branches disponibles
   - place de opt-trading dans le parc
4. Produire un audit borné sur:
   - cohérence trunk vs branches
   - cohérence rôle repo vs contenu observé
   - points de contradiction éventuels
   - zones à garder, geler, archiver ou séparer
5. Écrire la sortie dans le repo sous:
   - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_journal_technique.md si travail exploratoire
   - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_decisions.md si décision stabilisée
6. Ne pas promouvoir bundle_zip en canon.
7. Ne faire aucun refactor repo large.
8. Ne modifier aucun index global sauf si le verdict du sous-GO le justifie explicitement.

Format de sortie obligatoire
- Besoin initial
- Cible finale locale GO
- Plan retenu
- ETABLI
- HYPOTHESE
- CONTRADICTION
- GAP restant
- TODO
- REPRISE
- Verdict PASS / FAIL / OPEN

Contrôles finaux
- git status -sb
- liste exacte des fichiers touchés
- diff stat
- justification de périmètre

Interdits
- pas de réécriture d’historique
- pas de promotion du support externe en source canonique
- pas de mélange entre rôle machine, rôle IA, rôle repo
- pas de patch hors périmètre du GO sans le signaler explicitement
