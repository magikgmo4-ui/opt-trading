"""Check required external tokens/env vars are present (not blank)."""
import json, os, pathlib, datetime, re

REPORT_PATH = pathlib.Path("reports/ai/external_token_presence_check.json")
CREDENTIALS_REGISTRY = pathlib.Path("configs/env/registry/credentials.yaml")

ALWAYS_CHECK = [
    "TV_WEBHOOK_KEY", "OPS_ADMIN_KEY",
    "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID",
]


def load_required_from_registry() -> list[str]:
    if not CREDENTIALS_REGISTRY.exists():
        return []
    text = CREDENTIALS_REGISTRY.read_text()
    return re.findall(r'^\s*-?\s*name:\s*(\S+)', text, re.MULTILINE)


def main():
    required = list(dict.fromkeys(ALWAYS_CHECK + load_required_from_registry()))
    present, missing, blank = [], [], []
    for var in required:
        val = os.environ.get(var)
        if val is None:
            missing.append(var)
        elif not val.strip():
            blank.append(var)
        else:
            present.append(var)

    findings = [f"MISSING: {v}" for v in missing] + [f"BLANK: {v}" for v in blank]
    status = "PASS" if not findings else "WARN"
    report = {
        "job_id": "external-token-presence-check",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "checked_count": len(required),
        "present": len(present),
        "missing": missing,
        "blank": blank,
        "findings": findings,
        "status": status,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"], "present": len(present),
                      "missing": len(missing), "status": status}, indent=2))

if __name__ == "__main__":
    main()
