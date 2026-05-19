# UI Indexation — Scope

## Objectif
Construire d’abord une **registry UI / machine map** avant tout refactor ou développement ciblé d’une UI spécifique.

## Direction validée
- Héberger **le plus de surfaces UI opérateur possible sur MSI / db-layer**.
- Séparer les surfaces :
  - `ui/index/modules`
  - `ui/dev`
  - `ui/probabilites_trades`
  - `ui/screenshots_analyses_passees`
- **Conserver les screenshots avec leurs analyses**.
- Les artefacts non critiques pourront aller plus tard dans la routine quotidienne.

## Règles
- Ne pas refactorer les engines.
- Ne pas commencer par `desk_pro_dashboard` / `deskpro_toolbox` / `perf_ui` directement.
- Cartographier d’abord : machine, module, rôle, utilisateur, statut, données, priorités.
- Distinguer clairement UI opérateur vs UI dev/debug.

## Priorité actuelle
Créer une vue claire de :
1. ce qui existe déjà,
2. ce qui doit être centré sur MSI,
3. ce qui reste technique,
4. ce qui doit devenir une vraie UI utilisateur plus tard.
