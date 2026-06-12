# GO_SECURITY_CREDENTIAL_ROTATION_SCHEDULE_01

## Objectif

Documenter les dates d'expiration, rotation et statut de chaque credential dans le registre.
Aucune valeur de secret ne doit apparaître — uniquement : owner, provider, host, rôle, criticité,
dernière rotation connue, prochaine rotation prévue, statut.

## Périmètre

Tous les credentials actifs dans `configs/env/registry/credentials.yaml` :
- tokens API (PAT GitHub, Botpress PAT, Botpress BAK, Figma, Airtable, ClickUp, OpenAI)
- clés de marché gratuites (CoinGecko, AlphaVantage, FRED, EIA, Finnhub, TwelveData)
- secrets webhook (TV_WEBHOOK_KEY, Botpress webhook secret)
- credentials Telegram (bot token, session)
- credentials infrastructure (SSH keys, ADC Google)

## Critères d'acceptance

- [ ] Table de rotation complète dans `20_ROTATION_SCHEDULE.md`
- [ ] Chaque credential a : owner, provider, criticité, TTL recommandé, dernière rotation, prochaine rotation, statut
- [ ] Aucune valeur secrète exposée
- [ ] `credentials.yaml` enrichi avec champs `rotation_ttl_days` et `last_rotated` (optionnel)

## Règles

- Ne pas rotater les secrets pendant ce chantier — documentation uniquement
- Les dates de création/rotation sont déduites du contexte (ce qui est connu)
- Statut : FRESH / UNKNOWN / STALE / EXPIRING_SOON
