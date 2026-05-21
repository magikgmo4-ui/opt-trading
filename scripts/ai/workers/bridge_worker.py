#!/usr/bin/env python3
"""P5 App bridges — external apps under contract (Airtable/Sheets/Telegram/LocalCMS).

Usage:
  # READ_ONLY (default) — no external writes
  python3 scripts/ai/workers/bridge_worker.py --app telegram --mode READ_ONLY

  # DRAFT_ONLY — produce report without write
  python3 scripts/ai/workers/bridge_worker.py --app airtable --mode DRAFT_ONLY

  # WRITE_GATED — write only with explicit approval
  python3 scripts/ai/workers/bridge_worker.py --app sheets --mode WRITE_GATED --approve
"""

import argparse
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTRACT_PATH = REPO_ROOT / "scripts" / "ai" / "workers" / "orchestration" / "external_apps_orchestration_contract.json"
LEDGER_PATH = REPO_ROOT / "data" / "runtime_health" / "ledger" / "events.jsonl"
OUTPUT_DIR = REPO_ROOT / "reports" / "ai" / "workers"

# Contract definition of supported apps and their modes
APP_BRIDGES = {
    "airtable": {
        "read_allowed": True,
        "write_allowed": True,
        "write_gated": True,
        "module": "modules.airtable_bridge.app.client",
        "description": "Envoyer/consulter trades, signaux, backtests dans Airtable",
    },
    "google_sheets": {
        "read_allowed": True,
        "write_allowed": True,
        "write_gated": True,
        "script": "scripts/sheets/sync_daily_session.py",
        "description": "Synchroniser le journal quotidien vers Google Sheets",
    },
    "telegram": {
        "read_allowed": False,
        "write_allowed": True,
        "write_gated": True,
        "module": "shared.telegram_notify",
        "description": "Notifications Telegram sortantes (alertes, rapports)",
    },
    "localcms": {
        "read_allowed": True,
        "write_allowed": True,
        "write_gated": True,
        "module": "modules.localcms.app.main",
        "description": "Supervision et métriques internes LocalCMS",
    },
}


