# Consolidation strict workers

## Etat strict workers relu

- `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` existe sur sa branche dediee
- son closeout courant est explicitement `CLOSEOUT_PARENT_DRAFT_ONLY`
- la phase validee est bornee a la documentation, au registry modele et a un smoke `read-only`
- aucun `PATCH_DRAFT`, aucun write runtime et aucune promotion `PASS` globale n'y sont autorises

## Decision de rattachement

- `strict workers` est **rattache** a `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` pour la carte machine et la gouvernance
- `strict workers` n'est **pas** retenu comme parent machine autonome pour `fantome`
- `AI Team` reste le principal ; `strict workers` devient une surface specialisee adjacente sous ce principal

## Ce qui est absorbe

- la gouvernance machine `fantome`
- la place des micro-workers a autonomie etroite dans l'architecture AI Team
- la separation d'avec `cursor-ai`, qui orchestre mais ne porte pas les workers paralleles candidats

## Ce qui est conserve tel quel

- la branche `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01`
- les preuves `DRAFT_ONLY` deja figees
- les invariants `read-only`, `no secrets`, `validation externe`, `pas de write durable sans GO distinct`

## Ce qui reste differe

- toute reexecution technique sur `fantome`
- tout `PATCH_DRAFT`
- toute fusion structurelle entre les artefacts `strict workers` et le parent AI Team

## Limites

- la consolidation ici est documentaire et organisationnelle
- elle ne vaut pas validation runtime de `strict workers` sur `fantome`
- un futur GO enfant explicite reste necessaire si la ligne AI Team passe du cadrage a une execution technique borne
