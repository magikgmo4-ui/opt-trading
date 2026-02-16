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

echo "[2/6] Inject minimal UI polish (zebra + num align + OPEN/CLOSED chips) ..."
python - <<'PY'
import re, pathlib, sys

p = pathlib.Path("/opt/trading/perf/perf_app.py")
s = p.read_text(encoding="utf-8")

# ---- CSS inject (append before </style>) ----
m = re.search(r"</style>", s, re.I)
if not m:
    print("ERR: </style> not found", file=sys.stderr)
    sys.exit(1)

CSS_MARK = "/* === MIN_POLISH_V1 === */"
CSS_BLOCK = r"""
/* === MIN_POLISH_V1 === */
/* Zebra rows + hover */
table.tvpolish tbody tr:nth-child(odd){ background: rgba(255,255,255,.02); }
table.tvpolish tbody tr:hover{ background: rgba(99,102,241,.06); }

/* Numeric alignment */
table.tvpolish td.num, table.tvpolish th.num{
  text-align:right !important;
  font-variant-numeric: tabular-nums;
}

/* Status chips */
.status-chip{
  display:inline-flex;
  align-items:center;
  gap:6px;
  padding:2px 10px;
  border-radius:999px;
  border:1px solid rgba(255,255,255,.14);
  background: rgba(255,255,255,.06);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .2px;
}
.status-chip::before{
  content:"";
  width:8px; height:8px;
  border-radius:50%;
  display:inline-block;
  background: rgba(255,255,255,.35);
}
.status-chip.open{
  border-color: rgba(45,212,191,.35);
  background: rgba(45,212,191,.10);
}
.status-chip.open::before{ background: rgba(45,212,191,.95); }
.status-chip.closed{
  border-color: rgba(148,163,184,.25);
  background: rgba(148,163,184,.08);
}
.status-chip.closed::before{ background: rgba(148,163,184,.75); }
"""
if CSS_MARK not in s:
    s = s[:m.start()] + "\n" + CSS_BLOCK.strip() + "\n\n" + s[m.start():]

# ---- JS inject (before </body>) ----
b = re.search(r"</body>", s, re.I)
if not b:
    print("ERR: </body> not found", file=sys.stderr)
    sys.exit(1)

JS_MARK = "/* MIN_POLISH_V1 */"
JS_BLOCK = r"""
<script id="min-polish-v1">
/* MIN_POLISH_V1 */
(function(){
  function isNumericLike(t){
    if(!t) return false;
    t = t.replace(/\u00A0/g,' ').trim();           // nbsp
    if(!t) return false;
    // allow % , decimals, minus, thousands separators
    // examples: 5038.5, -12.0, 1,234.50, 100.0%, 0.9100
    const x = t.replace(/[, ]/g,'').replace(/%$/,'');
    return /^-?\d+(\.\d+)?$/.test(x);
  }

  function polishOneTable(table){
    if(!table) return;
    table.classList.add("tvpolish");

    // mark header numeric based on first body row sample
    const rows = table.tBodies && table.tBodies[0] ? Array.from(table.tBodies[0].rows) : [];
    const head = table.tHead && table.tHead.rows && table.tHead.rows[0] ? table.tHead.rows[0] : null;

    // zebra is pure CSS; here we do numeric+status
    rows.forEach(tr=>{
      Array.from(tr.cells).forEach((td, idx)=>{
        const raw = (td.textContent || "").trim();

        // status chip (OPEN/CLOSED)
        if(raw === "OPEN" || raw === "CLOSED"){
          const cls = raw.toLowerCase();
          // avoid double-wrapping
          if(!td.querySelector(".status-chip")){
            td.innerHTML = '<span class="status-chip '+cls+'">'+raw+'</span>';
          }
        }

        // numeric right-align
        if(isNumericLike(raw)){
          td.classList.add("num");
          if(head && head.cells && head.cells[idx]) head.cells[idx].classList.add("num");
        }
      });
    });
  }

  function run(){
    document.querySelectorAll("table").forEach(polishOneTable);
  }

  window.addEventListener("load", ()=>{ setTimeout(run, 200); });
  setInterval(run, 1200);
})();
</script>
"""
if JS_MARK not in s:
    s = s[:b.start()] + "\n" + JS_BLOCK.strip() + "\n" + s[b.start():]

p.write_text(s, encoding="utf-8")
print("OK: injected MIN_POLISH_V1 (CSS+JS) safely")
PY

echo "[3/6] py_compile..."
python -m py_compile "$APP"

echo "[4/6] restart tv-perf..."
sudo systemctl restart tv-perf.service

echo "[5/6] wait until /perf/summary responds..."
for i in {1..30}; do
  curl -fsS http://127.0.0.1:8010/perf/summary >/dev/null && echo "OK: perf up" && break
  sleep 0.2
done

echo "[6/6] UI smoke (GET /perf/ui)..."
curl -fsS http://127.0.0.1:8010/perf/ui | head -n 5

echo "DONE. Backup saved at: $BAK"
