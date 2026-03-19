#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student - Run Logged
# Executes DeepSeek command and captures output to a log file

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

LOGS_DIR="$ROOT_DIR/data/logs/deepseek_student"
mkdir -p "$LOGS_DIR"

TIMESTAMP=$(date -u +"%Y%m%d_%H%M%S")
DEFAULT_MODEL="deepseek-r1:1.5b"

# --- Argument Parsing & Injection ---

# If no args, default to status
if [ $# -eq 0 ]; then
    ARGS=("status")
    CMD_NAME="status"

else
    CMD_NAME="${1}"
    shift
    
    # Logic to inject model if missing for specific commands
    # NOTE: deepseek_hub_cmd.sh expects: CMD [MODEL] [ARG1] [ARG2]
    # For many commands, MODEL is the 2nd argument (index 1 in 0-based, or $2 in script)
    
    case "$CMD_NAME" in
        think|response)
            # Hub expects: think [model] <sujet>
            # If 1 arg -> inject default model
            if [ $# -eq 1 ]; then
                ARGS=("$CMD_NAME" "$DEFAULT_MODEL" "$1")
            else
                ARGS=("$CMD_NAME" "$@")
            fi
            ;;
            
        roadmap_events)
            # Hub expects: roadmap_events [model] [N]
            # If 0 args -> inject default model
            if [ $# -eq 0 ]; then
                ARGS=("$CMD_NAME" "$DEFAULT_MODEL")
            # If 1 arg and it looks like a number -> inject default model before it
            elif [ $# -eq 1 ] && [[ "$1" =~ ^[0-9]+$ ]]; then
                ARGS=("$CMD_NAME" "$DEFAULT_MODEL" "$1")
            else
                ARGS=("$CMD_NAME" "$@")
            fi
            ;;
            
        roadmap_think_module|roadmap_response_module)
            # Hub expects: roadmap_think_module [model] <module> [N]
            # If 1 arg (module) -> inject default model
            if [ $# -eq 1 ]; then
                ARGS=("$CMD_NAME" "$DEFAULT_MODEL" "$1")
            # If 2 args and 2nd is number -> inject default model
            elif [ $# -eq 2 ] && [[ "$2" =~ ^[0-9]+$ ]]; then
                ARGS=("$CMD_NAME" "$DEFAULT_MODEL" "$1" "$2")
            else
                ARGS=("$CMD_NAME" "$@")
            fi
            ;;
            
        *)
            # For other commands (status, models, etc), pass as is
            ARGS=("$CMD_NAME" "$@")
            ;;
    esac
fi

# --- Execution ---

RUN_ID="deepseek_${CMD_NAME}_${TIMESTAMP}"
LOG_FILE="$LOGS_DIR/${RUN_ID}.log"
LATEST_LINK="$LOGS_DIR/latest.log"

# IMPORTANT: Point to the actual hub script, but ensure it's executable.
# If installed via shortcuts, we might want to use the global wrapper if available,
# but using the direct path is safer for standalone pack usage.
DEEPSEEK_HUB_CMD="$ROOT_DIR/modules/deepseek_hub/scripts/deepseek_hub_cmd.sh"

echo "=== DeepSeek Student Run (Logged) ==="
echo "Command: ${ARGS[*]}"
echo "Run ID:  $RUN_ID"
echo "Log:     $LOG_FILE"
echo "Start:   $(date -u)"
echo "----------------------------------------"

if [ ! -f "$DEEPSEEK_HUB_CMD" ]; then
    echo "Error: DeepSeek Hub script not found at: $DEEPSEEK_HUB_CMD"
    exit 1
fi

# Ensure wrappers used by hub are in PATH if needed, OR rely on hub script logic.
# The hub script calls `cmd-deepseek_thinking`, `cmd-deepseek_response`, `cmd-deepseek_student`.
# We need to make sure these are available or that the hub script finds them.
# Given install_shortcuts.sh, these are likely in /usr/local/bin.
# If not, we might fail. 
# BUT: deepseek_hub_cmd.sh uses `cmd-deepseek_thinking` directly.
# Let's check if they exist.

if ! command -v cmd-deepseek_thinking >/dev/null 2>&1; then
    # Fallback: add module scripts to PATH temporarily if possible, 
    # or warn user that shortcuts are missing.
    # We will try to add potential locations to PATH.
    export PATH="$PATH:$ROOT_DIR/modules/deepseek_thinking/scripts:$ROOT_DIR/modules/deepseek_response/scripts:$ROOT_DIR/modules/deepseek_student/scripts"
fi

# Run and capture output (tee)
# We invoke bash explicitly to avoid permission issues if +x is missing
if bash "$DEEPSEEK_HUB_CMD" "${ARGS[@]}" 2>&1 | tee "$LOG_FILE"; then
    STATUS="SUCCESS"
else
    STATUS="FAILED"
fi

echo "----------------------------------------"
echo "End:     $(date -u)"
echo "Status:  $STATUS"

# Update latest link
rm -f "$LATEST_LINK"
ln -s "$LOG_FILE" "$LATEST_LINK"

echo "Log saved to: $LOG_FILE"
echo "Latest log linked at: $LATEST_LINK"

exit 0
