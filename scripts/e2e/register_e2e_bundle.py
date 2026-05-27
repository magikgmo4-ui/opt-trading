#!/usr/bin/env python3
"""
E2E Artifact Registry — PF_OPENCLAW_ORCHESTRATOR_FULL

Registers a bundle produced by build_e2e_report_bundle.py into the lightweight
artifact registry without committing bundle content.

Registry file: artifacts/e2e_artifact_registry/e2e_artifact_registry.jsonl
  One JSON entry per line (append-only).
  Committed to git as metadata — bundles themselves stay gitignored.

Registry entry fields:
  run_id, created_at, registered_at, verdict, e2e_status, gate_status,
  dry_run, live_trade, go_id, pf_id, bundle_path, manifest_hash,
  summary_hash, git_sha, modules

Safety:
  Refused if dry_run != True, live_trade != False, gate_status != APPROVED_PAPER.
  Refused if bundle_dir missing or manifest.json absent.
  Deduplication: refuses if run_id already registered.

Usage:
  python3 scripts/e2e/register_e2e_bundle.py \\
    --bundle-dir data/e2e_report_bundles/20260526_120000

  python3 scripts/e2e/register_e2e_bundle.py \\
    --bundle-dir data/e2e_report_bundles/20260526_120000 \\
    --registry artifacts/e2e_artifact_registry/e2e_artifact_registry.jsonl
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)
log = logging.getLogger("register_e2e_bundle")

# ── Constants ─────────────────────────────────────────────────────────────────

GO_ID = "GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_ARTIFACT_REGISTRY_01"
REGISTRY_VERSION = "1.0"
DEFAULT_REGISTRY = (
    PROJECT_ROOT / "artifacts" / "e2e_artifact_registry" / "e2e_artifact_registry.jsonl"
)


# ── Exceptions ────────────────────────────────────────────────────────────────

class RegistryRefused(Exception):
    """Raised when a bundle fails safety checks or is ineligible for registration."""


# ── Validation ────────────────────────────────────────────────────────────────

def _validate_manifest(manifest: dict) -> None:
    """Raise RegistryRefused if the manifest fails safety invariants."""
    if manifest.get("dry_run") is not True:
        raise RegistryRefused(
            f"manifest.dry_run={manifest.get('dry_run')!r} — only dry_run=True bundles can be registered"
        )
    if manifest.get("live_trade") is not False:
        raise RegistryRefused(
            f"manifest.live_trade={manifest.get('live_trade')!r} — live_trade must be False"
        )
    if manifest.get("gate_status") != "APPROVED_PAPER":
        raise RegistryRefused(
            f"manifest.gate_status={manifest.get('gate_status')!r} — only APPROVED_PAPER bundles can be registered"
        )
    if not manifest.get("run_id"):
        raise RegistryRefused("manifest.run_id is missing or empty")
    if not manifest.get("go_id"):
        raise RegistryRefused("manifest.go_id is missing or empty")


def _check_duplicate(run_id: str, registry_path: Path) -> None:
    """Raise RegistryRefused if run_id is already registered."""
    if not registry_path.exists():
        return
    with registry_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get("run_id") == run_id:
                    raise RegistryRefused(
                        f"run_id={run_id!r} already registered in {registry_path}"
                    )
            except json.JSONDecodeError:
                continue


# ── Helpers ───────────────────────────────────────────────────────────────────

def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()}"


def _get_git_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=str(PROJECT_ROOT),
        )
        if result.returncode == 0:
            return result.stdout.strip()[:12]
    except Exception:
        pass
    return "unknown"


# ── Entry builder ─────────────────────────────────────────────────────────────

def _build_entry(bundle_dir: Path, manifest: dict, registry_path: Path) -> dict:
    summary_path = bundle_dir / "summary.md"
    manifest_path = bundle_dir / "manifest.json"

    manifest_hash = _sha256_file(manifest_path)
    summary_hash = _sha256_file(summary_path) if summary_path.exists() else None

    return {
        "registry_version": REGISTRY_VERSION,
        "registry_go_id": GO_ID,
        "run_id": manifest["run_id"],
        "created_at": manifest.get("created_at"),
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "verdict": manifest.get("verdict"),
        "e2e_status": manifest.get("verdict"),
        "gate_status": manifest.get("gate_status"),
        "dry_run": manifest.get("dry_run"),
        "live_trade": manifest.get("live_trade"),
        "sheets_mode": manifest.get("sheets_mode"),
        "telegram_mode": manifest.get("telegram_mode"),
        "localcms_gate": manifest.get("localcms_gate"),
        "go_id": manifest.get("go_id"),
        "pf_id": manifest.get("pf_id"),
        "parent_go": manifest.get("parent_go"),
        "bundle_path": str(bundle_dir.resolve()),
        "manifest_hash": manifest_hash,
        "summary_hash": summary_hash,
        "git_sha": _get_git_sha(),
        "modules": manifest.get("modules", {}),
        "duration_s": manifest.get("duration_s"),
    }


# ── Registry writer ───────────────────────────────────────────────────────────

def register_bundle(
    bundle_dir: Path | str,
    registry_path: Path | str | None = None,
) -> dict:
    """
    Register a bundle into the artifact registry.

    Returns result dict with status=REGISTERED or status=REFUSED.
    """
    bundle_dir = Path(bundle_dir).resolve()
    registry_path = Path(registry_path) if registry_path else DEFAULT_REGISTRY

    if not bundle_dir.exists():
        raise RegistryRefused(f"bundle_dir does not exist: {bundle_dir}")

    manifest_path = bundle_dir / "manifest.json"
    if not manifest_path.exists():
        raise RegistryRefused(f"manifest.json not found in {bundle_dir}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    _validate_manifest(manifest)
    _check_duplicate(manifest["run_id"], registry_path)

    entry = _build_entry(bundle_dir, manifest, registry_path)

    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with registry_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, default=str) + "\n")

    log.info("Registered bundle run_id=%s → %s", entry["run_id"], registry_path)
    return {
        "status": "REGISTERED",
        "run_id": entry["run_id"],
        "registry_path": str(registry_path),
        "manifest_hash": entry["manifest_hash"],
        "verdict": entry["verdict"],
        "gate_status": entry["gate_status"],
    }


# ── Registry reader ───────────────────────────────────────────────────────────

def list_registry(registry_path: Path | str | None = None) -> list[dict]:
    """Return all entries from the registry as a list of dicts."""
    registry_path = Path(registry_path) if registry_path else DEFAULT_REGISTRY
    if not registry_path.exists():
        return []
    entries = []
    with registry_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="E2E Artifact Registry")
    sub = parser.add_subparsers(dest="command", required=True)

    reg = sub.add_parser("register", help="Register a bundle")
    reg.add_argument("--bundle-dir", required=True, metavar="DIR",
                     help="Path to the bundle directory to register")
    reg.add_argument("--registry", metavar="FILE", default=None,
                     help=f"Registry JSONL path (default: {DEFAULT_REGISTRY})")

    lst = sub.add_parser("list", help="List registered bundles")
    lst.add_argument("--registry", metavar="FILE", default=None,
                     help=f"Registry JSONL path (default: {DEFAULT_REGISTRY})")

    args = parser.parse_args()

    if args.command == "register":
        try:
            result = register_bundle(
                bundle_dir=args.bundle_dir,
                registry_path=args.registry,
            )
            print(json.dumps(result, indent=2, default=str))
        except RegistryRefused as exc:
            log.error("REFUSED: %s", exc)
            print(json.dumps({"status": "REFUSED", "reason": str(exc)}, indent=2))
            sys.exit(1)

    elif args.command == "list":
        entries = list_registry(registry_path=args.registry)
        print(json.dumps(entries, indent=2, default=str))


if __name__ == "__main__":
    main()
