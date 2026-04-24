# naming_normalizer

## Description
Module durable audit-only pour auditer le nommage dans `opt-trading`, avec verification structurelle du canon GO deja publie dans le repo.

Lecture canonique :
- lire d'abord `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- utiliser `docs/governance/NAMING_CANON_POLICY_01.md` comme surface operatoire locale de nommage
- ne pas utiliser ce module comme surface souveraine de canonisation

## Mission V1
- scanner certaines surfaces du repo
- detecter les ecarts de nommage
- proposer un nom canonique quand la structure suffit
- marquer review-required quand une canonisation source manque
- generer :
  - un rapport markdown
  - un rapport json

## Canon retenu
- GO : `GO_<SCOPE>_<PRODUCT_OR_SURFACE>_<ROLE>_<OBJECT>_<NN>`
- doc_id / autres IDs documentaires : `UPPER_SNAKE_CASE`
- dossiers modules : `lower_snake_case`
- scripts et fichiers applicatifs : `lower_snake_case`
- fichiers ordonnes : `NN_lower_snake_case.ext`
- branches : `family/lower-kebab-case`

## Regle sur `<PRODUCT_OR_SURFACE>`
Le module ne canonise pas un nouveau token `<PRODUCT_OR_SURFACE>`.
Si un nouveau token apparait dans un exemple ou une proposition, il doit etre traite comme :
`a canoniser d'abord dans le canon produit ou la carte de surfaces avant toute application repo`

## Granularite regex GO retenue
La verification structurelle GO du module repose sur la granularite suivante :

- `<SCOPE>` = 1 token uppercase
- `<PRODUCT_OR_SURFACE>` = 1 a n tokens uppercase
- `<ROLE>` = `PARENT` ou `CHILD`
- `<OBJECT>` = 1 a n tokens uppercase
- `<NN>` = 2 chiffres minimum

La regex verifie la forme structurelle attendue.
Elle ne remplace pas :
- la canonisation de `<PRODUCT_OR_SURFACE>` dans le canon produit ou la carte de surfaces
- la validation documentaire du vocabulaire metier

## Portee V1
- `docs/chantiers/*`
- `docs/governance/*`
- `modules/*`

## Hors perimetre V1
- apply automatique
- renommage physique
- corrections de contenu interne
- migration de masse
- validation semantique implicite d'un nouveau `<PRODUCT_OR_SURFACE>`

## Usage
```bash
bash modules/naming_normalizer/cmd.sh explain-rules
bash modules/naming_normalizer/cmd.sh audit /chemin/du/repo
bash modules/naming_normalizer/scripts/audit_naming.sh /chemin/du/repo
```

## Sorties
Par defaut :
- `modules/naming_normalizer/output/naming_audit_report.md`
- `modules/naming_normalizer/output/naming_audit_report.json`

## Structure
- `app/` : logique Python
- `config/` : regles et exceptions
- `scripts/` : wrappers d'usage
- `output/` : rapports generes
