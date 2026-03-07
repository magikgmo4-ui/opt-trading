#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student - CMD Wrapper

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Define DeepSeek Hub location (assuming it's the main entry point)
DEEPSEEK_HUB_CMD="$ROOT_DIR/modules/deepseek_hub/scripts/deepseek_hub_cmd.sh"

cd "$ROOT_DIR" || exit 1

cmd="${1:-help}"

case "$cmd" in
  status|summary)
    bash "$SCRIPT_DIR/deepseek_student_summary.sh"
    ;;

  show-latest-thinking)
    bash "$SCRIPT_DIR/deepseek_student_show_latest_thinking.sh"
    ;;

  show-latest-response)
    bash "$SCRIPT_DIR/deepseek_student_show_latest_response.sh"
    ;;

  show-latest-roadmap)
    bash "$SCRIPT_DIR/deepseek_student_show_latest_roadmap.sh"
    ;;

  daily-log-thinking)
    bash "$SCRIPT_DIR/deepseek_student_daily_log_thinking.sh"
    ;;

  install-daily-timer)
    bash "$SCRIPT_DIR/deepseek_student_install_daily_timer.sh"
    ;;

  timer-status)
    echo "=== Daily Timer Status ==="
    systemctl --user --no-pager --full status deepseek_student_daily_log_thinking.timer || true
    echo "--------------------------"
    systemctl --user --no-pager --full status deepseek_student_daily_log_thinking.service || true
    ;;

  timer-logs)
    echo "=== Daily Timer Logs (Last 50 lines) ==="
    journalctl --user -u deepseek_student_daily_log_thinking.service -n 50 --no-pager
    ;;

  show-paths)
    echo "=== DeepSeek Student Paths ==="
    echo "Root:         $ROOT_DIR"
    echo "Scripts:      $SCRIPT_DIR"
    echo "Hub Cmd:      $DEEPSEEK_HUB_CMD"
    echo "Logs:         $ROOT_DIR/data/logs/deepseek_student"
    echo "Archives:     $ROOT_DIR/_student_archive"
    ;;

  help)
    echo "=== DeepSeek Student Help ==="
    echo "Commands:"
    echo "  think <prompt>       : Run thinking process"
    echo "  response <prompt>    : Run response process"
    echo "  roadmap-events       : Show roadmap"
    echo "  daily-log-thinking   : Run daily analysis manually"
    echo "  show-latest-*        : View latest results"
    echo "  tail-latest-log      : View latest technical log"
    echo "  summary              : View system summary"
    echo "  menu                 : Interactive menu"
    ;;

  sanity)
    bash "$SCRIPT_DIR/deepseek_student_sanity_check.sh"
    ;;
    
  run)
    # Delegate to Hub but wrap slightly if needed, or just call directly
    if [ -x "$DEEPSEEK_HUB_CMD" ]; then
        shift
        bash "$DEEPSEEK_HUB_CMD" "${@:-status}"
    else
        echo "Error: DeepSeek Hub script not executable or found."
        exit 1
    fi
    ;;
    
  run-logged)
    shift
    bash "$SCRIPT_DIR/deepseek_student_run_logged.sh" "$@"
    ;;

  think)
    shift
    bash "$SCRIPT_DIR/deepseek_student_run_logged.sh" think "$@"
    ;;

  response)
    shift
    bash "$SCRIPT_DIR/deepseek_student_run_logged.sh" response "$@"
    ;;

  roadmap-events)
    shift
    bash "$SCRIPT_DIR/deepseek_student_run_logged.sh" roadmap_events "$@"
    ;;

  roadmap-think-module)
    shift
    bash "$SCRIPT_DIR/deepseek_student_run_logged.sh" roadmap_think_module "$@"
    ;;

  roadmap-response-module)
    shift
    bash "$SCRIPT_DIR/deepseek_student_run_logged.sh" roadmap_response_module "$@"
    ;;

  models)
    bash "$SCRIPT_DIR/deepseek_student_run_logged.sh" models
    ;;

  tail-latest-log)
    bash "$SCRIPT_DIR/deepseek_student_tail_latest_log.sh"
    ;;
    
  explain)
    echo "DeepSeek Student Wrapper"
    echo "Provides SSH-friendly access to DeepSeek tools."
    echo "Commands: status, sanity, run, run-logged, think, response, roadmap-*, tail-latest-log."
    ;;
    
  *)
    echo "Usage: deepseek_student_cmd.sh status|sanity|run|run-logged|think|response|roadmap-events|roadmap-think-module|roadmap-response-module|models|tail-latest-log|summary|explain|show-latest-*|daily-log-thinking|install-daily-timer|timer-status|timer-logs|show-paths|help"
    exit 1
    ;;
esac
