\
#!/usr/bin/env bash
set -euo pipefail
DIR="${1:-}"
if [[ -z "$DIR" ]]; then
  echo "Usage: $0 </mnt/usb/student_backup_YYYYMMDD_HHMMSS>"
  exit 1
fi
if [[ ! -f "$DIR/manifest.sha256" ]]; then
  echo "ERROR: manifest.sha256 not found in $DIR"
  exit 1
fi
echo "Verifying checksums..."
( cd "$DIR" && sha256sum -c manifest.sha256 )
echo "OK: verified."
