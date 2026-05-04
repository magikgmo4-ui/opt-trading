---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01_CONTRACT
doc_type: data_contract
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01
status: open
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 40_DATA_CONTRACT — Vision Inbox

## Contrat de sortie bot_vision_headless -> vision_inbox

### Nommage

```
screen_YYYY-MM-DD_HH-mm-ss_RANDOM.png
```

Exemple: `screen_2026-05-04_16-30-00_a3f2.png`

Compatible avec le format actuel utilise par ShareX.
`RANDOM` = 4 caracteres hexa ou numeriques pour eviter collisions.

### Ecriture atomique obligatoire

```
1. Ecrire dans /tmp/bot_vision_headless/capture_YYYYMMDDHHmmss.png
2. Verifier taille > 0
3. Copier vers vision_inbox/.screen_YYYY-MM-DD_HH-mm-ss_RANDOM.png.uploading
4. Verifier taille > 0 du .uploading
5. Renommer: mv .uploading -> screen_YYYY-MM-DD_HH-mm-ss_RANDOM.png
```

Pourquoi atomique:
- vision_bot watch loop detecte les fichiers des qu'ils apparaissent
- Un .uploading partiel peut etre lu avant la fin de l'ecriture
- Le rename est atomique sur le meme filesystem

### Format

| Propriete | Valeur |
| --- | --- |
| Format | PNG |
| Resolution | 1920x1080 ou full-page |
| Taille min | > 0 (verifie avant rename) |
| Taille max | < 10 MB |
| Compression | Lossless (PNG default) |

### Sidecar (optionnel, futur)

```json
{
  "source_url": "https://...",
  "capture_ts": "2026-05-04T16:30:00Z",
  "method": "playwright_headless",
  "viewport": "1920x1080",
  "status": "ready"
}
```

Fichier: `screen_YYYY-MM-DD_HH-mm-ss_RANDOM.json` (meme nom que le PNG)

### Garde-fous anti-corruption

1. **Taille > 0**: verifiee avant tout move vers vision_inbox
2. **Atomic write**: .uploading -> rename (pas de fichier partiel visible)
3. **Timeout capture**: max 30s, sinon abort
4. **Retry**: max 2 tentatives en cas d'echec
5. **Cleanup tmp**: supprimer /tmp/bot_vision_headless/* apres chaque cycle
6. **Pas de .uploading abandonnes**: le wrapper nettoie les .uploading > 5 min

### Statut

| Fichier | Signification |
| --- | --- |
| screen_*.png | Capture prete, vision_bot peut la traiter |
| .screen_*.png.uploading | Ecriture en cours, vision_bot NE DOIT PAS la lire |
