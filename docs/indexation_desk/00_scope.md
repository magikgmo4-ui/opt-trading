# 00_scope.md

## Session
- **Date (America/Montreal)**: 2026-03-07
- **Titre**: Indexation complète Desk / MSI / Dell / Debian avant extension écran réseau et reprise API
- **Source brute**: `/opt/trading/_work/indexation_desk/raw_inventory_20260307_054013.log`
- **Session seed historique**: preuve opératoire retirée du canon journal depuis

## But de la phase
Créer une cartographie fiable, exploitable et non destructive de l’existant pour :
- comprendre ce qui existe déjà dans le repo et sur la machine `admin-trading`
- distinguer clairement les surfaces **opérateur / dev / maintenance**
- identifier les gaps réels avant toute extension (écran réseau Debian, intégrations API, rationalisation UI MSI)
- préparer une suite de travail ordonnée sans casser le setup actuel

## Périmètre inclus
- inventaire des modules présents dans `/opt/trading/modules`
- inventaire des scripts standards `menu.sh`, `cmd.sh`, `sanity_check.sh`
- inventaire des wrappers globaux `/usr/local/bin`
- inventaire des services/timers systemd liés au desk / trading / vision / webhook / perf
- inventaire des emplacements de logs et de journalisation
- première cartographie des rôles machines / écrans
- première gap analysis structurelle et opératoire

## Périmètre exclu pour cette phase
- refactor global du repo
- renommage massif de modules / wrappers
- migration UI vers une autre machine
- branchement massif d’API (Alternative.me, Bitget, etc.)
- changement de comportement des services existants
- nettoyage architectural profond des héritages (`fix1/fix2/fix3`, steps historiques, etc.)

## Contraintes de travail
- **lecture / structuration seulement** sauf mini-ajustement documentaire si nécessaire
- toute future modif devra être **minimale, traçable, sanity-checkée et documentée**
- ne pas rouvrir le chantier `student_deepseek_ops_v1.0_hotfix2` sauf régression
- conserver l’état stable déjà validé sur `origin/sot/mainline`

## État technique constaté
- `admin-trading` est désormais réaligné sur `origin/sot/mainline` via rebase propre
- HEAD local observé pendant l’indexation : `ce8d228` (`Journal update: 2026-03-07 05:26 | note60`)
- base fonctionnelle récente présente dans l’historique :
  - `a7b008f` — `desk_pro: add derivatives_analyzer v1`
  - `e5485f5` — `desk_pro: integrate derivatives context into probability_engine`

## Observation synthétique
Le repo contient déjà une grande partie des briques Desk Pro métier, UI et ops. Le problème principal n’est pas l’absence de modules, mais l’**hétérogénéité de la surface opérateur**, la **couverture incomplète des wrappers globaux**, et la **lisibilité encore imparfaite entre couches métier, ops, maintenance et écrans cibles**.

## Résultat attendu de cette phase
À la fin de l’indexation, on doit pouvoir répondre clairement à :
1. quels modules existent et à quoi servent-ils réellement ?
2. lesquels sont exposés proprement à l’opérateur ?
3. quels éléments tournent réellement en exploitation ?
4. quelle machine / quel écran porte quel rôle ?
5. quels sont les gaps prioritaires avant la phase écran réseau + API ?

## RISKS

- À qualifier.
