# 50_DATA_CENTER_HANDOFF

## Objectif

Documenter le schema `max data out` du pipeline vision vers Data Center.

## Categories proposees

- `raw_capture`
- `extracted_signal`
- `generated_summary`
- `distribution_payload`

## Contrat minimal

| Champ | Description |
|---|---|
| source_url | origine de la capture |
| capture_timestamp | horodatage |
| asset_scope | assets / indices / screener concernes |
| capture_ref | reference de l'image source |
| extracted_data | champs structures extraits |
| generated_outputs | sorties derivees |
| confidence | niveau de confiance |
| schema_version | version du payload |

## TODO

- `DATA_CENTER_MAX_DATA_OUT_SCHEMA`
