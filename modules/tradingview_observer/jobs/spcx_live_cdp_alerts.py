from __future__ import annotations

import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CURRENT_FILE = Path(__file__).resolve()
REPO_ROOT = CURRENT_FILE.parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import yaml

from modules.env.env import ensure_dirs, load_env, project_root

load_env()
ensure_dirs()

ROOT = project_root()
TV_CLI_PATH = Path(os.environ.get("TRADINGVIEW_MCP_CLI", Path.home() / ".claude" / "tools" / "tradingview-mcp" / "src" / "cli" / "index.js"))
TV_TOOL_ROOT = Path.home() / ".claude" / "tools" / "tradingview-mcp" / "src"
TV_CONNECTION_URL = (TV_TOOL_ROOT / "connection.js").resolve().as_uri()
TV_PINE_CORE_URL = (TV_TOOL_ROOT / "core" / "pine.js").resolve().as_uri()
ALERT_NAMES = [
    "SPCX_VWAP_RECLAIM",
    "SPCX_VWAP_LOST",
    "SPCX_VWAP_REJECT",
    "SPCX_ORB_HIGH_BREAK",
    "SPCX_ORB_LOW_BREAK",
    "SPCX_BREAK_174",
    "SPCX_BREAK_180",
    "SPCX_LOST_160",
    "SPCX_TEST_148",
]
ALERT_FLAGS = {
    "SPCX_VWAP_RECLAIM": {"vwap_reclaim": True, "vwap_near": True, "vwap_state": True},
    "SPCX_VWAP_LOST": {"vwap_loss": True, "vwap_state": True},
    "SPCX_VWAP_REJECT": {"vwap_loss": True, "vwap_state": True, "vwap_reject": True},
    "SPCX_ORB_HIGH_BREAK": {"orb_break_high": True, "orb_zone": True},
    "SPCX_ORB_LOW_BREAK": {"orb_break_low": True, "orb_zone": True},
    "SPCX_BREAK_174": {"breakout_high": True, "key_level_break": True},
    "SPCX_BREAK_180": {"breakout_high": True, "key_level_break": True, "extension_level": True},
    "SPCX_LOST_160": {"breakdown_low": True, "key_level_break": True, "support_loss": True},
    "SPCX_TEST_148": {"breakdown_low": True, "key_level_break": True, "ipo_level": True},
}

ALERT_META = {
    "SPCX_VWAP_RECLAIM": {"event": "vwap_reclaim", "bias": "bullish", "signal": "BUY", "flags": ALERT_FLAGS["SPCX_VWAP_RECLAIM"]},
    "SPCX_VWAP_LOST": {"event": "vwap_loss", "bias": "bearish", "signal": "SELL", "flags": ALERT_FLAGS["SPCX_VWAP_LOST"]},
    "SPCX_VWAP_REJECT": {"event": "vwap_loss", "bias": "bearish", "signal": "SELL", "flags": ALERT_FLAGS["SPCX_VWAP_REJECT"]},
    "SPCX_ORB_HIGH_BREAK": {"event": "orb_break_high", "bias": "bullish", "signal": "BUY", "flags": ALERT_FLAGS["SPCX_ORB_HIGH_BREAK"]},
    "SPCX_ORB_LOW_BREAK": {"event": "orb_break_low", "bias": "bearish", "signal": "SELL", "flags": ALERT_FLAGS["SPCX_ORB_LOW_BREAK"]},
    "SPCX_BREAK_174": {"event": "breakout_high", "bias": "bullish", "signal": "BUY", "flags": ALERT_FLAGS["SPCX_BREAK_174"]},
    "SPCX_BREAK_180": {"event": "breakout_high", "bias": "bullish_extension", "signal": "BUY", "flags": ALERT_FLAGS["SPCX_BREAK_180"]},
    "SPCX_LOST_160": {"event": "breakdown_low", "bias": "bearish", "signal": "SELL", "flags": ALERT_FLAGS["SPCX_LOST_160"]},
    "SPCX_TEST_148": {"event": "breakdown_low", "bias": "risk_off", "signal": "SELL", "flags": ALERT_FLAGS["SPCX_TEST_148"]},
}


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def slug_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    return value.strip().lower() in {"1", "true", "yes", "on"}


