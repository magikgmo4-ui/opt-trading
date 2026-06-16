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
    h2{margin:16px 0 8px 0;font-size:15px;color:#444;border-bottom:1px solid #e0e0e0;padding-bottom:4px;letter-spacing:.02em;text-transform:uppercase}
    .muted{color:#666;font-size:13px}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:10px}
    .card{border:1px solid #ddd;border-radius:10px;padding:14px}
    table{width:100%;border-collapse:collapse;font-size:13px}
    th,td{border-bottom:1px solid #eee;padding:6px 6px;text-align:left;vertical-align:top}
    input,select,textarea{width:100%;padding:8px;border:1px solid #ccc;border-radius:8px;font-size:14px}
    button{padding:10px 12px;border:1px solid #333;border-radius:10px;background:#111;color:#fff;cursor:pointer}
    button:disabled{opacity:.5;cursor:not-allowed}
    .row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
    pre{background:#0b0b0b;color:#e8e8e8;padding:10px;border-radius:10px;overflow:auto;font-size:12px}
    .pill{display:inline-block;padding:2px 8px;border:1px solid #ddd;border-radius:999px;font-size:12px;margin-right:6px}
    .action-panel{display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:8px 10px;background:#f5f5f5;border-radius:8px;border:1px solid #e8e8e8;margin:10px 0}
    .action-link{font-size:12px;color:#555;padding:4px 10px;border:1px solid #ddd;border-radius:8px;text-decoration:none;background:#fff}
    .action-link:hover{background:#e8e8e8}
    .action-btn{font-size:12px;padding:5px 12px;border:1px solid #333;border-radius:8px;background:#111;color:#fff;cursor:pointer}
    .action-btn:disabled{opacity:.5;cursor:not-allowed}
    .tools-section>summary{cursor:pointer;user-select:none;font-size:15px;font-weight:600;color:#444;padding:6px 0;border-bottom:1px solid #e0e0e0;list-style:none}
    .tools-section>summary::before{content:'▶ ';font-size:11px;color:#999}
    .tools-section[open]>summary::before{content:'▼ ';font-size:11px;color:#999}
    @media(max-width:900px){.grid{grid-template-columns:1fr}}
  </style>
</head>
<body>
  <h1>Desk Pro</h1>
  <div class="muted">
    Endpoints: <span class="pill">/desk/health</span><span class="pill">/desk/snapshot</span><span class="pill">/desk/form</span>
  </div>

  <h2>Runtime Health</h2>

  <!-- Action Panel — static, always visible, not JS-dependent -->
  <div id="actionPanel" class="action-panel">
    <button id="btnStatus" class="action-btn">Refresh Status</button>
    <button id="btnTestAlert" class="action-btn">Test Alert</button>
    <a href="/desk/errors" class="action-link">errors</a>
    <a href="/desk/alerts" class="action-link">alerts</a>
    <a href="/desk/logs/latest" class="action-link">logs</a>
    <a href="/desk/toolbox" class="action-link">toolbox</a>
    <a href="http://127.0.0.1:8000" class="action-link" id="localcmsLink" target="_blank" title="localcms docs viewer — port 8000 (incompatible avec webhook server)">localcms</a>
    <span id="testAlertResult" class="muted" style="font-size:12px;margin-left:4px"></span>
    <span id="statusTs" class="muted" style="font-size:12px;margin-left:auto"></span>
  </div>
  <div id="portConflictNote" style="font-size:11px;color:#888;margin-bottom:8px;padding:0 2px">
    ⚠ Port 8000 partagé — <strong>localcms</strong> et <strong>webhook server</strong> ne peuvent pas coexister. Choisir l'un ou l'autre avant de démarrer.
  </div>

  <div class="card" id="runtimeHealthCard">
    <h3 style="margin-top:0">Pipeline Status</h3>
    <div class="muted">Live from /desk/status</div>
    <div id="pipelineSummary"></div>
    <div id="errorDiagnostics" style="margin-top:10px;border-top:1px solid #eee;padding-top:8px;font-size:12px">
      <span class="muted">…</span>
    </div>
    <details style="margin-top:6px">
      <summary class="muted" style="cursor:pointer">Raw JSON</summary>
      <pre id="pipelineStatus" style="font-size:11px">loading...</pre>
    </details>
  </div>

  <details class="tools-section" id="analysisTools" style="margin-top:16px">
    <summary>Analysis Tools</summary>
    <div class="grid">
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

      <details class="card" id="formCard">
        <summary style="cursor:pointer;font-size:16px;font-weight:600">Formulaire → Probabilité</summary>

        <div class="row" style="margin-top:12px">
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
      </details>
    </div>
  </details>

  <details class="tools-section" id="visionPanel" style="margin-top:16px">
    <summary>Coinglass Vision</summary>
    <div class="card" style="margin-top:10px">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
        <button id="btnVision" class="action-btn">Refresh</button>
        <span id="visionMeta" class="muted" style="font-size:12px"></span>
      </div>
      <div id="visionContent">
        <span class="muted">Click Refresh to load vision data.</span>
      </div>
    </div>
  </details>

  <details class="tools-section" id="followupPanel" style="margin-top:16px">
    <summary>Follow-up Surfaces</summary>
    <div class="grid">
      <div class="card">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
          <button id="btnNewsVision" class="action-btn">Refresh</button>
          <span id="newsVisionMeta" class="muted" style="font-size:12px"></span>
        </div>
        <h3 style="margin-top:0">News Sentiment</h3>
        <div id="newsVisionContent"><span class="muted">Click Refresh to load news sentiment.</span></div>
      </div>
      <div class="card">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
          <button id="btnScreenerVision" class="action-btn">Refresh</button>
          <span id="screenerVisionMeta" class="muted" style="font-size:12px"></span>
        </div>
        <h3 style="margin-top:0">Screener Context</h3>
        <div id="screenerVisionContent"><span class="muted">Click Refresh to load screener context.</span></div>
      </div>
      <div class="card">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
          <button id="btnTelegramClaim" class="action-btn">Refresh</button>
          <span id="telegramClaimMeta" class="muted" style="font-size:12px"></span>
        </div>
        <h3 style="margin-top:0">Telegram Claim</h3>
        <div id="telegramClaimContent"><span class="muted">Click Refresh to load telegram claim.</span></div>
      </div>
    </div>
  </details>

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

function renderKeyValueList(entries){
  return '<ul style="margin:0;padding-left:18px">' + entries.map(e=>`<li>${e}</li>`).join('') + '</ul>';
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

    // Contextual guidance when degraded or down
    if(h.status === 'down' || h.status === 'degraded'){
      const failing = (h.checks||[]).filter(c => c.status === 'fail' || c.status === 'warn');
      const causes = failing.map(c => c.check);
      let msg = '';
      if(causes.includes('webhook_activity')){
        msg = 'Aucun signal TradingView récent — normal en dev local, vérifier les alertes TradingView en production.';
      } else if(causes.includes('webhook')){
        msg = 'Port 8000 injoignable — démarrer le webhook server.';
      } else if(causes.includes('perf')){
        msg = 'Module Perf injoignable — vérifier le service sur le port 8010.';
      } else if(causes.includes('probe_errors')){
        msg = 'Erreurs de sonde accumulées — consulter /desk/errors pour le détail.';
      } else if(causes.length > 0){
        msg = 'Composants en échec : ' + causes.join(', ') + '.';
      }
      if(msg){
        html += '<div style="margin-bottom:8px;padding:6px 10px;border-radius:6px;background:#fff8e1;border-left:3px solid #f9a825;font-size:12px;color:#555" id="healthGuidance">';
        html += msg;
        html += '</div>';
      }
    }

    // Update tab title to reflect health state
    document.title = 'Desk Pro' + (h.status && h.status !== 'healthy' ? ' — ' + h.status.toUpperCase() : '');

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
        if(a.dispatch){
          for(const d of a.dispatch){
            const ok = d.sent ? '✓' : '✗';
            html += ' <span class="muted">' + ok + ' ' + d.destination + '</span>';
          }
        }
        html += '</div>';
      } else if(a.reason === 'cooldown'){
        html += '<div style="margin-top:6px;font-size:12px;color:#888">';
        html += 'Alert cooldown: ' + a.cooldown_remaining_sec + 's remaining (last: ' + (a.last_status||'?') + ')';
        html += '</div>';
      }
    }

    el('pipelineSummary').innerHTML = html;
    el('statusTs').textContent = 'updated ' + (j.ts||'');
    refreshErrors();
  }catch(e){
    el('pipelineStatus').textContent = 'ERROR: '+e;
    el('pipelineSummary').innerHTML = '<span style="color:#c62828">Pipeline unreachable: '+e+'</span>';
  }
}

async function refreshErrors(){
  try{
    const r = await fetch('/desk/errors');
    const j = await r.json();
    let html = '<strong>Erreurs récentes</strong> ';
    if(j.count === 0){
      html += '<span style="color:#2e7d32">— aucune erreur</span>';
    } else {
      html += '<span style="color:#c62828">— ' + j.count + ' total</span>';
      // Next action suggestion based on failing probe
      const probes = (j.errors||[]).map(e => e.probe||'');
      let action = 'Consulter /desk/logs/latest pour le détail.';
      if(probes.some(p => p.includes('8000') || p.includes('webhook'))){
        action = 'Port 8000 injoignable — démarrer le webhook server ou localcms.';
      } else if(probes.some(p => p.includes('8010') || p.includes('perf'))){
        action = 'Erreur de sonde Perf — vérifier le service sur port 8010.';
      }
      html += '<div style="margin:4px 0 4px 0;padding:4px 8px;border-radius:4px;background:#fff3e0;border-left:2px solid #e65100;color:#555">Action suggérée : ' + action + '</div>';
      html += '<table style="width:100%;font-size:11px;margin-top:2px">';
      html += '<thead><tr><th>heure</th><th>probe</th><th>erreur</th></tr></thead><tbody>';
      for(const e of (j.errors||[]).slice(0,5)){
        const t = (e.ts||'').slice(11,19);
        const probe = e.probe||'?';
        const err = e.error||'?';
        html += `<tr><td style="white-space:nowrap;color:#888;padding-right:8px">${t}</td><td style="color:#888;padding-right:8px">${probe}</td><td style="color:#c62828">${err}</td></tr>`;
      }
      html += '</tbody></table>';
      if(j.count > 5){
        html += '<div class="muted" style="margin-top:2px">+ ' + (j.count-5) + ' autres — voir <a href="/desk/errors">errors log</a></div>';
      }
    }
    el('errorDiagnostics').innerHTML = html;
  }catch(e){
    el('errorDiagnostics').innerHTML = '<span class="muted">erreurs : inaccessible</span>';
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

async function testAlert(){
  el('btnTestAlert').disabled = true;
  el('testAlertResult').textContent = '…';
  try{
    const r = await fetch('/desk/alert/test', {method:'POST'});
    const j = await r.json();
    if(!r.ok){ el('testAlertResult').textContent = 'error ' + r.status; return; }
    const parts = (j.dispatch||[]).map(d=>{
      const icon = d.status === 'delivered' ? '✓' : (d.status === 'skipped' ? '–' : '✗');
      return icon + ' ' + d.destination;
    });
    el('testAlertResult').textContent = parts.join('  ') || 'no destinations';
  }catch(e){
    el('testAlertResult').textContent = 'error: ' + e;
  }finally{
    el('btnTestAlert').disabled = false;
  }
}

async function refreshVision(){
  el('btnVision').disabled = true;
  el('visionMeta').textContent = 'loading…';
  try{
    const r = await fetch('/desk/vision');
    const j = await r.json();
    if(!j.ok || !j.vision){
      el('visionContent').innerHTML = '<span class="muted">No vision data — ' + (j.reason||'unavailable') + '</span>';
      el('visionMeta').textContent = '';
      return;
    }
    const v = j.vision;
    const age = j.age_hours != null ? j.age_hours.toFixed(1) + 'h ago' : '';
    const freshColor = v.freshness_state === 'fresh' ? '#2e7d32' : (v.freshness_state === 'stale' ? '#e65100' : '#888');
    el('visionMeta').innerHTML =
      v.symbol + ' ' + v.timeframe + ' | ' +
      '<span style="color:' + freshColor + ';font-weight:600">' + v.freshness_state + '</span>' +
      (age ? ' | ' + age : '') + ' | ' + (v.screenshot_ts||'');

    let html = '<table><thead><tr><th>metric</th><th>value</th><th>unit</th><th>conf</th><th>quality bar</th><th>notes</th></tr></thead><tbody>';
    for(const det of (v.detections||[])){
      const val = det.extracted_value != null ? det.extracted_value.toLocaleString() : '<em>N/A</em>';
      const conf = det.confidence != null ? (det.confidence*100).toFixed(0)+'%' : '?';
      const confColor = det.confidence >= 0.85 ? '#2e7d32' : (det.confidence >= 0.60 ? '#e65100' : '#c62828');
      const barW = Math.round((det.confidence||0)*100);
      const bar = '<div style="width:80px;height:8px;background:#eee;border-radius:4px;overflow:hidden"><div style="width:' + barW + '%;height:100%;background:' + confColor + '"></div></div>';
      html += '<tr><td>' + det.detected_metric_type + '</td><td>' + val + '</td><td>' + (det.unit||'') + '</td><td style="color:' + confColor + ';font-weight:600">' + conf + '</td><td>' + bar + '</td><td class="muted">' + (det.notes||'') + '</td></tr>';
    }
    if(!(v.detections||[]).length) html += '<tr><td colspan="6" class="muted">No detections</td></tr>';
    html += '</tbody></table>';
    if((v.warnings||[]).length){
      html += '<div style="margin-top:8px;padding:6px 10px;background:#fff8e1;border-left:3px solid #f9a825;border-radius:4px;font-size:12px">';
      html += '<strong>Warnings:</strong> ' + v.warnings.join(' — ');
      html += '</div>';
    }
    el('visionContent').innerHTML = html;
  }catch(e){
    el('visionContent').innerHTML = '<span class="muted">Error: ' + e + '</span>';
    el('visionMeta').textContent = '';
  }finally{
    el('btnVision').disabled = false;
  }
}

async function refreshSimplePanel(url, contentId, metaId, renderFn){
  const content = el(contentId);
  const meta = el(metaId);
  try{
    const r = await fetch(url);
    const j = await r.json();
    if(!j.ok){
      content.innerHTML = '<span class="muted">No data — ' + (j.reason||'unavailable') + '</span>';
      meta.textContent = '';
      return;
    }
    const payload = j.payload || j.vision || {};
    content.innerHTML = renderFn(payload);
    meta.textContent = j.age_hours == null ? '' : (j.age_hours.toFixed(1) + 'h ago');
  }catch(e){
    content.innerHTML = '<span class="muted">Error: ' + e + '</span>';
    meta.textContent = '';
  }
}

function renderNews(payload){
  const agg = payload.aggregate || {};
  const top = (payload.articles || []).slice(0,3).map(a => `${a.source}: ${a.headline}`);
  return renderKeyValueList([
    `sentiment=${agg.sentiment_label||'n/a'}`,
    `avg_score=${agg.average_sentiment_score ?? 'n/a'}`,
    `articles=${payload.article_count ?? 0}`,
    `top=${top.join(' | ') || 'n/a'}`,
  ]);
}

function renderScreener(payload){
  const top = (payload.top_gainers || []).slice(0,3).map(s => `${s.symbol} ${s.change_pct}%`);
  return renderKeyValueList([
    `label=${payload.screener_label||payload.screener_symbol||'n/a'}`,
    `stocks=${payload.stock_count ?? 0}`,
    `avg_change=${payload.avg_change_pct ?? 'n/a'}`,
    `top=${top.join(' | ') || 'n/a'}`,
  ]);
}

function renderTelegramClaim(payload){
  const entities = payload.entities || {};
  return renderKeyValueList([
    `type=${payload.claim_type||'n/a'}`,
    `symbol=${payload.symbol||'n/a'}`,
    `timeframe=${payload.timeframe||'n/a'}`,
    `direction=${entities.direction||'n/a'}`,
    `confidence=${entities.confidence ?? 'n/a'}`,
    `levels=${(entities.levels||[]).join(', ') || 'n/a'}`,
  ]);
}

async function refreshNewsVision(){
  return refreshSimplePanel('/desk/vision/news', 'newsVisionContent', 'newsVisionMeta', renderNews);
}

async function refreshScreenerVision(){
  return refreshSimplePanel('/desk/vision/screener', 'screenerVisionContent', 'screenerVisionMeta', renderScreener);
}

async function refreshTelegramClaim(){
  return refreshSimplePanel('/desk/vision/telegram-claim', 'telegramClaimContent', 'telegramClaimMeta', renderTelegramClaim);
}

el('btnSnap').addEventListener('click', refreshSnap);
el('btnSubmit').addEventListener('click', submitForm);
el('btnStatus').addEventListener('click', refreshStatus);
el('btnTestAlert').addEventListener('click', testAlert);
el('btnVision').addEventListener('click', refreshVision);
el('btnNewsVision').addEventListener('click', refreshNewsVision);
el('btnScreenerVision').addEventListener('click', refreshScreenerVision);
el('btnTelegramClaim').addEventListener('click', refreshTelegramClaim);

// -- SPCX Score

function gradeColor(grade){
  const m={'A+':'#2e7d32','A':'#4caf50','B':'#e65100','C':'#c62828'};
  return m[grade]||'#888';
}
function stateColor(state){
  const m={'active':'#2e7d32','watch':'#e65100','invalidated':'#c62828'};
  return m[state]||'#888';
}
function renderSpcxCard(j){
  const grade=j.grade||'?',state=j.setup_state||'?',score=j.score??0;
  const bias=j.bias||'?',lvl=j.levels||{};
  const events=(j.events||[]).join(', ')||'-';
  const risk=(j.risk_notes||[]).join(', ')||'-';
  const inv=j.invalidation||{},ds=j.data_source||{};
  const fmtN=v=>v!=null?Number(v).toFixed(2):'-';
  let invHtml='';
  if(inv.vwap_loss) invHtml+='<div>VWAP loss @ '+fmtN(inv.vwap_loss.level)+' -- '+(inv.vwap_loss.note||'')+'</div>';
  if(inv.orb_loss)  invHtml+='<div>ORB loss @ '+fmtN(inv.orb_loss.level)+' -- '+(inv.orb_loss.note||'')+'</div>';
  const gradeBadge='<div style="font-size:42px;font-weight:700;line-height:1;color:'+gradeColor(grade)+'">'+grade+'</div>';
  const scoreBadge='<div style="font-size:22px;font-weight:600;color:#333">'+score+'<span style="font-size:13px;color:#888">/100</span></div>';
  const stateBadge='<div style="margin-top:4px;padding:2px 8px;border-radius:999px;background:'+stateColor(state)+';color:#fff;font-size:11px;font-weight:600;display:inline-block">'+state.toUpperCase()+'</div>';
  let rows='<tr><td style="color:#888;padding:2px 8px 2px 0;white-space:nowrap">Bias</td><td>'+bias+'</td></tr>';
  rows+='<tr><td style="color:#888;padding:2px 8px 2px 0">Prix</td><td>'+fmtN(lvl.price)+'</td></tr>';
  rows+='<tr><td style="color:#888;padding:2px 8px 2px 0">VWAP</td><td>'+fmtN(lvl.vwap)+'</td></tr>';
  rows+='<tr><td style="color:#888;padding:2px 8px 2px 0">ORB High</td><td>'+fmtN(lvl.orb_high)+'</td></tr>';
  rows+='<tr><td style="color:#888;padding:2px 8px 2px 0">Signaux</td><td style="font-size:12px">'+events+'</td></tr>';
  if(risk!=='-') rows+='<tr><td style="color:#e65100;padding:2px 8px 2px 0">Risque</td><td style="color:#e65100;font-size:12px">'+risk+'</td></tr>';
  if(invHtml) rows+='<tr><td style="color:#888;padding:2px 8px 2px 0;vertical-align:top">Invalide si</td><td style="font-size:12px;color:#555">'+invHtml+'</td></tr>';
  return '<div style="display:grid;grid-template-columns:auto 1fr;gap:10px 18px;align-items:start"><div style="text-align:center;min-width:70px">'+gradeBadge+scoreBadge+stateBadge+'</div><table style="font-size:13px;border-collapse:collapse;width:100%">'+rows+'</table></div><div style="margin-top:8px;font-size:11px;color:#aaa">Source: '+(ds.cdp_events||0)+' CDP + '+(ds.wire_events||0)+' wire | <span style="color:#2e7d32">monitor_only</span></div>';
}
async function refreshSpcx(){
  const btn=el('btnSpcx'),meta=el('spcxMeta'),content=el('spcxContent');
  if(btn) btn.disabled=true;
  if(meta) meta.textContent='loading...';
  try{
    const r=await fetch('/desk/spacex/score');
    const j=await r.json();
    if(content) content.innerHTML=renderSpcxCard(j);
    if(meta) meta.textContent=new Date().toLocaleTimeString();
  }catch(e){
    if(content) content.innerHTML='<span class="muted">Error: '+e+'</span>';
    if(meta) meta.textContent='';
  }finally{
    if(btn) btn.disabled=false;
  }
}
async function sendVoiceCommand(){
  const inp=el('voiceInput'),out=el('voiceOutput'),btn=el('btnVoiceCmd');
  const q=(inp?inp.value:'').trim();
  if(!q) return;
  if(btn) btn.disabled=true;
  if(out) out.textContent='...';
  try{
    const r=await fetch('/desk/voice?q='+encodeURIComponent(q));
    const j=await r.json();
    if(out) out.textContent=j.response||'(no response)';
    if(j.intent==='spcx_score'&&j.data){
      const c=el('spcxContent');
      if(c) c.innerHTML=renderSpcxCard(j.data);
    }
  }catch(e){
    if(out) out.textContent='Error: '+e;
  }finally{
    if(btn) btn.disabled=false;
  }
}
// -- Opening Session card (Phase 4)
function renderOpeningSessionCard(j){
  const m=j.opening_metrics||{},c=j.opening_components||{},l=j.score??0,g=j.grade||'?',s=j.setup_state||'?';
  const gap=m.opening_gap_pct!=null?m.opening_gap_pct.toFixed(2)+'%':'-';
  const drive=m.opening_drive||'-';
  const pmh=m.premarket_high!=null?Number(m.premarket_high).toFixed(2):'-';
  const pml=m.premarket_low!=null?Number(m.premarket_low).toFixed(2):'-';
  const dv=m.distance_vwap_pct!=null?m.distance_vwap_pct.toFixed(2)+'%':'-';
  const dorb=m.distance_orb_pct!=null?m.distance_orb_pct.toFixed(2)+'%':'-';
  const rvol=m.relative_volume_15m!=null?m.relative_volume_15m.toFixed(2)+'x':'-';
  const rs=m.risk_score??0;
  const cs=m.continuation_score??0;
  const es=m.exhaustion_score??0;
  const boost=c.dynamic_boost??0;
  const det=(c.details||[]).join(', ')||'-';
  const boostClr=boost>0?'#2e7d32':(boost<0?'#c62828':'#888');
  const rsClr=rs>=60?'#c62828':(rs>=30?'#e65100':'#2e7d32');
  const csClr=cs>=60?'#2e7d32':(cs>=30?'#e65100':'#c62828');
  const esClr=es>=60?'#c62828':(es>=30?'#e65100':'#2e7d32');
  let rows='<table style="font-size:13px;border-collapse:collapse;width:100%">';
  rows+='<tr><td style="color:#888;padding:2px 8px 2px 0;white-space:nowrap">Gap %</td><td>'+gap+'</td><td style="color:#888;padding:2px 8px 2px 0;white-space:nowrap">Drive</td><td>'+drive+'</td></tr>';
  rows+='<tr><td style="color:#888;padding:2px 8px 2px 0">Premarket H</td><td>'+pmh+'</td><td style="color:#888;padding:2px 8px 2px 0">Premarket L</td><td>'+pml+'</td></tr>';
  rows+='<tr><td style="color:#888;padding:2px 8px 2px 0">Dist VWAP</td><td>'+dv+'</td><td style="color:#888;padding:2px 8px 2px 0">Dist ORB</td><td>'+dorb+'</td></tr>';
  rows+='<tr><td style="color:#888;padding:2px 8px 2px 0">RVOL 15m</td><td>'+rvol+'</td><td colspan="2"></td></tr>';
  rows+='</table>';
  rows+='<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:8px">';
  rows+='<div style="text-align:center;border:1px solid #ddd;border-radius:8px;padding:6px"><div style="font-size:11px;color:#888">Risque</div><div style="font-size:20px;font-weight:700;color:'+rsClr+'">'+rs+'</div></div>';
  rows+='<div style="text-align:center;border:1px solid #ddd;border-radius:8px;padding:6px"><div style="font-size:11px;color:#888">Continuation</div><div style="font-size:20px;font-weight:700;color:'+csClr+'">'+cs+'</div></div>';
  rows+='<div style="text-align:center;border:1px solid #ddd;border-radius:8px;padding:6px"><div style="font-size:11px;color:#888">Épuisement</div><div style="font-size:20px;font-weight:700;color:'+esClr+'">'+es+'</div></div>';
  rows+='</div>';
  rows+='<div style="margin-top:6px;font-size:11px;color:#888">Score: <span style="font-weight:600;color:#333">'+l+'/100</span> | Grade: <span style="color:'+gradeColor(g)+';font-weight:600">'+g+'</span> | '+s.toUpperCase()+' | Boost: <span style="color:'+boostClr+';font-weight:600">'+(boost>0?'+':'')+boost+'</span></div>';
  if(det!=='-') rows+='<div style="margin-top:4px;font-size:11px;color:#888">Signaux: '+det+'</div>';
  rows+='<div style="margin-top:4px;font-size:10px;color:#aaa">monitor_only</div>';
  return rows;
}
async function refreshOpeningSession(){
  const btn=el('btnOpeningSession'),meta=el('openingSessionMeta'),content=el('openingSessionContent');
  if(btn) btn.disabled=true;
  if(meta) meta.textContent='loading...';
  try{
    const r=await fetch('/desk/spacex/opening-session');
    const j=await r.json();
    if(content) content.innerHTML=renderOpeningSessionCard(j);
    if(meta) meta.textContent=new Date().toLocaleTimeString();
  }catch(e){
    if(content) content.innerHTML='<span class="muted">Error: '+e+'</span>';
    if(meta) meta.textContent='';
  }finally{
    if(btn) btn.disabled=false;
  }
}
if(el('btnOpeningSession')) el('btnOpeningSession').addEventListener('click',refreshOpeningSession);

if(el('btnSpcx')) el('btnSpcx').addEventListener('click',refreshSpcx);
if(el('btnVoiceCmd')) el('btnVoiceCmd'].addEventListener('click',sendVoiceCommand);
if(el('voiceInput')) el('voiceInput').addEventListener('keydown',e=>{if(e.key==='Enter')sendVoiceCommand();});

refreshStatus();
refreshNewsVision();
refreshScreenerVision();
refreshTelegramClaim();
</script>

  <!-- SPCX Score card -->
  <details class="tools-section" id="spcxPanel" style="margin-top:16px" ontoggle="if(this.open&&el('spcxContent')&&!el('spcxContent').innerHTML.trim())refreshSpcx()">
    <summary>SPCX Score</summary>
    <div class="card" style="margin-top:10px">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
        <button id="btnSpcx" class="action-btn">Refresh</button>
        <a href="/desk/spacex/score" class="action-link" target="_blank">JSON</a>
        <span id="spcxMeta" class="muted" style="font-size:12px"></span>
      </div>
      <div id="spcxContent"><span class="muted">Cliquez Refresh pour charger le score SPCX.</span></div>
    </div>
  </details>

  <!-- Opening Session card (Phase 4) -->
  <details class="tools-section" id="openingSessionPanel" style="margin-top:16px" ontoggle="if(this.open&&el('openingSessionContent')&&!el('openingSessionContent').innerHTML.trim())refreshOpeningSession()">
    <summary>Opening Session</summary>
    <div class="card" style="margin-top:10px">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
        <button id="btnOpeningSession" class="action-btn">Refresh</button>
        <a href="/desk/spacex/opening-session" class="action-link" target="_blank">JSON</a>
        <span id="openingSessionMeta" class="muted" style="font-size:12px"></span>
      </div>
      <div id="openingSessionContent"><span class="muted">Cliquez Refresh pour charger les métriques d'ouverture.</span></div>
    </div>
  </details>

  <!-- Voice Operator -->
  <details class="tools-section" id="voicePanel" style="margin-top:16px">
    <summary>Voice Operator</summary>
    <div class="card" style="margin-top:10px">
      <div class="muted" style="margin-bottom:8px">Commande texte/voix -- reponse lecture seule</div>
      <div style="display:flex;gap:8px;align-items:center">
        <input id="voiceInput" placeholder='"score spcx" ou "help"'
               style="flex:1;padding:8px;border:1px solid #ccc;border-radius:8px;font-size:14px" />
        <button id="btnVoiceCmd" class="action-btn">Envoyer</button>
      </div>
      <pre id="voiceOutput" style="margin-top:10px;font-size:13px;min-height:40px;white-space:pre-wrap"></pre>
    </div>
  </details>

</body>
</html>
"""
