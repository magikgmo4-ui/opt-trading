# 20_TEST_PLAN

## Tests

| Test | Cible | Type |
|---|---|---|
| `test_detect_type_text` | TypeDetector → text | unit |
| `test_detect_type_link` | TypeDetector → link | unit |
| `test_detect_type_poll` | TypeDetector → poll | unit |
| `test_detect_type_image` | TypeDetector → image | unit |
| `test_detect_type_empty` | TypeDetector → text sur vide | unit |
| `test_extract_mentions` | MetadataExtractor → @mentions | unit |
| `test_extract_hashtags` | MetadataExtractor → #hashtags | unit |
| `test_extract_links` | MetadataExtractor → URLs | unit |
| `test_extract_no_metadata` | MetadataExtractor → empty lists | unit |
| `test_extract_empty_text` | MetadataExtractor → empty lists | unit |
| `test_normalize_text` | MessageNormalizer → InboundMessage(text) | unit |
| `test_normalize_link` | MessageNormalizer → InboundMessage(link) + URLs | unit |
| `test_normalize_poll` | MessageNormalizer → InboundMessage(poll) | unit |
| `test_normalize_minimal` | MessageNormalizer → sender=None | unit |

## Critères

- 100% tests passant
- 0 dépendance réseau
- 0 modification de l'inbound parser