def normalize_resolution(value: str) -> str:
    raw = str(value).strip().lower()
    if raw.endswith("m"):
        return raw[:-1]
    return raw


def resolve_webhook_url(raw_url: str) -> str:
    host = (
        os.environ.get("TRADINGVIEW_WEBHOOK_HOST")
        or os.environ.get("TV_WEBHOOK_HOST")
        or os.environ.get("HOST")
        or "127.0.0.1"
    )
    return raw_url.replace("<HOST>", host)


def redact_secret(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}***{value[-4:]}"


def load_config(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("Config root must be a mapping")
    alerts = data.get("alerts") or []
    if alerts != ALERT_NAMES:
        missing = [name for name in ALERT_NAMES if name not in alerts]
        if missing:
            raise ValueError(f"Config missing alerts: {', '.join(missing)}")
    data["symbol_full"] = f"{data['exchange']}:{data['symbol']}"
    data["tv_resolution"] = normalize_resolution(data["timeframe"])
    data["webhook_url_resolved"] = resolve_webhook_url(str(data["webhook_url"]))
    data["webhook_key"] = os.environ.get("TV_WEBHOOK_KEY", "").strip()
    return data


def run_process(args: list[str], input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        input=input_text,
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=False,
    )


def parse_last_json(text: str) -> Any:
    if not text.strip():
        raise RuntimeError("Expected JSON output, got empty stdout")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in reversed(lines):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue
    raise RuntimeError(f"Could not parse JSON from output: {text[-1000:]}")


def run_tv_json(*args: str) -> Any:
    proc = run_process(["node", str(TV_CLI_PATH), *args])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or f"tv command failed: {' '.join(args)}")
    return parse_last_json(proc.stdout)


def run_node_module_json(source: str) -> Any:
    proc = run_process(["node", "--input-type=module", "-"], input_text=source)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "node module failed")
    return parse_last_json(proc.stdout)


