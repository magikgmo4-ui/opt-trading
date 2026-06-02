"""Validate capability matrix — reads docs/agents/ capability docs."""
import json, pathlib, datetime, re

AGENTS_DIR = pathlib.Path("docs/agents")
REPORT_PATH = pathlib.Path("reports/ai/capability_matrix_validate.json")
EXPECTED_SECTIONS = ["capabilities", "constraints", "task_types"]


def scan_agent_docs():
    findings, agents = [], []
    if not AGENTS_DIR.exists():
        return [f"docs/agents/ directory not found"], []
    for f in sorted(AGENTS_DIR.rglob("*.md")):
        text = f.read_text(errors="ignore")
        agents.append(str(f))
        missing = [s for s in EXPECTED_SECTIONS if s.lower() not in text.lower()]
        if missing:
            findings.append(f"{f.name}: missing sections {missing}")
    return findings, agents


def main():
    findings, agents = scan_agent_docs()
    status = "PASS" if not findings else "WARN"
    report = {
        "job_id": "capability-matrix-validate",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "agents_scanned": len(agents),
        "findings": findings[:20],
        "status": status,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"], "agents": len(agents),
                      "findings": len(findings), "status": status}, indent=2))

if __name__ == "__main__":
    main()
