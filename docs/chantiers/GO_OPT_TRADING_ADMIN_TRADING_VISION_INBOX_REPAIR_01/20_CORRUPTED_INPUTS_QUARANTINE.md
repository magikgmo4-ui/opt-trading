---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01_QUARANTINE
doc_type: quarantine_log
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_CORRUPTED_INPUTS_QUARANTINE

## Quarantaine

**Chemin**: `/srv/sftp/shared_files/shared/quarantine/GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01_20260504T190858Z/`

## Fichiers deplaces (14)

### 0-byte PNGs (9)

Tous proviennent de `/srv/sftp/shared_files/shared/vision_inbox/`:
- screen_2026-03-05_23-08-47_8.png (0 B)
- screen_2026-03-05_23-45-30_2.png (0 B)
- screen_2026-03-05_23-55-30_0.png (0 B)
- screen_2026-03-06_01-37-07_3.png (0 B)
- screen_2026-03-06_01-57-07_9.png (0 B)
- screen_2026-03-06_02-07-07_3.png (0 B)
- screen_2026-03-06_03-37-07_9.png (0 B)
- screen_2026-03-06_03-57-07_0.png (0 B)
- screen_2026-03-06_04-07-07_7.png (0 B)

### .uploading partiels (5)

Tous proviennent de `/srv/sftp/shared_files/shared/vision_inbox/`:
- screen_2026-04-03_10-56-15_7.png.uploading.* (535 KB)
- screen_2026-04-03_16-16-14_5.png.uploading.* (515 KB)
- screen_2026-04-04_07-36-16_2.png.uploading.* (339 KB)
- screen_2026-04-04_07-46-16_5.png.uploading.* (338 KB)
- screen_2026-04-04_09-36-16_5.png.uploading.* (338 KB)

## Methode

- Commande `mv` uniquement (pas de `rm`)
- Aucune suppression directe
- Fichiers renommes avec leur chemin complet (prefixe path)
- Manifests before/after conserves dans la quarantaine

## Fichiers NON touches

- `__init__.py` (0-byte legitimes)
- `py.typed` (marqueurs PEP 561)
- `.gitkeep` (placeholders)
- Fichiers dans `/opt/trading/.venvs/` (environnements Python)
- Images valides (data/desk_pro/vision/, desk/snapshots/)
