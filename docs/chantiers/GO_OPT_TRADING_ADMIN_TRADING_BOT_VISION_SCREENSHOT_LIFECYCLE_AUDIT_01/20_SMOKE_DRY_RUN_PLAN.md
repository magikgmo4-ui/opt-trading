---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_SCREENSHOT_LIFECYCLE_AUDIT_01
surface: ADMIN_TRADING
source_kind: canonical
updated_at: 2026-05-19
---

# 20_SMOKE_DRY_RUN_PLAN

## Objectif

Verifier le cycle capture -> ingestion sans suppression et sans restart service.

## Smoke read-only deja effectue

Commandes effectuees sans mutation applicative :

- `git fetch origin` pour mettre a jour les refs Git ;
- `git status --short --branch` ;
- inventaire `find` sur `/srv/sftp/shared_files/shared` ;
- lecture des fichiers de configuration suivis Git ;
- `systemctl is-active/is-enabled/list-timers/status` en lecture seule ;
- verification de presence `node_modules/playwright` sans installation.

Resultat : `BLOCKED_WITH_REASON_PLAYWRIGHT_MISSING_NO_PNG_INGESTION_NOT_PROVEN`.

## Commande inventory dry-run documentee

Cette commande ne supprime rien, ne lit pas `.env`, et ne redemarre aucun service.

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

BASE="/srv/sftp/shared_files/shared"

echo "== inventory =="
for d in vision_inbox vision_processed vision_outbox inbox desk/snapshots desk_pro/latest; do
  p="$BASE/$d"
  echo "--- $p"
  if [ -d "$p" ]; then
    total=$(find "$p" -maxdepth 3 -type f 2>/dev/null | wc -l)
    png=$(find "$p" -maxdepth 3 -type f -name "*.png" 2>/dev/null | wc -l)
    json=$(find "$p" -maxdepth 3 -type f -name "*.json" 2>/dev/null | wc -l)
    uploading=$(find "$p" -maxdepth 3 -type f -name "*.uploading" 2>/dev/null | wc -l)
    small=$(find "$p" -maxdepth 3 -type f -size -1024c 2>/dev/null | wc -l)
    zero=$(find "$p" -maxdepth 3 -type f -size 0 2>/dev/null | wc -l)
    echo "files=$total png=$png json=$json uploading=$uploading small_lt_1kb=$small zero_byte=$zero"
  else
    echo "MISSING"
  fi
done

echo "== latest/history =="
for f in "$BASE/desk/snapshots/latest.json" "$BASE/desk/snapshots/history.jsonl" "$BASE/desk_pro/latest/latest.json" "$BASE/desk_pro/latest/history.jsonl"; do
  if [ -f "$f" ]; then
    printf "%s size=%s mtime=%s
" "$f" "$(stat -c %s "$f")" "$(stat -c %y "$f")"
  else
    echo "MISSING $f"
  fi
done

echo "== recent screen files =="
find "$BASE" -type f \( -name "screen_*.png" -o -name "screen_*.json" \) -printf '%TY-%Tm-%Td %TH:%TM %s %p
' 2>/dev/null | sort | tail -100
```

## Capture smoke gate

Ne pas lancer `capture_headless.js` tant que Playwright est absent et que le service est failed.

Apres correction approuvee :

1. desactiver tout risque de collision humaine avant smoke ;
2. executer une capture unique sur `tv_btc_h1` seulement ;
3. verifier PNG + JSON sidecar ;
4. verifier absence `.uploading` stale ;
5. verifier ingestion downstream ;
6. seulement ensuite proposer le passage 3 pages.

## Criteres PASS

| Check | PASS attendu |
| --- | --- |
| PNG valide | fichier `.png` present, > 1 KB, dimensions attendues |
| JSON sidecar | present, parseable, reference le PNG |
| Atomic write | aucun `.uploading` stale |
| Ingestion | fichier traite dans `vision_processed` ou outbox equivalent |
| Extraction | OCR ou metadata visible dans `vision_outbox` |
| Desk bridge | `desk/snapshots/latest.json` ou equivalent mis a jour |

## Criteres BLOCKED

- `playwright` manquant ;
- service capture failed ;
- aucun PNG produit ;
- JSON sidecar orphelin ;
- downstream `vision_processed`/`vision_outbox` vide ;
- `desk/snapshots` manquant.

