# SPEC LOCKED — MIMO OPEN OBSERVER V0

## Mission
Observer XAUUSD à 18:00 (America/Montreal), détecter le premier FVG sur les 5 premières M1, journaliser un événement brut, puis enrichir avec des outcomes simples à +30m / +60m.

## Périmètre
- symbol: XAUUSD
- window: OPEN_1800
- weekdays: sun..thu
- scope: M1x5
- first valid FVG only
- one canonical event per window

## FVG
- bullish: low(c3) > high(c1)
- bearish: high(c3) < low(c1)

## Sweep (règle V0 K3)
- règle retenue: **both sides**
- `sweep = true` si un bar de l'intervalle `[0 .. signal_bar_index]` dépasse strictement un extrême de `bar[0]`
- `bar.high > bar[0].high` → high register
- `bar.low < bar[0].low` → low register
- `sweep_side`: high | low | both | none
- `sweep` booléen: true si `sweep_side != none`

### Note structurelle
- pour un FVG bullish, le bar signal a typiquement son low au-dessus de `bar[0].high` (gap), donc `bar[0].high` est structurellement pris par le bar signal lui-même → sweep=high est quasi systématique
- pour un FVG bearish au triplet 0-1-2, les bars 1..2 descendent sous `bar[0].low` → sweep=low quasi systématique
- la valeur discriminante du sweep pour V0 sera affinée si nécessaire après collecte de données réelles

## Journal
- raw append-only
- enriched derived
- stats derived