def connect_cdp(cdp_url: str) -> dict[str, Any]:
    with urllib.request.urlopen(cdp_url, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def open_tradingview(cdp_url: str) -> dict[str, Any]:
    try:
        return connect_cdp(cdp_url)
    except Exception:
        launch = run_tv_json("launch")
        for _ in range(20):
            time.sleep(1)
            try:
                return connect_cdp(cdp_url)
            except Exception:
                continue
        raise RuntimeError(f"TradingView launch did not expose CDP: {launch}")


def set_symbol(symbol_full: str) -> Any:
    return run_tv_json("symbol", symbol_full)


def set_timeframe(resolution: str) -> Any:
    return run_tv_json("timeframe", resolution)


def screenshot_validation(output_path: Path) -> Any:
    return run_tv_json("screenshot", "--file", str(output_path))


def write_run_log(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_study(state: dict[str, Any], needle: str) -> dict[str, Any] | None:
    for study in state.get("studies", []):
        if needle.lower() in str(study.get("name", "")).lower():
            return study
    return None


def ensure_monitor_script(config: dict[str, Any], run_log: list[str], dry_run: bool) -> dict[str, Any]:
    pine_source = build_monitor_pine(config)
    check_source = textwrap.dedent(
        f"""
        import {{ check }} from {json.dumps(TV_PINE_CORE_URL)};
        const result = await check({{ source: {json.dumps(pine_source)} }});
        console.log(JSON.stringify(result));
        """
    )
    compile_check = run_node_module_json(check_source)
    run_log.append(f"pine.check compiled={compile_check.get('compiled')} errors={compile_check.get('error_count', 0)}")
    if compile_check.get("compiled") is not True:
        raise RuntimeError(f"Pine compile check failed: {compile_check}")
    if dry_run:
        return {"compiled": True, "updated_chart": False}
    module_source = textwrap.dedent(
        f"""
        import {{ disconnect }} from {json.dumps(TV_CONNECTION_URL)};
        import {{ ensurePineEditorOpen, setSource, smartCompile, save }} from {json.dumps(TV_PINE_CORE_URL)};

        const source = {json.dumps(pine_source)};
        const editorReady = await ensurePineEditorOpen();
        if (!editorReady) {{
          await new Promise(resolve => setTimeout(resolve, 1500));
        }}
        const setResult = await setSource({{ source }});
        const compileResult = await smartCompile();
        const saveResult = await save();
        console.log(JSON.stringify({{ editorReady, setResult, compileResult, saveResult }}));
        await disconnect();
        """
    )
    try:
        result = run_node_module_json(module_source)
    except RuntimeError:
        time.sleep(2)
        result = run_node_module_json(module_source)
    run_log.append(
        "pine.update "
        f"button={result['compileResult'].get('button_clicked')} "
        f"has_errors={result['compileResult'].get('has_errors')}"
    )
    if result["compileResult"].get("has_errors"):
        raise RuntimeError(f"Pine chart compile failed: {result}")
    return {"compiled": True, "updated_chart": True, **result}


def ensure_indicators(config: dict[str, Any], run_log: list[str], dry_run: bool) -> dict[str, Any]:
    state_before = run_tv_json("state")
    set_symbol(config["symbol_full"])
    set_timeframe(config["tv_resolution"])
    pine_update = ensure_monitor_script(config, run_log, dry_run)
    state = run_tv_json("state")
    monitor = find_study(state, "SPCX Monitor Alerts | opt-trading")
    smc = find_study(state, "Smart Money Clone")
    if not monitor:
        raise RuntimeError("SPCX monitor indicator not found after Pine update")
    if not smc:
        raise RuntimeError("Smart Money Clone indicator not found on chart")
    smc_info = run_tv_json("indicator", "get", str(smc["id"]))
    if smc_info.get("visible") is not True and not dry_run:
        run_tv_json("indicator", "toggle", str(smc["id"]), "--visible", "true")
        smc_info = run_tv_json("indicator", "get", str(smc["id"]))
    values = run_tv_json("values")
    vwap_visible = False
    for study in values.get("studies", []):
        if study.get("name") == "SPCX Monitor Alerts | opt-trading" and "VWAP" in study.get("values", {}):
            vwap_visible = True
            break
    if not vwap_visible:
        raise RuntimeError("VWAP is not visible in the monitor indicator values")
    monitor_info = run_tv_json("indicator", "get", str(monitor["id"]))
    run_log.append(f"state symbol={state.get('symbol')} resolution={state.get('resolution')}")
    run_log.append(f"indicator monitor_id={monitor['id']} smc_id={smc['id']} smc_visible={smc_info.get('visible')}")
    return {
        "state_before": state_before,
        "state_after": state,
        "monitor": monitor,
        "monitor_info": monitor_info,
        "smc": smc,
        "smc_info": smc_info,
        "values": values,
        "pine_update": pine_update,
    }


def build_symbol_payload(symbol_full: str) -> str:
    symbol_json = {
        "symbol": symbol_full,
        "adjustment": "splits",
        "session": "regular",
        "currency-id": "USD",
    }
    return "=" + json.dumps(symbol_json, separators=(",", ":"))


def parse_decimal_text(value: Any) -> float:
    return float(str(value).strip().replace(" ", "").replace(",", "."))


def build_snapshot_context(config: dict[str, Any], indicator_context: dict[str, Any]) -> dict[str, float]:
    vwap_value = config["levels"]["vwap_reference"]
    for study in indicator_context["values"].get("studies", []):
        if study.get("name") == "SPCX Monitor Alerts | opt-trading":
            values = study.get("values", {})
            if "VWAP" in values:
                vwap_value = parse_decimal_text(values["VWAP"])
                break
    bars = run_tv_json("ohlcv", "--count", "20").get("bars", [])
    if not bars:
        raise RuntimeError("Could not read OHLCV bars for ORB snapshot")
    orb_high = float(bars[0]["high"])
    orb_low = float(bars[0]["low"])
    return {"vwap": float(vwap_value), "orb_high": orb_high, "orb_low": orb_low}


def alert_stop_target(alert_name: str, snapshot: dict[str, float], config: dict[str, Any]) -> tuple[float, float]:
    levels = config["levels"]
    if alert_name == "SPCX_VWAP_RECLAIM":
        return min(snapshot["vwap"], levels["support_intraday"]), levels["breakout_1"]
    if alert_name == "SPCX_ORB_HIGH_BREAK":
        return snapshot["orb_low"], levels["breakout_1"]
    if alert_name == "SPCX_BREAK_174":
        return min(snapshot["vwap"], levels["support_intraday"]), levels["breakout_2"]
    if alert_name == "SPCX_BREAK_180":
        return levels["breakout_1"], levels["extension"]
    if alert_name == "SPCX_ORB_LOW_BREAK":
        return snapshot["orb_high"], levels["support_intraday"]
    if alert_name == "SPCX_LOST_160":
        return max(snapshot["vwap"], levels["breakout_1"]), levels["ipo_low"]
    if alert_name == "SPCX_TEST_148":
        return levels["support_intraday"], levels["ipo_low"]
    return max(snapshot["vwap"], levels["breakout_1"]), levels["support_intraday"]


def build_price_alert_message(config: dict[str, Any], alert_name: str, snapshot: dict[str, float]) -> str:
    meta = ALERT_META[alert_name]
    payload = {
        "source": "tradingview_cdp",
        "contract_class": "signal_event.v1",
        "symbol": config["symbol"],
        "exchange": config["exchange"],
        "timeframe": str(config["timeframe"]).replace("m", ""),
        "event": meta["event"],
        "price": "{{close}}",
        "volume": "{{volume}}",
        "timestamp": "{{time}}",
        "flags": meta["flags"],
        "risk_mode": "monitor_only",
        "route": "data_center.signal_event",
    }
    return json.dumps(payload, separators=(",", ":"))


def price_condition_for(alert_name: str, snapshot: dict[str, float], config: dict[str, Any]) -> tuple[str, float]:
    levels = config["levels"]
    if alert_name == "SPCX_VWAP_RECLAIM":
        return "greater_than", snapshot["vwap"]
    if alert_name in {"SPCX_VWAP_LOST", "SPCX_VWAP_REJECT"}:
        return "less_than", snapshot["vwap"]
    if alert_name == "SPCX_ORB_HIGH_BREAK":
        return "greater_than", snapshot["orb_high"]
    if alert_name == "SPCX_ORB_LOW_BREAK":
        return "less_than", snapshot["orb_low"]
    if alert_name == "SPCX_BREAK_174":
        return "greater_than", float(levels["breakout_1"])
    if alert_name == "SPCX_BREAK_180":
        return "greater_than", float(levels["breakout_2"])
    if alert_name == "SPCX_LOST_160":
        return "less_than", float(levels["support_intraday"])
    return "less_than", float(levels["ipo_low"])


def create_price_alert(config: dict[str, Any], alert_name: str, snapshot: dict[str, float]) -> dict[str, Any]:
    condition, price = price_condition_for(alert_name, snapshot, config)
    message = build_price_alert_message(config, alert_name, snapshot)
    result = run_tv_json(
        "alert",
        "create",
        "--condition",
        condition,
        "--price",
        str(price),
        "--name",
        alert_name,
        "--webhook",
        config["webhook_url_resolved"],
        "--message",
        message,
        "--frequency",
        "on_bar_close",
    )
    return {
        "ok": result.get("success"),
        "status": 200 if result.get("success") else None,
        "body": result,
        "alert_name": alert_name,
    }


def create_alert(
    config: dict[str, Any],
    base_condition: dict[str, Any],
    monitor_inputs: dict[str, Any],
    pine_id: str,
    pine_version: str,
    alert_name: str,
) -> dict[str, Any]:
    request = {
        "alert_name": alert_name,
        "symbol_payload": build_symbol_payload(config["symbol_full"]),
        "resolution": config["tv_resolution"],
        "webhook_url": config["webhook_url_resolved"],
        "base_condition": base_condition,
        "monitor_inputs": monitor_inputs,
        "pine_id": pine_id,
        "pine_version": pine_version,
        "webhook_key": config["webhook_key"],
    }
    module_source = textwrap.dedent(
        f"""
        import {{ evaluate, evaluateAsync, disconnect, safeString }} from {json.dumps(TV_CONNECTION_URL)};

        const request = {json.dumps(request)};
        const requestString = JSON.stringify(request);
        await evaluate(`window.__opencodeCreateRequest = ${{safeString(requestString)}};`);
        const result = await evaluateAsync(`
        (async function() {{
          const request = JSON.parse(window.__opencodeCreateRequest);
          const condition = JSON.parse(JSON.stringify(request.base_condition));
          if (!condition.series || !condition.series.length) {{
            return {{ ok: false, error: "missing_condition_series", alert_name: request.alert_name }};
          }}
          condition.resolution = request.resolution;
          condition.cross_interval = false;
          condition.series[0].pine_id = request.pine_id;
          condition.series[0].pine_version = request.pine_version;
          condition.series[0].inputs = JSON.parse(JSON.stringify(request.monitor_inputs));
          condition.series[0].inputs.in_0 = true;
          condition.series[0].inputs.in_1 = request.webhook_key || "";
          condition.series[0].inputs.in_2 = request.alert_name;
          const payload = {{
            conditions: [condition],
            symbol: request.symbol_payload,
            resolution: request.resolution,
            message: "",
            sound_file: "alert/3_notes_reverb",
            sound_duration: 0,
            popup: false,
            auto_deactivate: false,
            email: false,
            sms_over_email: false,
            mobile_push: false,
            web_hook: request.webhook_url,
            name: request.alert_name,
            expiration: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
            active: true,
            ignore_warnings: true,
          }};
          const resp = await fetch("https://pricealerts.tradingview.com/create_alert", {{
            method: "POST",
            credentials: "include",
            body: JSON.stringify({{ payload }}),
          }});
          const text = await resp.text();
          let body = null;
          try {{ body = JSON.parse(text); }} catch (error) {{ body = {{ raw: text, parse_error: String(error) }}; }}
          return {{ ok: resp.status === 200 && body && body.s === "ok", status: resp.status, body, alert_name: request.alert_name }};
        }})()
        `);
        console.log(JSON.stringify(result));
        await disconnect();
        """
    )
    return run_node_module_json(module_source)


def create_all_alerts(config: dict[str, Any], indicator_context: dict[str, Any], run_log: list[str], dry_run: bool) -> dict[str, Any]:
    monitor_inputs = {}
    pine_id = ""
    pine_version = ""
    for item in indicator_context["monitor_info"].get("inputs", []):
        monitor_inputs[item["id"]] = item["value"]
        if item["id"] == "pineId":
            pine_id = str(item["value"])
        elif item["id"] == "pineVersion":
            pine_version = str(item["value"])
    base_alert = None
    raw_alerts = run_node_module_json(
        textwrap.dedent(
            f"""
            import {{ evaluateAsync, disconnect }} from {json.dumps(TV_CONNECTION_URL)};
            const result = await evaluateAsync(`fetch("https://pricealerts.tradingview.com/list_alerts", {{ credentials: "include" }}).then(r => r.json())`);
            console.log(JSON.stringify(result));
            await disconnect();
            """
        )
    )
    for alert in raw_alerts.get("r", []):
        if alert.get("type") != "indicator":
            continue
        studies = (alert.get("presentation_data") or {}).get("studies") or {}
        if any(study.get("description") == "SPCX Monitor Alerts | opt-trading" for study in studies.values()):
            base_alert = alert
            break
    if not base_alert:
        raise RuntimeError("No base SPCX monitor indicator alert found to clone")
    base_condition = copy.deepcopy(base_alert["conditions"][0])
    existing_by_name = {alert.get("name"): alert for alert in raw_alerts.get("r", [])}
    deleted_ids: list[int] = []
    snapshot = build_snapshot_context(config, indicator_context)
    if not dry_run:
        for alert_name in config["alerts"]:
            existing = existing_by_name.get(alert_name)
            if existing:
                run_tv_json("alert", "delete", "--id", str(existing["alert_id"]))
                deleted_ids.append(existing["alert_id"])
    results = []
    creation_mode = "indicator_clone"
    use_indicator_clone = any(item.get("id") == "in_5" for item in indicator_context["monitor_info"].get("inputs", []))
    for alert_name in config["alerts"]:
        meta = ALERT_META[alert_name]
        if dry_run:
            results.append({
                "name": alert_name,
                "event": meta["event"],
                "bias": meta["bias"],
                "signal": meta["signal"],
                "dry_run": True,
                "snapshot": snapshot,
            })
            continue
        if use_indicator_clone:
            result = create_alert(config, base_condition, monitor_inputs, pine_id, pine_version, alert_name)
            if result.get("ok") is not True:
                creation_mode = "price_snapshot_fallback"
                use_indicator_clone = False
                result = create_price_alert(config, alert_name, snapshot)
        else:
            creation_mode = "price_snapshot_fallback"
            result = create_price_alert(config, alert_name, snapshot)
        results.append({
            "name": alert_name,
            "event": meta["event"],
            "bias": meta["bias"],
            "signal": meta["signal"],
            "status": result.get("status"),
            "ok": result.get("ok"),
            "response": result.get("body"),
        })
        run_log.append(f"alert.create name={alert_name} ok={result.get('ok')} status={result.get('status')}")
        if result.get("ok") is not True:
            raise RuntimeError(f"Failed to create alert {alert_name}: {result}")
    final_alerts = run_tv_json("alert", "list")
    return {
        "creation_mode": creation_mode,
        "snapshot": snapshot,
        "deleted_ids": deleted_ids,
        "results": results,
        "final_alerts": final_alerts,
        "pine_id": pine_id,
        "pine_version": pine_version,
    }


def local_test_event(config: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "source": "tradingview",
        "symbol": config["symbol"],
        "exchange": config["exchange"],
        "timeframe": config["timeframe"],
        "tf": config["timeframe"],
        "event": "SPCX_CDP_SETUP_TEST",
        "bias": "bullish",
        "mode": "monitor_only",
        "price": str(config["levels"]["premarket_zone_high"]),
        "vwap": str(config["levels"]["vwap_reference"]),
        "engine": "TV_TEST",
        "signal": "BUY",
        "sl": str(config["levels"]["vwap_reference"]),
        "tp": str(config["levels"]["breakout_1"]),
        "reason": "SPCX_CDP_SETUP_TEST",
    }
    if config["webhook_key"]:
        payload["key"] = config["webhook_key"]
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(config["webhook_url_resolved"], data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8")
            return {"ok": True, "status": response.status, "body": json.loads(body) if body else None}
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8")
        return {"ok": False, "status": error.code, "body": body}
    except Exception as error:
        return {"ok": False, "status": None, "body": str(error)}


def build_monitor_pine(config: dict[str, Any]) -> str:
    levels = config["levels"]
    return textwrap.dedent(
        f"""
        //@version=5
        indicator("SPCX Monitor Alerts | opt-trading", overlay=true, max_labels_count=100)

        send_alerts = input.bool(true, "Send webhook alerts", group="Webhook")
        webhook_key = input.string("", "TV_WEBHOOK_KEY", group="Webhook")
        enabled_event = input.string("", "Enabled alert name", group="Webhook")

        regular_session = input.session("0930-1600", "Regular session", group="ORB")

        breakout_1 = input.float({levels['breakout_1']}, "Breakout 174", group="Levels")
        breakout_2 = input.float({levels['breakout_2']}, "Breakout 180", group="Levels")
        support_intraday = input.float({levels['support_intraday']}, "Support 160", group="Levels")
        ipo_low = input.float({levels['ipo_low']}, "IPO low 148", group="Levels")
        vwap_reference = input.float({levels['vwap_reference']}, "VWAP ref", group="Levels")
        premarket_zone_low = input.float({levels['premarket_zone_low']}, "Premarket low", group="Levels")
        premarket_zone_high = input.float({levels['premarket_zone_high']}, "Premarket high", group="Levels")
        extension = input.float({levels['extension']}, "Extension 190", group="Levels")

        vwap_value = ta.vwap(hlc3)
        in_regular = not na(time(timeframe.period, regular_session))
        new_regular = in_regular and not in_regular[1]

        var float orb_high = na
        var float orb_low = na

        if new_regular
            orb_high := high
            orb_low := low
        else if not in_regular
            orb_high := na
            orb_low := na

        f_num(v) =>
            str.tostring(v, format.mintick)

        f_match(code) =>
            send_alerts and str.length(enabled_event) > 0 and enabled_event == code

        f_event(code) =>
            switch code
                "SPCX_VWAP_RECLAIM" => "VWAP_RECLAIM"
                "SPCX_VWAP_LOST" => "VWAP_LOST"
                "SPCX_VWAP_REJECT" => "VWAP_REJECT"
                "SPCX_ORB_HIGH_BREAK" => "ORB_HIGH_BREAK"
                "SPCX_ORB_LOW_BREAK" => "ORB_LOW_BREAK"
                "SPCX_BREAK_174" => "BREAK_174"
                "SPCX_BREAK_180" => "BREAK_180"
                "SPCX_LOST_160" => "LOST_160"
                "SPCX_TEST_148" => "IPO_LOW_TEST_148"
                => code

        f_bias(code) =>
            switch code
                "SPCX_VWAP_RECLAIM" => "bullish"
                "SPCX_ORB_HIGH_BREAK" => "bullish"
                "SPCX_BREAK_174" => "bullish"
                "SPCX_BREAK_180" => "bullish_extension"
                "SPCX_TEST_148" => "risk_off"
                => "bearish"

        f_signal(code) =>
            switch code
                "SPCX_VWAP_RECLAIM" => "BUY"
                "SPCX_ORB_HIGH_BREAK" => "BUY"
                "SPCX_BREAK_174" => "BUY"
                "SPCX_BREAK_180" => "BUY"
                => "SELL"

        f_stop(code) =>
            switch code
                "SPCX_VWAP_RECLAIM" => math.min(vwap_value, support_intraday)
                "SPCX_ORB_HIGH_BREAK" => na(orb_low) ? vwap_value : orb_low
                "SPCX_BREAK_174" => math.min(vwap_value, support_intraday)
                "SPCX_BREAK_180" => breakout_1
                "SPCX_VWAP_LOST" => math.max(vwap_value, breakout_1)
                "SPCX_VWAP_REJECT" => math.max(vwap_value, breakout_1)
                "SPCX_ORB_LOW_BREAK" => na(orb_high) ? vwap_value : orb_high
                "SPCX_LOST_160" => math.max(vwap_value, breakout_1)
                "SPCX_TEST_148" => support_intraday
                => vwap_reference

        f_target(code) =>
            switch code
                "SPCX_VWAP_RECLAIM" => breakout_1
                "SPCX_ORB_HIGH_BREAK" => breakout_1
                "SPCX_BREAK_174" => breakout_2
                "SPCX_BREAK_180" => extension
                "SPCX_VWAP_LOST" => support_intraday
                "SPCX_VWAP_REJECT" => support_intraday
                "SPCX_ORB_LOW_BREAK" => support_intraday
                "SPCX_LOST_160" => ipo_low
                "SPCX_TEST_148" => ipo_low
                => close

        f_payload(code) =>
            event_name = f_event(code)
            flags_str = "\\\"flags\\\":{" + "\\\"" + event_name + "\\\":true}"
            payload = "{{" + "\\\"source\\\":\\\"tradingview_cdp\\\"," + "\\\"contract_class\\\":\\\"signal_event.v1\\\"," + "\\\"symbol\\\":\\\"SPCX\\\"," + "\\\"exchange\\\":\\\"NASDAQ\\\"," + "\\\"timeframe\\\":\\\"15\\\"," + "\\\"event\\\":\\\"" + event_name + "\\\"," + "\\\"price\\\":\\\"" + f_num(close) + "\\\"," + "\\\"volume\\\":\\\"" + f_num(volume) + "\\\"," + "\\\"timestamp\\\":\\\"" + f_num(time) + "\\\"," + flags_str + "," + "\\\"risk_mode\\\":\\\"monitor_only\\\"," + "\\\"route\\\":\\\"data_center.signal_event\\\"" + "}}"
            payload

        f_emit(code, condition) =>
            if barstate.isconfirmed and condition and f_match(code)
                alert(f_payload(code), alert.freq_once_per_bar_close)

        vwap_reclaim = ta.crossover(close, vwap_value)
        vwap_lost = ta.crossunder(close, vwap_value)
        vwap_reject = close < vwap_value and open < vwap_value and high >= vwap_value
        orb_high_break = not na(orb_high) and ta.crossover(close, orb_high)
        orb_low_break = not na(orb_low) and ta.crossunder(close, orb_low)
        break_174 = ta.crossover(close, breakout_1)
        break_180 = ta.crossover(close, breakout_2)
        lost_160 = ta.crossunder(close, support_intraday)
        test_148 = ta.crossunder(close, ipo_low)

        plot(vwap_value, "VWAP", color=color.orange, linewidth=2)
        plot(orb_high, "ORB High", color=color.new(color.lime, 0), linewidth=1, style=plot.style_linebr)
        plot(orb_low, "ORB Low", color=color.new(color.red, 0), linewidth=1, style=plot.style_linebr)

        plotshape(vwap_reclaim, title="SPCX VWAP Reclaim", style=shape.triangleup, location=location.belowbar, color=color.lime, size=size.tiny, text="VR")
        plotshape(vwap_lost, title="SPCX VWAP Lost", style=shape.triangledown, location=location.abovebar, color=color.red, size=size.tiny, text="VL")
        plotshape(vwap_reject, title="SPCX VWAP Reject", style=shape.flag, location=location.abovebar, color=color.maroon, size=size.tiny, text="RJ")
        plotshape(orb_high_break, title="SPCX ORB High", style=shape.triangleup, location=location.belowbar, color=color.aqua, size=size.tiny, text="OH")
        plotshape(orb_low_break, title="SPCX ORB Low", style=shape.triangledown, location=location.abovebar, color=color.fuchsia, size=size.tiny, text="OL")

        f_emit("SPCX_VWAP_RECLAIM", vwap_reclaim)
        f_emit("SPCX_VWAP_LOST", vwap_lost)
        f_emit("SPCX_VWAP_REJECT", vwap_reject)
        f_emit("SPCX_ORB_HIGH_BREAK", orb_high_break)
        f_emit("SPCX_ORB_LOW_BREAK", orb_low_break)
        f_emit("SPCX_BREAK_174", break_174)
        f_emit("SPCX_BREAK_180", break_180)
        f_emit("SPCX_LOST_160", lost_160)
        f_emit("SPCX_TEST_148", test_148)
        """
    ).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create SPCX monitor-only TradingView alerts through CDP")
    parser.add_argument("--config", required=True)
    parser.add_argument("--cdp-url", default="http://127.0.0.1:9222/json/version")
    parser.add_argument("--dry-run", default="true")
    args = parser.parse_args()

    dry_run = parse_bool(args.dry_run)
    config = load_config(args.config)
    output_dir = ROOT / "outputs" / "tradingview_observer" / "spcx_live_alerts" / slug_now()
    output_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = output_dir / "screenshot.png"
    alerts_path = output_dir / "alerts_created.json"
    run_log_path = output_dir / "run.log"
    run_log = [
        f"started_at={iso_now()}",
        f"dry_run={dry_run}",
        f"config={Path(args.config).as_posix()}",
        f"webhook_url={config['webhook_url_resolved']}",
        f"webhook_key_present={bool(config['webhook_key'])}",
    ]
    try:
        cdp = connect_cdp(args.cdp_url)
        run_log.append(f"cdp_browser={cdp.get('Browser')}")
    except Exception:
        cdp = open_tradingview(args.cdp_url)
        run_log.append(f"cdp_browser={cdp.get('Browser')}")
    indicator_context = ensure_indicators(config, run_log, dry_run)
    alerts_context = create_all_alerts(config, indicator_context, run_log, dry_run)
    screenshot_result = screenshot_validation(screenshot_path)
    run_log.append(f"screenshot_written={screenshot_path.as_posix()}")
    test_event_result = {"skipped": dry_run}
    if not dry_run:
        test_event_result = local_test_event(config)
        run_log.append(f"test_event_ok={test_event_result.get('ok')} status={test_event_result.get('status')}")
    serializable = {
        "started_at": iso_now(),
        "dry_run": dry_run,
        "config": {
            "symbol": config["symbol"],
            "exchange": config["exchange"],
            "mode": config["mode"],
            "timeframe": config["timeframe"],
            "webhook_url": config["webhook_url_resolved"],
            "webhook_key": redact_secret(config["webhook_key"]),
            "levels": config["levels"],
            "alerts": config["alerts"],
        },
        "cdp": cdp,
        "indicator_context": {
            "state_after": indicator_context["state_after"],
            "monitor": indicator_context["monitor"],
            "smc": indicator_context["smc"],
            "smc_visible": indicator_context["smc_info"].get("visible"),
            "pine_update": indicator_context["pine_update"],
        },
        "alerts": alerts_context,
        "screenshot": screenshot_result,
        "test_event": test_event_result,
    }
    alerts_path.write_text(json.dumps(serializable, indent=2, ensure_ascii=False), encoding="utf-8")
    write_run_log(run_log_path, run_log)
    print(json.dumps({
        "ok": True,
        "dry_run": dry_run,
        "output_dir": str(output_dir),
        "screenshot": str(screenshot_path),
        "alerts_json": str(alerts_path),
        "run_log": str(run_log_path),
        "created_alerts": len(alerts_context["results"]),
        "test_event_ok": test_event_result.get("ok"),
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
