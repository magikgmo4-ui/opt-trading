\
#!/usr/bin/env bash
set -euo pipefail

while true; do
  echo ""
  echo "=== STUDENT MENU (v2) ==="
  echo "1) Sanity check"
  echo "2) Service status"
  echo "3) Service logs (last 200)"
  echo "4) Tail events.jsonl"
  echo "5) Test drop -> archive"
  echo "6) Ingest test (localhost)"
  echo "7) Rotate ingest key"
  echo "8) USB detect"
  echo "9) USB backup to /mnt/usb"
  echo "q) Quit"
  read -r -p "Choice: " c
  case "$c" in
    1) /opt/trading/scripts/student_sanity_check.sh ;;
    2) /opt/trading/scripts/student_cmd.sh status ;;
    3) /opt/trading/scripts/student_cmd.sh logs ;;
    4) /opt/trading/scripts/student_cmd.sh tail-events 20 ;;
    5) echo "hello $(date -Is)" > /opt/trading/drop/test.txt; sleep 1; /opt/trading/scripts/student_cmd.sh tail-events 5 ;;
    6) /opt/trading/scripts/student_cmd.sh ingest-test ;;
    7) /opt/trading/scripts/student_cmd.sh rotate-key ;;
    8) /opt/trading/scripts/student_cmd.sh usb-detect ;;
    9) /opt/trading/scripts/student_cmd.sh usb-backup ;;
    q|Q) exit 0 ;;
    *) echo "Unknown choice" ;;
  esac
done
