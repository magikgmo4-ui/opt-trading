#!/usr/bin/env bash
# canon_full_push_student.sh
# 1-click: compile canon FULL + push to student + log
set -euo pipefail

STUDENT_IP="${STUDENT_IP:-192.168.16.103}"
STUDENT_USER="${STUDENT_USER:-student}"

REPO="${REPO:-/opt/trading}"
LOCAL_STUDENT_ARCHIVE="${LOCAL_STUDENT_ARCHIVE:-/opt/trading/_student_archive/journals}"

MOD="/opt/trading/modules/journal_de_bord/scripts"
PY="$MOD/compile_canon.py"

if [[ ! -f "$PY" ]]; then
  echo "ERROR: compile_canon.py not found at: $PY" >&2
  exit 2
fi

TS="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="/tmp/canon_full_${TS}.md"

echo "[jdb] compile_canon.py -> $OUT_DIR"
mkdir -p "$LOCAL_STUDENT_ARCHIVE" 2>/dev/null || true

python3 "$PY" \
  --repo "$REPO" \
  --student_archive "$LOCAL_STUDENT_ARCHIVE" \
  --out "$OUT_DIR"

J="$OUT_DIR/JOURNAL_CANON_FULL.md"
T="$OUT_DIR/TODO_CONSOLIDE_FULL.md"

if [[ ! -s "$J" || ! -s "$T" ]]; then
  echo "ERROR: canon files missing/empty:" >&2
  ls -lah "$OUT_DIR" || true
  exit 3
fi

echo "[jdb] sizes:"
wc -c "$J" "$T" || true

# Store locally in a ghost-writable place (no sudo)
ADMIN_CANON_DIR="/opt/trading/_student_archive/journals/canon_admin"
mkdir -p "$ADMIN_CANON_DIR" 2>/dev/null || true

J2="$ADMIN_CANON_DIR/JOURNAL_CANON_FULL_${TS}.md"
T2="$ADMIN_CANON_DIR/TODO_CONSOLIDE_FULL_${TS}.md"
cp -f "$J" "$J2"
cp -f "$T" "$T2"
chmod 644 "$J2" "$T2" 2>/dev/null || true

echo "[jdb] push to student:/tmp"
scp "$J2" "$T2" "${STUDENT_USER}@${STUDENT_IP}:/tmp/"

echo "[jdb] move on student (no sudo)"
ssh "${STUDENT_USER}@${STUDENT_IP}" "mkdir -p /opt/trading/_student_archive/journals/canon 2>/dev/null || true
mv -f /tmp/JOURNAL_CANON_FULL_${TS}.md /opt/trading/_student_archive/journals/canon/ || echo 'MOVE_FAIL_J'
mv -f /tmp/TODO_CONSOLIDE_FULL_${TS}.md   /opt/trading/_student_archive/journals/canon/ || echo 'MOVE_FAIL_T'
ls -lah /opt/trading/_student_archive/journals/canon/*_${TS}.md 2>/dev/null || true
"

# Auto-log if available
if command -v cmd-post_change >/dev/null 2>&1; then
  cmd-post_change journal_de_bord "Canon FULL 1-click push (student)" "canon FULL+TODO compiled + pushed to student (TS=${TS})" <<MD
## Résultat
- Canon FULL + TODO FULL générés + push OK vers student (TS=${TS})
- Student:
  - /opt/trading/_student_archive/journals/canon/JOURNAL_CANON_FULL_${TS}.md
  - /opt/trading/_student_archive/journals/canon/TODO_CONSOLIDE_FULL_${TS}.md
MD
fi

echo "PASS: canon_full_push_student TS=${TS}"
