"""Validate AI team role registry — reads configs/env/registry/roles.yaml."""
import json, pathlib, datetime, re

ROLES_REGISTRY = pathlib.Path("configs/env/registry/roles.yaml")
REPORT_PATH = pathlib.Path("reports/ai/ai_team_role_registry_check.json")
MIN_ROLES = 3


def parse_roles_yaml(text: str) -> list[str]:
    return re.findall(r'^\s*-?\s*id:\s*(\S+)', text, re.MULTILINE)


def main():
    findings = []

    if not ROLES_REGISTRY.exists():
        findings.append(f"roles.yaml not found at {ROLES_REGISTRY}")
        roles = []
        status = "WARN"
    else:
        text = ROLES_REGISTRY.read_text()
        roles = parse_roles_yaml(text)
        if len(roles) < MIN_ROLES:
            findings.append(f"too few roles defined: {len(roles)} (minimum {MIN_ROLES})")
        status = "PASS" if not findings else "WARN"

    report = {
        "job_id": "ai-team-role-registry-check",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "roles_found": roles,
        "findings": findings,
        "status": status,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"], "roles": len(roles),
                      "findings": len(findings), "status": status}, indent=2))

if __name__ == "__main__":
    main()
