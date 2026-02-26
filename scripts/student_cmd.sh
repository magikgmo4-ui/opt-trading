\
#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading"
MNT="/mnt/usb"

case "${1:-}" in
  status)
    systemctl status student-watchdrop --no-pager || true
    systemctl status student-ingest --no-pager || true
    ;;
  restart)
    sudo systemctl restart student-watchdrop student-ingest
    sudo systemctl status student-watchdrop --no-pager
    sudo systemctl status student-ingest --no-pager
    ;;
  logs)
    journalctl -u student-watchdrop -n 200 --no-pager
    journalctl -u student-ingest -n 200 --no-pager
    ;;
  tail-events)
    tail -n ${2:-20} "$BASE/journal/events/events.jsonl"
    ;;
  ingest-key)
    cat "$BASE/ingest/INGEST_API_KEY"
    ;;
  ingest-test)
    KEY="$(cat "$BASE/ingest/INGEST_API_KEY")"
    curl -s -X POST http://127.0.0.1:8020/ingest -H "Content-Type: application/json" -H "X-API-Key: $KEY" -d '{"session":"cmd","note":"ingest-test"}'
    echo ""
    tail -n 1 "$BASE/journal/events/events.jsonl"
    ;;
  rotate-key)
    bash "$BASE/scripts/rotate_ingest_key.sh"
    ;;
  usb-detect)
    bash "$BASE/scripts/usb_detect_mount.sh"
    ;;
  usb-mount-uuid)
    bash "$BASE/scripts/usb_mount_by_uuid.sh" "${2:-}"
    ;;
  usb-backup)
    bash "$BASE/scripts/usb_backup_student.sh"
    ;;
  usb-verify)
    bash "$BASE/scripts/usb_verify_backup.sh" "${2:-}"
    ;;
  open)
    echo "Base: $BASE"
    echo "Events: $BASE/journal/events/events.jsonl"
    echo "Outputs: $BASE/journal/outputs/"
    echo "Drop: $BASE/drop"
    echo "Archive: $BASE/archive"
    echo "Ingest: $BASE/ingest (port 8020)"
    echo "USB mount: $MNT"
    ;;
  *)
    echo "Usage: cmd-student {status|restart|logs|tail-events [N]|ingest-key|ingest-test|rotate-key|usb-detect|usb-mount-uuid <UUID>|usb-backup|usb-verify <DIR>|open}"
    exit 1
    ;;
esac
