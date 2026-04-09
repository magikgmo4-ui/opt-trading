\
#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading"
echo "=== Student Sanity Check (v2) ==="
echo "Host: $(hostname)"
echo "User: $(whoami)"
echo "IP:   $(ip -br a | tr '\n' ' ' | sed 's/  */ /g')"
echo "Base: $BASE"

for p in "$BASE/journal/events/events.jsonl" "$BASE/scripts/runlog" "$BASE/scripts/watch_drop.sh" "$BASE/drop" "$BASE/archive"; do
  [[ -e "$p" ]] && echo "OK: $p" || { echo "MISSING: $p"; exit 1; }
done

echo ""
echo "--- services ---"
systemctl is-active --quiet student-watchdrop && echo "OK: watchdrop active" || echo "WARN: watchdrop inactive"
systemctl is-active --quiet student-ingest && echo "OK: ingest active" || echo "WARN: ingest inactive"

echo ""
echo "--- swap ---"
(command -v swapon >/dev/null 2>&1 && swapon --show) || /sbin/swapon --show || true

echo ""
echo "PASS: student sanity ok"
