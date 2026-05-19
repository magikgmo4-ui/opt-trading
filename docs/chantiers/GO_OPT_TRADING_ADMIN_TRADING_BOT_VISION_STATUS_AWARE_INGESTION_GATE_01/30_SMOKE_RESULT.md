# 30_SMOKE_RESULT

## Tests effectués

| Test | Consumer | Attendu | Obtenu | Verdict |
|---|---|---|---|---|
| `status=ready` | vision_bot | process normal | - | PENDING |
| `status=invalid_visual` | vision_bot | skip → rejected | - | PENDING |
| `status=blocked` (JSON seul) | vision_bot | archive → rejected | - | PENDING |
| `status=invalid_visual` | bridge | skip pick_latest | - | PENDING |
| `status=ready` | bridge | pick_latest OK | - | PENDING |
| `status=blocked` | ingest | skip → rejected | - | PENDING |

## Vérifications

- [ ] `python3 compile` OK (tous)
- [ ] `bash -n` OK (bridge)
- [ ] Aucun `.uploading` stale
- [ ] `profiles.example.json` inchangé
