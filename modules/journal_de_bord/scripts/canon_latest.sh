\
#!/usr/bin/env bash
# canon_latest.sh
set -euo pipefail

N="${1:-10}"

STUDENT_IP="${STUDENT_IP:-192.168.16.103}"
STUDENT_USER="${STUDENT_USER:-student}"

echo "=== canon_latest (top ${N}) ==="
echo

echo "--- Student canon (via SSH) ---"
ssh "${STUDENT_USER}@${STUDENT_IP}" "ls -1t /opt/trading/_student_archive/journals/canon/JOURNAL_CANON_FULL_*.md 2>/dev/null | head -n ${N} | while read -r f; do
  [ -n \"\$f\" ] || continue
  s=\$(wc -c < \"\$f\" 2>/dev/null || echo 0)
  b=\$(basename \"\$f\")
  ts=\${b#JOURNAL_CANON_FULL_}; ts=\${ts%.md}
  printf \"%s  %8s bytes  %s\n\" \"\$ts\" \"\$s\" \"\$b\"
done" || echo "WARN: could not read student canon (ssh failed?)"

echo
echo "--- Admin canon_admin (local) ---"
ADMIN_DIR="/opt/trading/_student_archive/journals/canon_admin"
if [[ -d "$ADMIN_DIR" ]]; then
  ls -1t "$ADMIN_DIR"/JOURNAL_CANON_FULL_*.md 2>/dev/null | head -n "$N" | while read -r f; do
    [ -n "$f" ] || continue
    s=$(wc -c < "$f" 2>/dev/null || echo 0)
    b=$(basename "$f")
    ts="${b#JOURNAL_CANON_FULL_}"; ts="${ts%.md}"
    printf "%s  %8s bytes  %s\n" "$ts" "$s" "$b"
  done
else
  echo "INFO: $ADMIN_DIR does not exist"
fi

echo
echo "Tip: cmd-journal_de_bord canon_full_push_student generates a new TS and pushes to student."
