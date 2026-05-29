# 05_DATA_CENTER_INGESTION

## Objectif

Data Center recoit le maximum, pas seulement les signaux resumes.

## Payloads minimaux a pousser

- image raw ref
- image annotee ref si disponible
- metadata capture
- analyse JSON
- outputs derives
- refs pour relecture DeskPro

## Handoff attendu

```text
screenshot -> metadata capture -> analysis json -> data center payload -> consumer views
```

## Champs cibles minimaux

- `capture_id`
- `timestamp_utc`
- `source`
- `screen_type`
- `asset`
- `asset_class`
- `timeframe`
- `url_key`
- `image_path`
- `analysis_status`
- `deskpro_status`
- `telegram_status`

## Hypothese a verifier

- liaison vers `visual_context`
- liaison vers `desk_snapshot.v1`
- liaison vers `market_metrics.v1` si certaines analyses deviennent metrics
