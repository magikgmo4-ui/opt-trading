---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01
surface: ADMIN_TRADING
source_kind: canonical
updated_at: 2026-05-19
---

# 50_RETENTION_ARCHIVE_POLICY

## Objectif

Definir une politique de conservation avant toute archive ou suppression.

## Classes de retention

| Classe | Regle |
| --- | --- |
| `raw_inbox` | temporaire, traite puis deplace |
| `processed` | court terme seulement, 48h a 7j selon validation humaine |
| `canonical_daily` | garder 1 ou 2 screenshots/jour/page |
| `rejected` | court terme pour debug, 7j par defaut |
| `compressed_archive` | vieux screenshots compresses par jour/page apres manifest |
| `delete_candidate` | 0-byte, `.uploading` stale, doublons exacts, screenshots noirs/vides |

## Regle quotidienne

Conserver par defaut :

```text
1 screen / jour / page
```

Option session critique :

```text
2 screens / jour / page :
- NY open / session active
- NY close / fin de session
```

## Manifest obligatoire avant mutation

Toute archive, compression ou suppression doit produire un manifest avant action :

```json
{
  "manifest_id": "vision_retention_YYYYMMDD_HHMMSSZ",
  "mode": "dry_run",
  "base": "/srv/sftp/shared_files/shared",
  "generated_at_utc": "2026-05-19T14:30:00Z",
  "ruleset": "canonical_daily_v1",
  "candidates": [
    {
      "path": "/srv/sftp/shared_files/shared/vision_inbox/example.png",
      "action": "keep_canonical",
      "reason": "first_valid_screen_for_page_day"
    }
  ]
}
```

## Interdits

- Pas de suppression sans manifest.
- Pas de suppression dans ce chantier initial.
- Pas de compression sans validation humaine.
- Pas d'archive de fichiers `.uploading`.
- Pas de retention si l'ingestion n'est pas d'abord prouvee PASS.

## Selection canonical_daily

Ordre de priorite :

1. fichier PNG valide ;
2. sidecar JSON parseable ;
3. page_id reconnu ;
4. dimensions attendues ;
5. hash non duplique ;
6. timestamp proche de la fenetre cible ;
7. presence downstream si disponible.

## Etat actuel

Retention effective bloquee : absence de PNG et ingestion non prouvee.

