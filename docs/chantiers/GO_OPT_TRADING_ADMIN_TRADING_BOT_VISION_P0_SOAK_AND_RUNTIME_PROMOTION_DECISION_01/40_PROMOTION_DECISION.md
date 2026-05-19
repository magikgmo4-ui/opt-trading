# 40_PROMOTION_DECISION

## Décision

`PROMOTE_P0_RUNTIME`

## Motivation

1. Les 3 surfaces P0 ont tenu `3` cycles manuels consécutifs.
2. Les `12` captures observées sont toutes `ready / pass`.
3. Ingestion `vision_processed` et extraction `vision_outbox` sont stables.
4. Aucun `blocked` ni `invalid_visual` observé pendant le soak.
5. Les consumers status-aware sont présents dans la base de travail.

## Réserve explicitement maintenue

- Cette décision est une **décision de promotion**, pas l’application de la promotion.
- La modification du runtime actif, du timer ou des profils runtime doit rester dans un GO séparé.

## Risque résiduel

- Le bridge Desk n’a pas été activé durant cette fenêtre manuelle, donc la preuve Desk est indirecte :
  - absence de non-ready pendant le soak
  - gate consumer présent et vérifié dans le code

Ce risque résiduel est jugé acceptable pour ouvrir un GO séparé de promotion runtime.
