# 20_UPDATED_OPERATOR_SCRIPT

## Guard integre

``bash
# --- PREFLIGHT : TTY size guard ---
_STTY_BEFORE="$(stty size 2>/dev/null || echo 'no-stty')"
if [ -t 1 ]; then
  _STTY_COLS="$(echo "$_STTY_BEFORE" | awk '{print $2}')"
  _STTY_ROWS="$(echo "$_STTY_BEFORE" | awk '{print $1}')"
  if [ "${_STTY_COLS:-0}" = "0" ] || [ "${_STTY_ROWS:-0}" = "0" ]; then
    stty rows 50 cols 200 2>/dev/null || true
  fi
fi
_STTY_AFTER="$(stty size 2>/dev/null || echo 'no-stty')"
echo "STTY_BEFORE=$_STTY_BEFORE"
echo "STTY_AFTER=$_STTY_AFTER"
# --- END PREFLIGHT ---
``