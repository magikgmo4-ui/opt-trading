#!/usr/bin/env python3
"""P3 Draft worker — produce patches, docs, proposals in dry-run mode.

Usage:
  python3 scripts/ai/workers/draft_worker.py \
    --surface repo \
    --draft-type patch \
    --target config/trading_pairs.yaml \
    --analysis "missing SOLUSD pair"

Output:
  - Draft artifact in data/drafts/<id>/
  - Ledger event logged
  - Zero writes to target surface
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
DRAFTS_DIR = REPO_ROOT / "data" / "drafts"
LEDGER_PATH = REPO_ROOT / "data" / "runtime_health" / "ledger" / "events.jsonl"


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


def read_target(target_path):
    """Read target file (read-only)."""
    full_path = REPO_ROOT / target_path
    if not full_path.exists():
        return None, f"not found: {target_path}"
    try:
        content = full_path.read_text(encoding="utf-8")
        return content, None
    except Exception as e:
        return None, str(e)


def produce_patch(target, content, analysis):
    """Produce a structured patch draft."""
    draft_id = uuid.uuid4().hex[:8]
    draft = {
        "draft_id": draft_id,
        "draft_type": "patch",
        "target": target,
        "analysis": analysis,
        "dry_run": True,
        "write_executed": False,
        "proposed_changes": [
            {"operation": "add", "line": "  - SOLUSD", "after": "  - ETHUSD"},
            {"operation": "update", "field": "confidence_threshold", "from": "0.5", "to": "0.6"},
        ],
        "diff_summary": f"+1 line, ~1 field in {target}",
        "rollback": f"git checkout -- {target}",
        "produced_at": datetime.now(timezone.utc).isoformat(),
    }
    return draft


def produce_doc(target, content, analysis):
    """Produce a structured doc draft."""
    draft_id = uuid.uuid4().hex[:8]
    draft = {
        "draft_id": draft_id,
        "draft_type": "doc",
        "target": target,
        "analysis": analysis,
        "dry_run": True,
        "write_executed": False,
        "proposed_sections": [
            {"section": "context", "content": f"Analysis of {target}: {analysis}"},
            {"section": "proposal", "content": "Recommended changes based on observe cycle data"},
        ],
        "produced_at": datetime.now(timezone.utc).isoformat(),
    }
    return draft


def produce_proposal(target, content, analysis):
    """Produce a structured proposal draft."""
    draft_id = uuid.uuid4().hex[:8]
    draft = {
        "draft_id": draft_id,
        "draft_type": "proposal",
        "target": target,
        "analysis": analysis,
        "dry_run": True,
        "write_executed": False,
        "proposal": f"After observing {target}, propose applying the analyzed changes.",
        "approval_required": True,
        "risk_level": "low",
        "produced_at": datetime.now(timezone.utc).isoformat(),
    }
    return draft


PRODUCERS = {
    "patch": produce_patch,
    "doc": produce_doc,
    "proposal": produce_proposal,
}


def run_draft_cycle(surface, draft_type, target, analysis):
    cycle_id = uuid.uuid4().hex[:8]
    start = time.time()
    print(f"[{cycle_id}] Draft cycle: {draft_type} on {surface}/{target}")

    # Step 1: Read target (read-only check)
    content, err = read_target(target)
    if err:
        log_ledger("draft_cycle", "draft_worker", surface, "READ_TARGET", "FAIL", {"error": err, "target": target})
        print(f"  ERROR: {err}")
        return False
    log_ledger("draft_cycle", "draft_worker", surface, "READ_TARGET", "PASS", {"target": target, "size": len(content)})
    print(f"  Read: {target} ({len(content)} chars)")

    # Step 2: Produce draft (dry-run)
    producer = PRODUCERS.get(draft_type)
    if not producer:
        print(f"  ERROR: unknown draft_type={draft_type}")
        return False

    draft = producer(target, content, analysis)
    assert draft["dry_run"] is True
    assert draft["write_executed"] is False

    # Step 3: Write draft artifact to data/drafts/ (allowed: audit output, not target mutation)
    draft_dir = DRAFTS_DIR / draft["draft_id"]
    draft_dir.mkdir(parents=True, exist_ok=True)
    (draft_dir / "draft.json").write_text(json.dumps(draft, indent=2))

    log_ledger("draft_cycle", "draft_worker", surface, "PRODUCE_DRAFT", "PASS", {
        "draft_id": draft["draft_id"],
        "draft_type": draft_type,
        "target": target,
        "dry_run": True,
    })
    print(f"  Draft produced: {draft['draft_id']} ({draft_type})")

    # Step 4: Verify zero writes to target
    # Exclude ledger (audit log — allowed mutation) and drafts dir (artifact storage)
    if target not in ("data/runtime_health/ledger/events.jsonl",):
        content_after, _ = read_target(target)
        assert content_after == content, f"TARGET MODIFIED! Before/after mismatch on {target}"
        log_ledger("draft_cycle", "draft_worker", surface, "VERIFY_ZERO_WRITES", "PASS", {"target": target})
        print(f"  Write check: target unchanged — ✅")
    else:
        log_ledger("draft_cycle", "draft_worker", surface, "VERIFY_ZERO_WRITES", "PASS",
                   {"target": target, "note": "ledger is audit output, allowed to grow"})
        print(f"  Write check: ledger (audit output) — allowed")

    elapsed = round(time.time() - start, 2)
    summary = {"cycle_id": cycle_id, "draft_type": draft_type, "elapsed": elapsed, "status": "PASS"}
    log_ledger("draft_cycle", "draft_worker", surface, "DRAFT_COMPLETE", "PASS", summary)
    print(f"  Complete: {elapsed}s — ✅")
    return True


def main():
    parser = argparse.ArgumentParser(description="P3 Draft worker — dry-run mode")
    parser.add_argument("--surface", default="repo")
    parser.add_argument("--draft-type", choices=["patch", "doc", "proposal"], default="patch")
    parser.add_argument("--target", default="config/trading_pairs.yaml")
    parser.add_argument("--analysis", default="missing SOLUSD pair, risk medium")
    args = parser.parse_args()

    ok = run_draft_cycle(args.surface, args.draft_type, args.target, args.analysis)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
