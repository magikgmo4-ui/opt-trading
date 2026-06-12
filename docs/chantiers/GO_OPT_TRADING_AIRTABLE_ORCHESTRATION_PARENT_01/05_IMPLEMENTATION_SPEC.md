# 05_IMPLEMENTATION_SPEC — Airtable Bridge V1

## OBJECTIF

Implémenter un module `airtable_bridge` non bloquant pour opt-trading.

## STRUCTURE MODULE

modules/airtable_bridge/
- app/client.py
- app/payloads.py
- scripts/sanity_check.sh
- scripts/cmd.sh
- scripts/menu.sh
- .env.example

## API

POST https://api.airtable.com/v0/{base_id}/{table}

Headers:
Authorization: Bearer TOKEN
Content-Type: application/json

## RÈGLES CLIENT

- batch max 10
- retry exponentiel
- handle 429
- timeout safe

## FAIL-OPEN

- si erreur → log uniquement
- jamais bloquer core

## ENV

AIRTABLE_API_KEY=
AIRTABLE_BASE_ID=

## PAYLOADS

trade:
- symbol
- direction
- entry_price
- exit_price

signal:
- source
- timestamp

## SANITY

- test env
- test API

## INVARIANTS

- no blocking
- no infinite retry

## NEXT

impl module airtable_bridge

## RISKS

- À qualifier.
