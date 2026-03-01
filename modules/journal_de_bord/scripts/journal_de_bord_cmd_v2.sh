\
#!/usr/bin/env bash
# journal_de_bord_cmd_v2.sh
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'TXT'
cmd-journal_de_bord v2

Commands:
  sanity                     -> run sanity_check_journal_de_bord.sh
  canon_full_push_student    -> compile canon FULL + push to student + auto-log
  help                       -> this help

Examples:
  cmd-journal_de_bord sanity
  cmd-journal_de_bord canon_full_push_student
TXT
}

CMD="${1:-help}"
case "$CMD" in
  help|-h|--help) usage ;;
  sanity) exec "$DIR/sanity_check_journal_de_bord.sh" ;;
  canon_full_push_student) shift; exec "$DIR/canon_full_push_student.sh" "$@" ;;
  *) echo "Unknown: $CMD"; usage; exit 1 ;;
esac
