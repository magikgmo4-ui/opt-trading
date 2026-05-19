# 40_PROMOTION_DECISION

## Décision

`PROMOTION_CANDIDATE_AFTER_CONTROLLED_SOAK`

## Pourquoi

- Les 3 surfaces P0 ont maintenant au moins une route/stratégie `ready` avec `visual_status=pass`.
- Les consumers status-aware (`7476721b`) sont présents dans la base de travail.
- Les captures retenues ont réellement été ingérées (`vision_processed`) et extraites (`vision_outbox`).

## Ce qui n’est pas fait dans ce GO

1. aucune promotion timer/runtime
2. aucune politique de rétention/archive
3. aucune modification de profil runtime actif

## Recommandation de suite

1. faire un court soak non runtime avec le profil principal retenu
2. vérifier plusieurs cycles sur 24h
3. seulement ensuite ouvrir le GO de promotion runtime / rétention
