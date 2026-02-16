#!/usr/bin/env bash
set -euo pipefail

APP="/opt/trading/perf/perf_app.py"

if [ ! -f "$APP" ]; then
  echo "ERR: $APP not found"
  exit 1
fi

TS="$(date +%Y%m%d_%H%M%S)"
BAK="$APP.bak.${TS}"

echo "[1/6] Backup -> $BAK"
cp -a "$APP" "$BAK"

echo "[2/6] Patch <style> block (clean 17in square) ..."
python - <<'PY'
import re, pathlib, sys

p = pathlib.Path("/opt/trading/perf/perf_app.py")
s = p.read_text(encoding="utf-8")

m = re.search(r"<style>(.*?)</style>", s, re.S)
if not m:
    print("ERR: No <style>...</style> block found", file=sys.stderr)
    sys.exit(1)

CSS = """
:root{
  --bg:#0b0d10; --fg:#e8eef7; --muted:#a6b2c2; --card:#121723;
  --line:rgba(255,255,255,.10); --chip:rgba(255,255,255,.08);
  --accent:rgba(99,102,241,.28);
  --ok:#2dd4bf; --bad:#fb7185; --warn:#fbbf24;
}
*{ box-sizing:border-box; }
html,body{ height:100%; }
body{
  margin:14px;
  background:var(--bg);
  color:var(--fg);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
}
a{ color:inherit; text-decoration:none; }

.topbar{
  position:sticky; top:0;
  background:linear-gradient(to bottom, rgba(11,13,16,.92), rgba(11,13,16,.70));
  backdrop-filter: blur(6px);
  border:1px solid var(--line);
  border-radius:16px;
  padding:12px;
  margin-bottom:12px;
  display:flex; align-items:flex-start; justify-content:space-between; gap:12px;
  z-index:50;
}
.title{ display:flex; flex-direction:column; gap:4px; }
.title h1{ margin:0; font-size:18px; letter-spacing:.2px; }
.subtitle{ color:var(--muted); font-size:12px; }
.actions{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; justify-content:flex-end; }

.card{
  background:var(--card);
  border:1px solid var(--line);
  border-radius:16px;
  padding:12px;
  box-shadow: 0 1px 0 rgba(0,0,0,.35);
  overflow:hidden;
  min-width:0;
}
.card h2{
  margin:0 0 10px;
  font-size:12px;
  color:var(--muted);
  font-weight:700;
  letter-spacing:.18px;
  text-transform:uppercase;
}

.grid{ display:grid; grid-template-columns:repeat(12, minmax(0,1fr)); gap:12px; align-items:start; }
.row{ display:grid; grid-template-columns:repeat(12, minmax(0,1fr)); gap:12px; align-items:start; }

.kpis{ display:grid; grid-template-columns:repeat(4, minmax(0,1fr)); gap:10px; }
.kpi{
  background:rgba(15,19,32,.70);
  border:1px solid var(--line);
  border-radius:14px;
  padding:10px;
  min-width:0;
}
.kpi .label{ color:var(--muted); font-size:11px; }
.kpi .val{ font-size:15px; margin-top:6px; font-weight:800; letter-spacing:.2px; }

.chip{
  display:inline-flex; align-items:center; gap:7px;
  padding:6px 10px;
  border-radius:999px;
  border:1px solid var(--line);
  background:var(--chip);
  font-size:12px;
  color:var(--muted);
}
.dot{ width:8px; height:8px; border-radius:50%; background:var(--muted); display:inline-block; }
.dot.ok{ background:var(--ok); } .dot.bad{ background:var(--bad); } .dot.warn{ background:var(--warn); }

input, button, select{
  padding:8px 10px;
  border-radius:12px;
  border:1px solid var(--line);
  background:rgba(15,19,32,.85);
  color:var(--fg);
}
button{ cursor:pointer; }
button.primary{ background:var(--accent); border-color:rgba(99,102,241,.45); }
button.ghost{ background:transparent; }

table{ width:100%; border-collapse:collapse; font-size:12px; }
th,td{ border-bottom:1px solid rgba(255,255,255,.08); padding:8px 10px; text-align:left; vertical-align:top; }
th{ color:var(--muted); font-weight:700; }
tr:hover td{ background:rgba(255,255,255,.03); }

pre, code, .mono, .json, #rawSummary, #raw_summary, #raw{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
}
pre, #rawSummary, #raw_summary, #raw{
  background:rgba(0,0,0,.22);
  border:1px solid rgba(255,255,255,.08);
  border-radius:14px;
  padding:10px;
  max-height:240px;
  overflow:auto;
  white-space:pre;
}

@media (max-width: 1280px){ .kpis{ grid-template-columns:repeat(2, minmax(0,1fr)); } }
@media (max-width: 980px){
  body{ margin:10px; }
  .topbar{ position:static; }
  .grid, .row{ grid-template-columns:1fr; }
  .kpis{ grid-template-columns:repeat(2, minmax(0,1fr)); }
}

/* === FIX: prevent overlap === */
.grid, .row{
  display:grid !important;
  grid-template-columns:repeat(12, minmax(0, 1fr)) !important;
  gap:12px !important;
  align-items:start !important;
}
.card{
  position:relative !important;
  z-index:1 !important;
  overflow:hidden !important;
  min-height:0 !important;
}
pre, .mono, .json, #rawSummary, #raw_summary, #raw{
  max-height:240px !important;
  overflow:auto !important;
  white-space:pre !important;
}
""".strip("\n")

# anti "collage terminal dans CSS"
for bad in ("curl ", "sudo ", "systemctl ", "head -n", "echo ", "apt-get "):
    if bad in CSS:
        raise SystemExit(f"Refusing: CSS contains '{bad}'")

s2 = s[:m.start(1)] + "\n" + CSS + "\n" + s[m.end(1):]
p.write_text(s2, encoding="utf-8")
print("OK: <style> block replaced safely")
PY

echo "[3/6] py_compile..."
python -m py_compile /opt/trading/perf/perf_app.py

echo "[4/6] restart service..."
sudo systemctl restart tv-perf.service

echo "[5/6] wait until /perf/summary responds..."
for i in {1..40}; do
  curl -fsS http://127.0.0.1:8010/perf/summary >/dev/null && echo "OK: perf up" && break
  sleep 0.2
done

echo "[6/6] UI smoke (GET /perf/ui)..."
curl -fsS http://127.0.0.1:8010/perf/ui | head -n 5

echo "DONE. Backup saved at: $BAK"
