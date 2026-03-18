#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student - Install Daily Timer
# Installs a user-level systemd timer for daily log analysis

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

SERVICE_NAME="deepseek_student_daily_log_thinking"
USER_SYSTEMD_DIR="$HOME/.config/systemd/user"
mkdir -p "$USER_SYSTEMD_DIR"

echo "=== Installing DeepSeek Daily Timer ==="
echo "Target: $USER_SYSTEMD_DIR"

# 1. Create Service File
cat > "$USER_SYSTEMD_DIR/$SERVICE_NAME.service" <<EOF
[Unit]
Description=DeepSeek Student Daily Log Thinking
Wants=$SERVICE_NAME.timer

[Service]
Type=oneshot
ExecStart=$SCRIPT_DIR/deepseek_student_daily_log_thinking.sh
WorkingDirectory=$ROOT_DIR
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
EOF

# 2. Create Timer File (Run daily at 06:30)
cat > "$USER_SYSTEMD_DIR/$SERVICE_NAME.timer" <<EOF
[Unit]
Description=Run DeepSeek Student Daily Log Thinking at 06:30
Requires=$SERVICE_NAME.service

[Timer]
OnCalendar=*-*-* 06:30:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

# 3. Enable and Start
echo "Reloading systemd user daemon..."
systemctl --user daemon-reload
echo "Enabling timer..."
systemctl --user enable --now "$SERVICE_NAME.timer"

echo "Status:"
systemctl --user list-timers --all | grep "$SERVICE_NAME" || echo "Timer not found (check logs)"

echo "--------------------------------"
echo "To run manually: systemctl --user start $SERVICE_NAME.service"
echo "To view logs:    journalctl --user -u $SERVICE_NAME.service"
echo "Installation complete."
