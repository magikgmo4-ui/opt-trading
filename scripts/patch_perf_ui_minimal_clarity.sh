#!/usr/bin/env bash
set -euo pipefail

APP="/opt/trading/perf/perf_app.py"
[ -f "$APP" ] || { echo "ERR: $APP not found"; exit 1; }

TS="$(date +%Y%m%d_%H%M%S)"
BAK="${APP}.bak.${TS}"

echo "[1/6] Backup -> $BAK"
cp -a "$APP" "$BAK"

echo "[2/6] Inject minimal clarity CSS (append-only, safe)..."
python - <<'PY'
import re, pathlib, sys
p = pathlib.Path("/opt/trading/perf/perf_app.py")
s = p.read_text(encoding="utf-8")

m = re.search(r"<style>(.*?)</style>", s, re.S)
if not m:
    print("ERR: No <style> block found", file=sys.stderr)
    sys.exit(1)

css = m.group(1)

# Remove previous patch block if present
css = re.sub(r"/\*\s*MINIMAL_CLARITY_PATCH\s*\*/.*?/\\*\s*END_MINIMAL_CLARITY_PATCH\s*\\*/\s*",
             "", css, flags=re.S)

PATCH = r"""
/* MINIMAL_CLARITY_PATCH */
:root{ --fg:#f3f6fb; --muted:#b7c2d3; --line:rgba(255,255,255,.14); }
body{ font-size:13px; line-height:1.45; text-rendering:optimizeLegibility; }
.card h2{ color:var(--muted); font-weight:700; letter-spacing:.2px; }
.kpi .label{ color:var(--muted); font-size:12px; }
.kpi .val{ font-size:17px; font-weight:800; }
table{ font-size:13px; }
th{ color:#d8e2f2; font-weight:700; background:rgba(255,255,255,.03); }
td,th{ padding:8px 10px; }
pre, code{ font-size:12px; }
/* END_MINIMAL_CLARITY_PATCH */
"""

css2 = css.rstrip() + "\n\n" + PATCH.strip() + "\n"
s2 = s[:m.start(1)] + css2 + s[m.end(1):]
p.write_text(s2, encoding="utf-8")
print("OK: minimal clarity CSS appended safely")
PY

echo "[3/6] py_compile..."
python -m py_compile /opt/trading/perf/perf_app.py

echo "[4/6] restart tv-perf..."
sudo systemctl restart tv-perf.service

echo "[5/6] wait perf up..."
for i in {1..40}; do
  curl -fsS http://127.0.0.1:8010/perf/summary >/dev/null && echo "OK: perf up" && break
  sleep 0.2
done

echo "[6/6] UI smoke (GET)..."
curl -fsS http://127.0.0.1:8010/perf/ui | head -n 5

echo "DONE. Backup: $BAK"
