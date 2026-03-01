#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%Y%m%d_%H%M%S)"
OUT="/tmp/ui_diag_${TS}"
mkdir -p "$OUT"

echo "[ui_diag] writing to: $OUT"

# system basics
uname -a > "$OUT/uname.txt" 2>&1 || true
date --iso-8601=seconds > "$OUT/date.txt" 2>&1 || true
whoami > "$OUT/whoami.txt" 2>&1 || true
pwd > "$OUT/pwd.txt" 2>&1 || true
hostnamectl > "$OUT/hostnamectl.txt" 2>&1 || true
ip -br a > "$OUT/ip.txt" 2>&1 || true

# processes / ports
ss -ltnp > "$OUT/ss_ltnp.txt" 2>&1 || true
ps auxww > "$OUT/ps_auxww.txt" 2>&1 || true

# systemd
systemctl --failed > "$OUT/systemctl_failed.txt" 2>&1 || true
systemctl list-units --type=service --no-pager > "$OUT/systemctl_services.txt" 2>&1 || true
systemctl list-units --type=service --no-pager | egrep -i "desk|toolbox|perf|tv-|uvicorn|fastapi|gunicorn|nginx|caddy" > "$OUT/services_filtered.txt" 2>&1 || true

# service logs for candidates
while read -r s; do
  [[ -z "$s" ]] && continue
  [[ "$s" != *.service ]] && continue
  systemctl status "$s" --no-pager > "$OUT/status_${s}.txt" 2>&1 || true
  journalctl -u "$s" --since "today" --no-pager > "$OUT/journal_${s}.txt" 2>&1 || true
done < <(awk '{print $1}' "$OUT/services_filtered.txt" 2>/dev/null || true)

# app discovery
if [[ -d /opt/trading ]]; then
  find /opt/trading -maxdepth 5 -type f \( -name "*.service" -o -name "app.py" -o -name "main.py" -o -name "*_app.py" -o -name "pyproject.toml" -o -name "requirements.txt" \) \
    > "$OUT/find_apps.txt" 2>&1 || true

  grep -RIn --exclude-dir=.git --exclude="*.tgz" --exclude="*.zip" -E \
    "uvicorn|gunicorn|0\.0\.0\.0|127\.0\.0\.1|/ui\b|/toolbox\b|/perf\b|add_api_route|FastAPI\(" \
    /opt/trading 2>/dev/null | head -n 600 > "$OUT/grep_endpoints.txt" || true
fi

# curl tests on common ports
PORTS=(8000 8010 8020 8030 8040 8080 8100 8501)
PATHS=("/" "/health" "/ui" "/toolbox/ui" "/perf/ui" "/perf/summary" "/docs" "/openapi.json")

for port in "${PORTS[@]}"; do
  for path in "${PATHS[@]}"; do
    f="$OUT/curl_${port}$(echo "$path" | tr '/' '_' | tr -cd '[:alnum:]_').txt"
    curl -sS -m 3 -o /dev/null -D "$f" "http://127.0.0.1:${port}${path}" || true
  done
done

# pack
TGZ="/tmp/ui_diag_${TS}.tgz"
tar -czf "$TGZ" -C /tmp "ui_diag_${TS}"
echo
echo "[ui_diag] OK: packed -> $TGZ"
echo "[ui_diag] Quick peek:"
echo "  - $OUT/services_filtered.txt"
echo "  - $OUT/systemctl_failed.txt"
echo "  - $OUT/ss_ltnp.txt"
