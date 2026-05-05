# 50_PHASE_5 — Pont optionnel admin-trading

## Objectif

Déterminer si les exports TradingView Observer doivent alimenter desk/admin-trading.

## IMPORTANT

Cette phase est **optionnelle**.
Elle ne doit être ouverte que si les phases 1 à 4 sont **PASS**.

## Ponts possibles

- Copie JSON contrôlée vers `/srv/sftp/shared_files/shared`
- Feed manuel desk_pro
- Analyse via modules existants
- Comparaison avec webhook TradingView (validation croisée)

## Interdictions

- Pas de remplacement webhook (admin-trading reste canonique).
- Pas d'ingestion automatique avant validation humaine.
- Pas d'effet sur risk engine.

## Critère PASS

admin-trading peut consommer une sortie observer sans modifier le runtime existant.

## Résultat

**Statut** : [PASS / PARTIAL / FAIL / SKIPPED]

**Détail** :
