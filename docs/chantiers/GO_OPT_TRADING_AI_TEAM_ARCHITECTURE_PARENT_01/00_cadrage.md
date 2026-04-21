# GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 — 00_cadrage

## 1_MASTER_TARGET

Établir un chantier parent canonique, autonome et réutilisable pour cadrer la conception, l’évaluation documentaire et la future implémentation d’une architecture d’"équipe d’agents" spécialisée, inspirée des modèles de type Marblism, mais transposable au contexte interne avec surfaces réelles, mémoire partagée, orchestration, validation humaine et outillage durable.

## 2_INITIAL_PROJECT_DOC

Document de référence initial du projet pour ce chantier parent :
`docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md`

Rôle :
- fiche de référence obligatoire du parent ;
- transport initial complet du besoin ;
- base canonique autonome pour la suite des GO enfants ;
- ne doit pas être réécrit implicitement hors changement réel de projet.

## 3_INITIAL_NEED

Ouvrir un chantier parent, 100% indépendant de la session, documenté adéquatement, pour consolider :
- le modèle d’équipe d’agents à rôles spécialisés ;
- la mémoire / contexte partagé ;
- les intégrations aux surfaces réelles ;
- le mode proactif et l’automatisation ;
- la surface documentaire utile au développement ;
- l’étude comparative avec modèles open source / dev-first comparables ;
- le plan canonique complet pour la suite.

## 4_MASTER_PROJECT_PLAN

Direction validée :
1. Cadrer le modèle cible « équipe d’agents spécialisés ».
2. Séparer clairement : produit observé, architecture conceptuelle, architecture cible interne.
3. Canoniser les axes : rôles, mémoire, handoffs, surfaces, orchestration, HITL, sécurité, observabilité, gouvernance documentaire.
4. Préparer des GO enfants séparés :
   - audit documentaire sources externes ;
   - cartographie des patterns réutilisables ;
   - architecture cible interne ;
   - MVP / setup ;
   - closeout de conception.
5. Garder le parent strictement doc-only et canonique.

## 5_GO_PLAN

Workstreams dérivés du parent :
- GO_CHILD_01 : collecte documentaire et preuves externes ;
- GO_CHILD_02 : comparatif frameworks / produits ;
- GO_CHILD_03 : architecture canonique d’équipe d’agents ;
- GO_CHILD_04 : setup MVP et surfaces d’exécution ;
- GO_CHILD_05 : sécurité, mémoire, filtrage, HITL ;
- GO_CHILD_06 : closeout et synthèse canonique.

## 6_FINAL_TARGET

Livrable de cette phase :
- un parent canonique autonome ;
- un état de départ retenu ;
- un plan complet ;
- les invariants ;
- les décisions déjà prises ;
- les gaps restants ;
- les prochains GO logiques.

## 7_CANONICAL_STATE

État canonique courant retenu :
- l’intérêt principal porte sur le pattern « équipe d’agents spécialisés » ;
- Marblism est traité comme source d’inspiration produit, non comme framework dev-first confirmé ;
- la reconstruction interne doit être pensée comme architecture durable, séparable du produit observé ;
- le parent présent sert de base de continuité indépendante de la session ;
- aucun setup technique final n’est encore validé ;
- aucun GO enfant n’est encore ouvert dans ce parent.

NEXT_GO logique :
- ouvrir un GO enfant d’audit documentaire et de collecte de sources techniques utiles au développement.

## 8_VALIDATED_PLAN

Étapes validées vers la cible de phase :
1. Fixer le cadre canonique du parent.
2. Ancrer les blocs structurants et tags au bon niveau.
3. Éviter toute confusion entre :
   - observation produit,
   - hypothèses techniques,
   - architecture cible.
4. Préparer la filiation documentaire des GO enfants.
5. Conserver le parent en doc-only.

## 9_SELECTED_SOLUTION

Approche retenue :
- chantier parent documentaire unique ;
- séparation stricte entre cadrage, journal technique, décisions ;
- usage explicite des tags d’état ;
- continuité par état canonique + point de reprise ;
- aucune dérive immédiate vers implémentation sans GO enfant dédié.

## 10_SELECTED_SETUP

