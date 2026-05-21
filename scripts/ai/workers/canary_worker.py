#!/usr/bin/env python3
"""P9 Canary automation — first non-dry-run write with dual confirm.

Usage:
  # Propose a canary
  python3 scripts/ai/workers/canary_worker.py propose --action write_marker

  # Confirm (first approval)
  python3 scripts/ai/workers/canary_worker.py confirm <proposal_id> --approver "human_01"

  # Confirm again (second approval — triggers execution)
  python3 scripts/ai/workers/canary_worker.py confirm <proposal_id> --approver "human_02"

  # List proposals
  python3 scripts/ai/workers/canary_worker.py list

  # View canary history
  python3 scripts/ai/workers/canary_worker.py history
"""

import argparse
import json
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LEDGER_PATH = REPO_ROOT / "data" / "runtime_health" / "ledger" / "events.jsonl"
CANARY_DIR = REPO_ROOT / "data" / "canary"
PROPOSALS_DIR = CANARY_DIR / "proposals"
MARKERS_DIR = CANARY_DIR / "markers"

# Allowed canary actions — all non-critical
CANARY_ACTIONS = {
    "write_marker": {
        "description": "Write a canary marker file with metadata",
        "risk": "minimal",
        "target": "data/canary/markers/",
        "reversible": True,
        "critical": False,
    },
    "send_test_notification": {
        "description": "Send a test notification via Telegram bridge",
        "risk": "minimal",
        "target": "telegram (test channel)",
        "reversible": True,
        "critical": False,
    },
    "update_canary_log": {
        "description": "Append a line to the canary run log",
        "risk": "minimal",
        "target": "data/canary/canary_log.jsonl",
        "reversible": True,
        "critical": False,
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


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _load_proposals(status_filter=None):
    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    proposals = []
    for f in sorted(PROPOSALS_DIR.glob("*.json")):
        try:
            p = json.loads(f.read_text())
            if status_filter is None or p.get("status") == status_filter:
                proposals.append(p)
        except (json.JSONDecodeError, OSError):
            pass
    return proposals


def cmd_propose(action):
    if action not in CANARY_ACTIONS:
        print(f"ERROR: invalid canary action '{action}'. Allowed: {list(CANARY_ACTIONS.keys())}")
        return False

    meta = CANARY_ACTIONS[action]
    proposal = {
        "proposal_id": uuid.uuid4().hex[:12],
        "action": action,
        "description": meta["description"],
        "risk": meta["risk"],
        "target": meta["target"],
        "reversible": meta["reversible"],
        "critical": meta["critical"],
        "status": "proposed",
        "confirmations": [],
        "confirm_count": 0,
        "confirm_required": 2,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "executed_at": None,
    }
    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    path = PROPOSALS_DIR / f"{proposal['proposal_id']}.json"
    path.write_text(json.dumps(proposal, indent=2))

    log_ledger("canary", "canary_worker", meta["target"], "CANARY_PROPOSE", "PASS",
               {"proposal_id": proposal["proposal_id"], "action": action})
    print(f"Proposed: {proposal['proposal_id']} ({action} — {meta['description']})")
    print(f"  Confirmations required: 2")
    print(f"  Confirm with: python3 scripts/ai/workers/canary_worker.py confirm {proposal['proposal_id']} --approver <name>")
    return True


def cmd_confirm(proposal_id, approver):
    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    path = PROPOSALS_DIR / f"{proposal_id}.json"
    if not path.exists():
        print(f"ERROR: proposal not found: {proposal_id}")
        return False

    proposal = json.loads(path.read_text())

    if proposal["status"] == "executed":
        print(f"ERROR: proposal already executed")
        return False

    if proposal["status"] == "rejected":
        print(f"ERROR: proposal was rejected")
        return False

    # Check if this approver already confirmed
    existing = [c for c in proposal["confirmations"] if c["approver"] == approver]
    if existing:
        print(f"WARN: {approver} already confirmed on this proposal")

    confirmation = {
        "approver": approver,
        "role": "human",
        "timestamp": _now_iso(),
        "method": "cli_confirm",
    }
    proposal["confirmations"].append(confirmation)
    proposal["confirm_count"] = len(proposal["confirmations"])
    proposal["updated_at"] = _now_iso()

    log_ledger("canary", "canary_worker", proposal.get("target", "?"),
               "CANARY_CONFIRM", "PASS",
               {"proposal_id": proposal_id, "approver": approver,
                "confirm_count": proposal["confirm_count"],
                "confirm_required": proposal["confirm_required"]})

    if proposal["confirm_count"] >= proposal["confirm_required"]:
        # Dual confirm reached — execute
        proposal["status"] = "executed"
        proposal["executed_at"] = _now_iso()
        path.write_text(json.dumps(proposal, indent=2))

        result = _execute_canary(proposal)
        print(f"Confirmed: {proposal_id} ({proposal['confirm_count']}/{proposal['confirm_required']} — DUAL CONFIRM REACHED)")
        print(f"  Execute: {result['status']} — {result.get('message', '')}")
    else:
        proposal["status"] = "confirmed_once"
        path.write_text(json.dumps(proposal, indent=2))
        needed = proposal["confirm_required"] - proposal["confirm_count"]
        print(f"Confirmed: {proposal_id} ({proposal['confirm_count']}/{proposal['confirm_required']} — {needed} more needed)")

    return True


def _execute_canary(proposal):
    """Execute the canary action — actual non-dry-run write."""
    action = proposal["action"]
    exec_id = uuid.uuid4().hex[:12]

    if action == "write_marker":
        MARKERS_DIR.mkdir(parents=True, exist_ok=True)
        marker = {
            "execution_id": exec_id,
            "proposal_id": proposal["proposal_id"],
            "action": action,
            "timestamp": _now_iso(),
            "dry_run": False,
            "confirmations": proposal["confirm_count"],
            "confirmers": [c["approver"] for c in proposal["confirmations"]],
        }
        path = MARKERS_DIR / f"{exec_id}.json"
        path.write_text(json.dumps(marker, indent=2))
        log_ledger("canary", "canary_worker", proposal["target"], "CANARY_WRITE_MARKER", "PASS",
                   {"execution_id": exec_id, "file": str(path)})
        return {"status": "success", "message": f"Marker written to {path}"}

    elif action == "send_test_notification":
        log_ledger("canary", "canary_worker", proposal["target"], "CANARY_SEND_NOTIFICATION", "PASS",
                   {"execution_id": exec_id, "note": "Notification would be sent via Telegram bridge"})
        return {"status": "success", "message": "Test notification dispatched (simulated)"}

    elif action == "update_canary_log":
        log_path = CANARY_DIR / "canary_log.jsonl"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "execution_id": exec_id,
            "proposal_id": proposal["proposal_id"],
            "action": action,
            "timestamp": _now_iso(),
            "confirmers": [c["approver"] for c in proposal["confirmations"]],
        }
        with open(log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        log_ledger("canary", "canary_worker", proposal["target"], "CANARY_LOG_UPDATE", "PASS",
                   {"execution_id": exec_id})
        return {"status": "success", "message": "Canary log updated"}

    return {"status": "error", "message": f"Unknown action: {action}"}


def cmd_list():
    proposals = _load_proposals()
    if not proposals:
        print("No proposals.")
        return
    print(f"{'Proposal ID':16s} {'Action':20s} {'Status':18s} {'Confirms':10s} {'Created':20s}")
    print("-" * 84)
    for p in proposals:
        c = f"{p['confirm_count']}/{p['confirm_required']}"
        print(f"{p['proposal_id']:16s} {p['action']:20s} {p['status']:18s} {c:10s} {p['created_at'][:19]:20s}")
    print(f"\nTotal: {len(proposals)}")


def cmd_history():
    markers = sorted(MARKERS_DIR.glob("*.json")) if MARKERS_DIR.exists() else []
    if not markers:
        print("No canary executions yet.")
        return
    print(f"{'File':40s} {'Action':20s} {'Confirmers':30s} {'Timestamp':20s}")
    print("-" * 110)
    for f in markers:
        try:
            m = json.loads(f.read_text())
            confs = ", ".join(m.get("confirmers", []))
            print(f"{f.name:40s} {m['action']:20s} {confs:30s} {m['timestamp'][:19]:20s}")
        except (json.JSONDecodeError, OSError):
            print(f"{f.name:40s} {'ERROR':20s}")
    print(f"\nTotal executions: {len(markers)}")


def main():
    parser = argparse.ArgumentParser(description="P9 Canary automation — dual confirm non-dry-run")
    sub = parser.add_subparsers(dest="command", required=True)

    p_propose = sub.add_parser("propose", help="Propose a canary action")
    p_propose.add_argument("--action", required=True, choices=list(CANARY_ACTIONS.keys()),
                           help="Canary action type")

    p_confirm = sub.add_parser("confirm", help="Confirm a canary proposal")
    p_confirm.add_argument("proposal_id", help="Proposal ID")
    p_confirm.add_argument("--approver", required=True, help="Approver identifier")

    sub.add_parser("list", help="List all proposals")
    sub.add_parser("history", help="View execution history")

    args = parser.parse_args()

    ok = True
    if args.command == "propose":
        ok = cmd_propose(args.action)
    elif args.command == "confirm":
        ok = cmd_confirm(args.proposal_id, args.approver)
    elif args.command == "list":
        cmd_list()
    elif args.command == "history":
        cmd_history()

    return 0 if ok else 1


if __name__ == "__main__":
    main()
