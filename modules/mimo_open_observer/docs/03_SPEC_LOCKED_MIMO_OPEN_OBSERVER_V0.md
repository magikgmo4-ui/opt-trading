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

## Sweep
- true si un extrême de la première M1 est pris avant ou au moment du triplet gagnant
- sides: high | low | both | none

## Journal
- raw append-only
- enriched derived
- stats derived
