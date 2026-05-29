# 10_IMPLEMENTATION_SPEC

## Module structure

```text
modules/telegram_ingestion/
  normalizer/
    __init__.py
    message_normalizer.py    — normalize(raw) → InboundMessage
    type_detector.py         — classifier le type du message
    metadata_extractor.py    — extraire mentions, hashtags, URLs
```

## TypeDetector

Détecte le type du message selon les règles :

| Type | Règle |
|---|---|
| `link` | raw_text contient une URL |
| `poll` | sender contient "poll" ou raw_text commence par "Poll" |
| `image` | sender contient "media" ou raw_text est vide avec sender média |
| `text` | fallback |

## MetadataExtractor

Extrait depuis `raw_text` :

- `mentions` : toutes les entités `@username`
- `hashtags` : tous les `#topic`
- `links` : toutes les URLs (http/https)

## MessageNormalizer

```python
def normalize(raw: RawMessage) -> InboundMessage:
    msg_type = detect_type(raw)
    metadata = extract_metadata(raw.raw_text)
    return InboundMessage.from_raw(raw, normalized_type=msg_type, metadata=metadata)
```

## Tests

- `test_detect_type_text` — message texte normal
- `test_detect_type_link` — message avec URL
- `test_detect_type_poll` — message poll
- `test_detect_type_image` — message média
- `test_detect_type_empty` — message vide → text
- `test_extract_mentions` — extrait @mentions
- `test_extract_hashtags` — extrait #hashtags
- `test_extract_links` — extrait URLs
- `test_extract_no_metadata` — pas de metadata
- `test_extract_empty_text` — texte vide
- `test_normalize_text` — RawMessage → InboundMessage complet
- `test_normalize_with_metadata` — avec mentions/hashtags/links
- `test_normalize_minimal` — sender=None, sans metadata
