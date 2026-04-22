# GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_DOC_AUDIT_01 — 00_cadrage

## Identité

- GO enfant : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_DOC_AUDIT_01`
- Parent : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
- Repo : `magikgmo4-ui/opt-trading`
- Branche canonique : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
- Nature : doc-only
- Objet : audit documentaire et collecte bornée de sources techniques utiles au développement d'une architecture d'équipe d'agents

## Lien Parent

- cadrage parent : `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md`
- décisions parent : `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/03_decisions.md`
- ancrage parent : premier GO enfant logique d'audit documentaire explicitement prévu par `7_CANONICAL_STATE` et `16_TODO`

## ETABLI

- Le parent validé demande en premier un GO enfant d'audit documentaire et de collecte de sources techniques.
- Ce GO enfant reste strictement documentaire et n'autorise aucune implémentation.
- Le besoin immédiat est de distinguer :
  - produit observé ;
  - frameworks et patterns techniques réutilisables ;
  - architecture interne cible encore non décidée.
- Le livrable attendu de ce GO enfant est un corpus borné, exploitable et traçable pour des travaux enfants ultérieurs.

## HYPOTHESE

- Les sources les plus utiles au développement seront probablement des frameworks, documentations techniques et dépôts open source plutôt que la seule documentation produit.
- Un bornage strict des familles de sources réduira le risque de dérive documentaire ou de confusion architecture/marketing.

## TODO

- auditer les familles de sources retenues ;
- qualifier leur utilité réelle pour le développement ;
- séparer les preuves établies des hypothèses d'architecture ;
- produire un point de reprise exploitable par les prochains GO enfants.

## Périmètre d'audit autorisé

- documentation publique du produit observé `Marblism`, limitée à ce qui éclaire le modèle opératoire apparent ;
- documentations techniques publiques de frameworks d'agents et d'orchestration multi-agents ;
- dépôts open source et README de frameworks dev-first comparables ;
- documentation technique sur mémoire partagée, handoffs, orchestration, outils, validation humaine, observabilité et sécurité applicables à une équipe d'agents ;
- comparatifs et schémas techniques quand ils sont directement exploitables pour la conception.

## Hors périmètre

- toute implémentation locale ;
- tout benchmark runtime ;
- tout choix final de stack ;
- toute décision finale d'architecture interne ;
- toute ouverture implicite d'un GO enfant supplémentaire.

## Critères PASS / FAIL

- PASS si : le GO enfant produit un bornage clair des sources, une séparation stricte entre établi/hypothèse/todo, et une base documentaire exploitable pour la suite.
- FAIL si : le contenu mélange audit, implémentation, choix de stack, ou traite des hypothèses comme des faits.

## Point de reprise

- Reprendre sur la branche `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`.
- Relire le parent puis ce cadrage enfant.
- Démarrer l'audit uniquement dans le périmètre autorisé.
- Consigner uniquement du réel exécuté dans `02_journal_technique.md`.
- Porter les arbitrages validés dans `03_decisions.md`.
