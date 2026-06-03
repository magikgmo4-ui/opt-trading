#!/usr/bin/env bash
set -euo pipefail

SCRIPT="$(dirname "${BASH_SOURCE[0]}")/sanity_check.sh"
case "${1:-}" in
    sanity|check|test)
        exec bash "$SCRIPT"
        ;;
    "")
        echo "telegram_command_center — Command Center UX"
        echo ""
        echo "Commands:"
        echo "  sanity    Run sanity checks"
        echo "  env       Show required env vars"
        echo ""
        ;;
    env)
        echo "TELEGRAM_BOT_TOKEN"
        echo "TELEGRAM_CHAT_ID_ALERTS"
        echo "TELEGRAM_CHAT_ID_PIPELINE"
        echo "TELEGRAM_CHAT_ID_PUSH"
        echo "TELEGRAM_CHAT_ID_OPS"
        ;;
    *)
        echo "Unknown: $1"
        exit 2
        ;;
esac