Setup documentaire retenu pour le parent :
- `00_cadrage.md` : cadre canonique complet ;
- `02_journal_technique.md` : journal borné des actions réellement faites ;
- `03_decisions.md` : décisions validées, exclusions, verdict, reprise.

## 11_KEY_DECISIONS

- Le dépôt canonique de travail pour ce chantier est `magikgmo4-ui/opt-trading`.
- Le parent est ouvert en doc-only sur la branche dédiée `go_repos_agent-role_initial_01`.
- Marblism n’est pas traité comme base technique interne directe.
- Les frameworks open source / dev-first comparables feront l’objet d’un travail séparé et tracé.
- Le parent doit rester 100% autonome et réutilisable hors session.

## 12_INVARIANTS

- Ne pas confondre produit observé et architecture cible interne.
- Ne pas dériver vers une implémentation sans GO enfant dédié.
- Ne pas rouvrir les décisions déjà établies sans raison explicite.
- Conserver la séparation `13_ESTABLISHED` / `14_HYPOTHESIS` / `16_TODO`.
- Utiliser `7_CANONICAL_STATE` comme base de reprise.
- Le parent reste doc-only tant qu’aucun GO enfant d’application n’est validé.

## 13_ESTABLISHED

- Le besoin utilisateur principal est la modélisation d’une équipe d’agents à rôles spécialisés.
- Les axes majeurs déjà identifiés sont : rôle, mémoire partagée, intégrations réelles, proactivité.
- La documentation publique observée jusqu’ici permet surtout une lecture produit / opérateur.
- Un chantier parent autonome est nécessaire pour éviter la dépendance à la session.

## 14_HYPOTHESIS

- Une architecture interne réutilisable peut être dérivée du pattern observé.
- Les sources les plus utiles côté développement seront probablement extérieures au produit observé.
- Une séparation manager / spécialistes / mémoire / outils / validation humaine sera probablement le meilleur axe d’architecture.

## 15_REMAINING_GAP

Il manque encore :
- l’audit documentaire complet des sources techniques ;
- la matrice comparative produit vs framework ;
- l’architecture canonique interne détaillée ;
- le setup MVP retenu ;
- la politique de mémoire / sécurité / filtrage / observabilité ;
- la séquence de GO enfants validée avec contenu précis.

## 16_TODO

Actions suivantes concrètes :
1. Ouvrir un GO enfant d’audit documentaire ciblé.
2. Recenser les docs utiles au développement.
3. Établir un comparatif structuré des modèles proches.
4. Produire un schéma d’architecture canonique interne.
5. Préparer le GO de setup MVP.

## 17_RESUME_POINT

Reprendre depuis `7_CANONICAL_STATE`, puis rappeler `1_MASTER_TARGET`, `2_INITIAL_PROJECT_DOC`, `4_MASTER_PROJECT_PLAN`, replacer `5_GO_PLAN` et `6_FINAL_TARGET`, puis ouvrir le prochain GO enfant logique sans réinterpréter les hypothèses comme des faits.

## 18_TO_DOCUMENT

TAGS :
- `1_MASTER_TARGET`
- `2_INITIAL_PROJECT_DOC`
- `3_INITIAL_NEED`
- `4_MASTER_PROJECT_PLAN`
- `5_GO_PLAN`
- `6_FINAL_TARGET`
- `7_CANONICAL_STATE`
- `8_VALIDATED_PLAN`
- `9_SELECTED_SOLUTION`
- `10_SELECTED_SETUP`
- `11_KEY_DECISIONS`
- `12_INVARIANTS`
- `13_ESTABLISHED`
- `14_HYPOTHESIS`
- `15_REMAINING_GAP`
- `16_TODO`
- `17_RESUME_POINT`

Blocs à extraire :
- `AI_TEAM_PARENT_CADRAGE_CANONIQUE`
- `AI_TEAM_PARENT_INVARIANTS`
- `AI_TEAM_PARENT_NEXT_GO`

## 19_TO_REMEMBER

TAGS :
- `NO_MEMORY`

Blocs :
- `AUCUN_AJOUT_MEMOIRE_DURABLE_AUTOMATIQUE`
