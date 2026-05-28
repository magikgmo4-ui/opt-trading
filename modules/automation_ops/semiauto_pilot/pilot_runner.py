"""Semi-auto pilot runner.

Exit codes:
  0 = PASS_DRY_RUN
  2 = STOP_CONDITION_TRIGGERED
  3 = INVALID_HANDOFF_CONTRACT
"""
from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

from modules.automation_ops.semiauto_pilot import handoff_contract, proof_writer, stop_conditions

GO_ID = "GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_SCOPE_01"
PARENT_GO_ID = "GO_AUTOMATION_OPS_OPT_TRADING_PARENT_SEMIAUTO_RUNTIME_PILOT_01"


def run(prompt_path: str | Path, base_dir: Path | None = None) -> int:
    prompt_path = Path(prompt_path)

    run_id = f"pilot_{uuid.uuid4().hex[:8]}"

    contract = handoff_contract.build_empty(
        run_id=run_id,
        go_id=GO_ID,
        parent_go_id=PARENT_GO_ID,
        input_prompt_path=str(prompt_path),
        next_go="",
    )

    try:
        _populate_from_prompt(contract, prompt_path)
    except Exception as exc:
        contract["verdict"] = "BLOCKED_WITH_REASON"
        _finalize(contract, base_dir)
        print(f"[pilot] INVALID_HANDOFF_CONTRACT: {exc}", file=sys.stderr)
        return 3

    try:
        stop_conditions.check(contract)
    except stop_conditions.StopConditionTriggered as exc:
        contract["verdict"] = "STOP_CONDITION_TRIGGERED"
        _finalize(contract, base_dir)
        print(f"[pilot] STOP_CONDITION_TRIGGERED: {exc.reason}", file=sys.stderr)
        return 2

    contract["verdict"] = "PASS_DRY_RUN"
    json_path, md_path = _finalize(contract, base_dir)
    print(f"[pilot] PASS_DRY_RUN — proof: {json_path}")
    print(f"[pilot] summary:           {md_path}")
    return 0


def _populate_from_prompt(contract: dict, prompt_path: Path) -> None:
    if not prompt_path.exists():
        raise FileNotFoundError(f"prompt file not found: {prompt_path}")

    raw = prompt_path.read_text().strip()
    if not raw:
        raise ValueError("prompt file is empty")

    contract["actions_planned"] = [
        "read GO_PROMPT",
        "validate handoff contract",
        "check stop conditions",
        "write proof artefacts",
        "return verdict",
    ]
    contract["actions_executed"] = ["read GO_PROMPT", "validate handoff contract"]

    try:
        overrides = json.loads(raw)
        if isinstance(overrides, dict):
            for key in ("stop_conditions", "next_go", "actions_planned"):
                if key in overrides:
                    contract[key] = overrides[key]
    except json.JSONDecodeError:
        pass
    # verdict is set by the caller after stop-condition checks pass


def _finalize(contract: dict, base_dir: Path | None) -> tuple[Path, Path]:
    return proof_writer.write(contract, base_dir)


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: pilot_runner.py <go_prompt_path>", file=sys.stderr)
        sys.exit(1)
    sys.exit(run(sys.argv[1]))


if __name__ == "__main__":
    main()
