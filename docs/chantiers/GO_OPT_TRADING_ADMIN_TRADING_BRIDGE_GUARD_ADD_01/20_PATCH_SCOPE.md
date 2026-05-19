---
doc_id: BRIDGE_GUARD_01_PATCH
doc_type: patch_scope
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BRIDGE_GUARD_ADD_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_PATCH_SCOPE

## 3 guards ajoutes

### 1. pick_latest() — skip invalid candidates

```
while read candidate; do
  [[ "$candidate" == *.uploading* ]] && continue  # skip partial uploads
  [ -s "$candidate" ] || continue                  # skip 0-byte
  f="$candidate"; break
done < <(ls -1t ...)
```

Applique a vision_processed ET vision_inbox.

### 2. main() — verify before crop

```
if [[ "$src" == *.uploading* ]]; then exit 0; fi
if [ ! -s "$src" ]; then exit 0; fi
```

### 3. crop_with_python() — verify before Image.open

```python
if not os.path.exists(src) or os.path.getsize(src) <= 0:
    sys.exit(0)
if os.path.basename(src).endswith(".uploading"):
    sys.exit(0)
```

## Comportement preserve

| Input | Comportement |
| --- | --- |
| PNG valide (> 0) | Traite normalement (crop + ingest) |
| PNG 0-byte | SKIP (silencieux, exit 0) |
| .uploading | SKIP (silencieux, exit 0) |
| Pas de PNG | exit 2 (comportement existant) |
