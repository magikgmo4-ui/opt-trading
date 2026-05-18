from __future__ import annotations

def render_ui_html() -> str:
    return r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Desk Pro</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Arial,sans-serif;margin:20px;max-width:1100px}
    h1{margin:0 0 6px 0}
    .muted{color:#666;font-size:13px}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
    .card{border:1px solid #ddd;border-radius:10px;padding:14px}
    table{width:100%;border-collapse:collapse;font-size:13px}
    th,td{border-bottom:1px solid #eee;padding:6px 6px;text-align:left;vertical-align:top}
    input,select,textarea{width:100%;padding:8px;border:1px solid #ccc;border-radius:8px;font-size:14px}
    button{padding:10px 12px;border:1px solid #333;border-radius:10px;background:#111;color:#fff;cursor:pointer}
    button:disabled{opacity:.5;cursor:not-allowed}
    .row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
    pre{background:#0b0b0b;color:#e8e8e8;padding:10px;border-radius:10px;overflow:auto;font-size:12px}
    .pill{display:inline-block;padding:2px 8px;border:1px solid #ddd;border-radius:999px;font-size:12px;margin-right:6px}
  </style>
</head>
<body>
  <h1>Desk Pro</h1>
  <div class="muted">
    Endpoints: <span class="pill">/desk/health</span><span class="pill">/desk/snapshot</span><span class="pill">/desk/form</span>
  </div>

  <div class="grid">
    <div class="card">
      <h3 style="margin-top:0">Pipeline Status</h3>
      <div class="muted">Live from /desk/status</div>
      <div id="pipelineSummary"></div>
      <div style="margin-top:8px">
        <button id="btnStatus">Refresh</button>
        <span id="statusTs" class="muted" style="margin-left:8px"></span>
      </div>
      <details style="margin-top:6px">
        <summary class="muted" style="cursor:pointer">Raw JSON</summary>
        <pre id="pipelineStatus" style="font-size:11px">loading...</pre>
      </details>
    </div>

    <div class="card">
      <h3 style="margin-top:0">Snapshot</h3>
      <div class="muted">Refresh loads /desk/snapshot</div>
      <p><button id="btnSnap">Refresh</button></p>
      <table id="snapTable">
        <thead><tr><th>source</th><th>asset</th><th>metric</th><th>value</th><th>unit</th><th>window</th><th>notes</th></tr></thead>
        <tbody></tbody>
      </table>
      <p class="muted" id="snapMeta"></p>
    </div>

    <div class="card">
      <h3 style="margin-top:0">Formulaire → Probabilité</h3>

      <div class="row">
        <div>
          <label>Symbol</label>
          <input id="symbol" value="BTC" />
        </div>
        <div>
          <label>Bias</label>
          <select id="bias">
            <option value="neutral">neutral</option>
            <option value="bull">bull</option>
            <option value="bear">bear</option>
          </select>
        </div>
      </div>

      <div class="row" style="margin-top:10px">
        <div>
          <label>Vol regime</label>
          <select id="vol">
            <option value="normal">normal</option>
            <option value="low">low</option>
            <option value="high">high</option>
          </select>
        </div>
        <div>
          <label>Fear & Greed (0-100)</label>
          <input id="fg" type="number" min="0" max="100" value="42" />
        </div>
      </div>

      <div class="row" style="margin-top:10px">
        <div>
          <label>ETF flow</label>
          <select id="etf">
            <option value="">(none)</option>
            <option value="in">in</option>
            <option value="out">out</option>
            <option value="flat">flat</option>
          </select>
        </div>
        <div>
          <label>Onchain flow</label>
          <select id="onchain">
            <option value="">(none)</option>
            <option value="in">in</option>
            <option value="out">out</option>
            <option value="flat">flat</option>
          </select>
        </div>
      </div>

      <div class="row" style="margin-top:10px">
        <div>
          <label>Futures flow</label>
          <select id="fut">
            <option value="">(none)</option>
            <option value="in">in</option>
            <option value="out">out</option>
            <option value="flat">flat</option>
          </select>
        </div>
        <div>
          <label>Funding</label>
          <select id="funding">
            <option value="">(none)</option>
            <option value="pos">pos</option>
            <option value="neg">neg</option>
            <option value="flat">flat</option>
          </select>
        </div>
      </div>

      <div class="row" style="margin-top:10px">
        <div>
          <label>DXY trend</label>
          <select id="dxy">
            <option value="">(none)</option>
            <option value="up">up</option>
            <option value="down">down</option>
            <option value="flat">flat</option>
          </select>
        </div>
        <div>
          <label>Corr XAU/BTC (-1..1)</label>
          <input id="corr" type="number" step="0.01" min="-1" max="1" value="0.35" />
        </div>
      </div>

      <div style="margin-top:10px">
        <label>Supports/Resistances (JSON) — Weekly/Daily</label>
        <textarea id="sr" rows="5">[
  {"tf":"W","kind":"S","level":67900,"label":"W support"},
  {"tf":"D","kind":"R","level":69000,"label":"D resistance"}
]</textarea>
        <div class="muted">Format: [{"tf":"W|D","kind":"S|R","level":float,"label":str?,"confidence":0..1?}]</div>
      </div>

      <p style="margin-top:10px"><button id="btnSubmit">Calculer</button></p>
      <div class="muted">Résultat:</div>
      <pre id="out">{}</pre>
    </div>
  </div>

<script>
const el = (id)=>document.getElementById(id);

function healthBadge(status){
  const colors = {'healthy':'#2e7d32','degraded':'#e65100','down':'#c62828'};
  const bg = colors[status]||'#888';
  return `<span style="display:inline-block;padding:2px 12px;border-radius:999px;background:${bg};color:#fff;font-size:13px;font-weight:600">${status.toUpperCase()}</span>`;
}

function badge(ok, label, labelFail){
  const good = ok === true || ok === 'live' || ok === 'fixture' || ok === 'pass';
  const warn = ok === 'warn';
  const color = warn ? '#e65100' : (good ? '#2e7d32' : '#c62828');
  const text = warn ? 'WARN' : (good ? (label||'OK') : (labelFail||'DOWN'));
  return `<span style="display:inline-block;padding:1px 8px;border-radius:999px;background:${color};color:#fff;font-size:11px;margin:1px 0">${text}</span>`;
}

async function refreshStatus(){
  try{
    const r = await fetch('/desk/status');
    const j = await r.json();
    el('pipelineStatus').textContent = JSON.stringify(j, null, 2);

    let html = '';

    // Health badge
    const h = j.health || {};
    html += '<div style="margin-bottom:8px;display:flex;align-items:center;gap:8px">';
    html += healthBadge(h.status||'unknown');
    html += '<span class="muted">' + (h.checks||[]).length + ' checks</span>';
    html += '</div>';

    // Checks table
    html += '<table style="font-size:12px;margin-bottom:8px">';
    html += '<thead><tr><th>check</th><th>status</th><th>reason</th></tr></thead><tbody>';
    if(h.checks){
      for(const c of h.checks){
        html += `<tr><td>${c.check}</td><td>${badge(c.status, c.status, c.status)}</td><td>${c.reason||''}</td></tr>`;
      }
    }
    html += '</tbody></table>';

    // 3-col component cards
    html += '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;font-size:12px">';

    // Desk Pro
    html += '<div style="border:1px solid #ddd;border-radius:6px;padding:6px">';
    html += '<strong>Desk Pro</strong><br>';
    html += 'Mode: ' + (j.desk_pro?.mode||'?') + '<br>';
    html += badge(j.desk_pro?.ok, 'up', 'down');
    html += '</div>';

    // Webhook
    html += '<div style="border:1px solid #ddd;border-radius:6px;padding:6px">';
    html += '<strong>Webhook</strong><br>';
    if(j.webhook){
      html += 'Engine: ' + (j.webhook.active_engine||'-') + '<br>';
      html += 'Trade: ' + (j.webhook.trade_allowed ? 'ALLOWED' : 'BLOCKED') + '<br>';
      html += badge(j.webhook.ok, 'up', 'down');
    } else {
      html += badge(false, '', 'unreachable');
    }
    html += '</div>';

    // Perf
    html += '<div style="border:1px solid #ddd;border-radius:6px;padding:6px">';
    html += '<strong>Perf</strong><br>';
    if(j.perf){
      html += 'Trades: ' + (j.perf.total_trades||0) + '<br>';
      html += 'PnL: ' + (j.perf.pnl_realized||0) + '<br>';
      const pct = ((j.perf.equity_last||0) / (j.perf.equity0||1) * 100 - 100).toFixed(1);
      html += 'Return: ' + (j.perf.pnl_realized >= 0 ? '+' : '') + pct + '%<br>';
      html += badge(true, 'live', '');
    } else {
      html += badge(false, '', 'down');
    }
    html += '</div>';

    // Sources row
    html += '</div>';
    html += '<div style="margin-top:6px;font-size:12px"><strong>Sources:</strong> ';
    if(j.sources){
      for(const [k,v] of Object.entries(j.sources)){
        html += `<span class="pill">${k}=${v}</span>`;
      }
    }
    html += '</div>';

    // Alert status
    if(j.alert){
      const a = j.alert;
      if(a.triggered){
        html += '<div style="margin-top:6px;font-size:12px;padding:4px 8px;border-radius:6px;background:#fff3e0;border:1px solid #e65100">';
        html += '<strong>ALERT:</strong> status=' + a.status + ' cooldown=' + a.cooldown_sec + 's';
        html += '</div>';
      } else if(a.reason === 'cooldown'){
        html += '<div style="margin-top:6px;font-size:12px;color:#888">';
        html += 'Alert cooldown: ' + a.cooldown_remaining_sec + 's remaining (last: ' + (a.last_status||'?') + ')';
        html += '</div>';
      }
    }

    // Errors
    if(j.error_count > 0){
      html += '<div style="margin-top:6px;font-size:12px;color:#c62828">';
      html += '<strong>Errors:</strong> ' + j.error_count + ' total, last: ';
      if(j.recent_errors && j.recent_errors.length > 0){
        html += j.recent_errors[0].error || 'unknown';
      }
      html += '</div>';
    }

    el('pipelineSummary').innerHTML = html;
    el('statusTs').textContent = 'updated ' + (j.ts||'');
  }catch(e){
    el('pipelineStatus').textContent = 'ERROR: '+e;
    el('pipelineSummary').innerHTML = '<span style="color:#c62828">Pipeline unreachable: '+e+'</span>';
  }
}

async function refreshSnap(){
  el('btnSnap').disabled = true;
  try{
    const r = await fetch('/desk/snapshot');
    const j = await r.json();
    const tb = el('snapTable').querySelector('tbody');
    tb.innerHTML = '';
    (j.metrics||[]).forEach(m=>{
      const tr=document.createElement('tr');
      tr.innerHTML = `<td>${m.source}</td><td>${m.asset}</td><td>${m.metric}</td><td>${m.value}</td><td>${m.unit||''}</td><td>${m.window||''}</td><td>${m.notes||''}</td>`;
      tb.appendChild(tr);
    });
    el('snapMeta').textContent = `ts=${j.ts_iso}  meta=${JSON.stringify(j.meta||{})}`;
  }catch(e){
    alert('Snapshot error: '+e);
  }finally{
    el('btnSnap').disabled = false;
  }
}

async function submitForm(){
  el('btnSubmit').disabled = true;
  try{
    let sr = [];
    try { sr = JSON.parse(el('sr').value || '[]'); } catch(e){ alert('SR JSON invalid'); throw e; }

    const payload = {
      symbol: el('symbol').value || 'BTC',
      bias: el('bias').value,
      vol_regime: el('vol').value,
      fear_greed: Number(el('fg').value),
      etf_flow_bias: el('etf').value || null,
      onchain_flow_bias: el('onchain').value || null,
      futures_flow_bias: el('fut').value || null,
      funding_bias: el('funding').value || null,
      dxy_trend: el('dxy').value || null,
      corr_xau_btc: Number(el('corr').value),
      sr: sr
    };

    const r = await fetch('/desk/form', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    const j = await r.json();
    el('out').textContent = JSON.stringify(j, null, 2);
  }catch(e){
    console.error(e);
  }finally{
    el('btnSubmit').disabled = false;
  }
}

el('btnSnap').addEventListener('click', refreshSnap);
el('btnSubmit').addEventListener('click', submitForm);
el('btnStatus').addEventListener('click', refreshStatus);
refreshStatus();
refreshSnap();
</script>

</body>
</html>"""