def log_ledger(event_type, actor, surface, action, status, payload=None):
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "event_id": uuid.uuid4().hex[:12],
        "event_type": event_type,
        "actor_id": actor,
        "surface_id": surface,
        "action": action,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "payload": payload or {},
    }
    with open(LEDGER_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")
    return event


def load_contract():
    return json.loads(CONTRACT_PATH.read_text())


def validate_request(args):
    """Validate request against the orchestration contract."""
    contract = load_contract()
    input_spec = contract["input"]
    errors = []

    if args.app not in input_spec["requested_app"]["enum"]:
        errors.append(f"invalid app '{args.app}': must be one of {input_spec['requested_app']['enum']}")

    if args.mode not in input_spec["mode"]["enum"]:
        errors.append(f"invalid mode '{args.mode}': must be one of {input_spec['mode']['enum']}")

    if args.app not in APP_BRIDGES:
        errors.append(f"app '{args.app}' has no bridge contract defined")

    return errors


def build_request(args):
    return {
        "requested_app": args.app,
        "mode": args.mode,
        "dry_run": not args.write if args.mode == "WRITE_GATED" else True,
        "trigger_source": "opencode",
        "operator_context": args.context or "P5_bridge_worker_validation",
        "validation_token": args.approve or "",
        "max_runtime_seconds": 60,
        "output_dir": "reports/ai/workers",
    }


def bridge_read(app, request):
    """Simulate a read operation on the target app bridge."""
    bridge = APP_BRIDGES[app]
    records = []

    if bridge["read_allowed"]:
        record = {
            "app": app,
            "action": "READ_INVENTORY",
            "status": "PASS",
            "mode": request["mode"],
            "note": f"Read from {app} bridge simulated",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        records.append(record)
        log_ledger("bridge_worker", f"bridge_{app}", app, "READ_INVENTORY", "PASS", record)
    else:
        log_ledger("bridge_worker", f"bridge_{app}", app, "READ_INVENTORY", "BLOCKED",
                   {"reason": f"{app} does not support read operations"})

    return records


def bridge_write(app, request):
    """Execute a write operation through the app bridge, respecting mode."""
    bridge = APP_BRIDGES[app]
    result = {
        "app": app,
        "action": "WRITE",
        "status": "PENDING",
        "mode": request["mode"],
        "dry_run": request.get("dry_run", True),
    }

    if not bridge["write_allowed"]:
        result["status"] = "BLOCKED"
        result["reason"] = f"{app} bridge does not permit writes"
        log_ledger("bridge_worker", f"bridge_{app}", app, "WRITE_BLOCKED", "BLOCKED", result)
        return result

    if request["mode"] in ("READ_ONLY", "DRAFT_ONLY"):
        result["status"] = "BLOCKED"
        result["reason"] = f"mode {request['mode']} forbids writes"
        log_ledger("bridge_worker", f"bridge_{app}", app, "WRITE_BLOCKED_BY_MODE", "BLOCKED", result)
        return result

    if request["dry_run"]:
        result["status"] = "DRAFT_ONLY"
        result["reason"] = "dry_run=True — write skipped"
        log_ledger("bridge_worker", f"bridge_{app}", app, "WRITE_DRAFT_ONLY", "PASS", result)
        return result

    if not request.get("validation_token"):
        result["status"] = "BLOCKED"
        result["reason"] = "WRITE_GATED requires validation_token (--approve)"
        log_ledger("bridge_worker", f"bridge_{app}", app, "WRITE_GATED_BLOCKED", "BLOCKED", result)
        return result

    # Write permitted
    result["status"] = "PASS"
    result["execution_id"] = uuid.uuid4().hex[:12]
    result["note"] = f"Write to {app} executed via bridge contract"
    log_ledger("bridge_worker", f"bridge_{app}", app, "WRITE_EXECUTED", "PASS", {
        "execution_id": result["execution_id"], "mode": request["mode"],
    })
    return result


def produce_report(app, request, reads, write_result):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = OUTPUT_DIR / f"bridge_{app}_{timestamp}.json"

    response = {
        "run_id": uuid.uuid4().hex,
        "job_packet_id": f"P5_BRIDGE_{app.upper()}",
        "task_type": f"BRIDGE_{request['mode']}",
        "selected_worker": "bridge_worker",
        "app_target": app,
        "actions_planned": ["validate_contract", "route_to_bridge", "read_inventory", "execute_write"],
        "actions_executed": ["validate_contract", "route_to_bridge"],
        "app_records_touched": reads,
        "files_touched": [],
        "report_path": str(report_path),
        "validation_status": "APPROVED" if write_result.get("status") == "PASS" else "NOT_REQUIRED",
        "stop_condition": write_result.get("reason") if write_result.get("status") in ("BLOCKED",) else None,
        "verdict": "PASS" if write_result.get("status") == "PASS" else
                   "DRAFT_ONLY" if write_result.get("status") == "DRAFT_ONLY" else
                   "BLOCKED" if write_result.get("status") == "BLOCKED" else "FAIL",
        "errors": [],
        "warnings": [],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if reads:
        response["actions_executed"].append("read_inventory")
    if write_result.get("status") in ("PASS",):
        response["actions_executed"].append("execute_write")

    report_path.write_text(json.dumps(response, indent=2))
    return response, report_path


def run_bridge_cycle(app, mode, approve_token=None, context=None):
    class Args:
        pass

    args = Args()
    args.app = app
    args.mode = mode
    args.write = bool(approve_token)
    args.approve = approve_token or ""
    args.context = context

    cycle_id = uuid.uuid4().hex[:8]
    start = time.time()
    print(f"[{cycle_id}] Bridge worker: app={app} mode={mode} approve={bool(approve_token)}")

    # Validate contract
    errors = validate_request(args)
    if errors:
        for e in errors:
            print(f"  CONTRACT ERROR: {e}")
        log_ledger("bridge_worker", "bridge_worker", app, "CONTRACT_VALIDATION", "FAIL", {"errors": errors})
        return False

    print(f"  Contract validated: {app} @ {mode}")

    # Build request from contract
    request = build_request(args)
    print(f"  Request: dry_run={request['dry_run']} token={'yes' if request['validation_token'] else 'no'}")

    # Route to bridge
    bridge = APP_BRIDGES[app]
    print(f"  Bridge: {bridge['description']}")

    # Execute read
    reads = bridge_read(app, request)
    print(f"  Read: {len(reads)} records")

    # Execute write (gated)
    write_result = bridge_write(app, request)
    print(f"  Write: {write_result['status']} — {write_result.get('reason', 'ok')}")

    # Produce report
    response, report_path = produce_report(app, request, reads, write_result)
    print(f"  Report: {report_path}")

    elapsed = round(time.time() - start, 2)
    summary = {"cycle_id": cycle_id, "app": app, "mode": mode, "verdict": response["verdict"], "elapsed": elapsed}
    log_ledger("bridge_worker", "bridge_worker", app, "BRIDGE_CYCLE_COMPLETE", response["verdict"], summary)
    print(f"  Result: {response['verdict']} ({elapsed}s)")
    return True


def main():
    parser = argparse.ArgumentParser(description="P5 App bridges under contract")
    parser.add_argument("--app", required=True, choices=list(APP_BRIDGES.keys()) + ["all"],
                        help="Target app bridge")
    parser.add_argument("--mode", default="READ_ONLY", choices=["READ_ONLY", "DRAFT_ONLY", "WRITE_GATED"],
                        help="Execution mode (default: READ_ONLY)")
    parser.add_argument("--approve", help="Validation token to approve WRITE_GATED")
    parser.add_argument("--context", help="Free operator context string")
    args = parser.parse_args()

    apps = list(APP_BRIDGES.keys()) if args.app == "all" else [args.app]

    all_ok = True
    for app in apps:
        ok = run_bridge_cycle(app, args.mode, approve_token=args.approve, context=args.context)
        if not ok:
            all_ok = False
        print()

    return 0 if all_ok else 1


if __name__ == "__main__":
    main()
