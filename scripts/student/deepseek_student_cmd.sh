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
    echo "=== DEEPSEEK STUDENT STATUS ==="
    echo "Repo Root:    $ROOT_DIR"
    echo "Host:         $(hostname)"
    echo "Date:         $(date -u)"
    
    if [ -f "$DEEPSEEK_HUB_CMD" ]; then
        echo "DeepSeek Hub: FOUND"
        if [ -x "$DEEPSEEK_HUB_CMD" ]; then
             echo "Hub Script:   EXECUTABLE"
        else
             echo "Hub Script:   NOT EXECUTABLE (Run sanity check)"
        fi
    else
        echo "DeepSeek Hub: MISSING"
    fi

    # Check Logs
    LOGS_DIR="$ROOT_DIR/data/logs/deepseek_student"
    if [ -d "$LOGS_DIR" ]; then
        echo "Logs Dir:     EXISTS"
    else
        echo "Logs Dir:     MISSING (Will be created)"
    fi
    
    echo "Summary:      DeepSeek Student pack ready."
    echo "================================"
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
    echo "Usage: deepseek_student_cmd.sh status|sanity|run|run-logged|think|response|roadmap-events|roadmap-think-module|roadmap-response-module|models|tail-latest-log|summary|explain"
    exit 1
    ;;
esac
