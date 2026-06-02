"""Check localcms safe button config — validates write-gate labels in UI config."""
import json, pathlib, datetime, re

LOCALCMS_APP = pathlib.Path("modules/localcms/app.py")
LOCALCMS_ROUTES = pathlib.Path("modules/localcms")
REPORT_PATH = pathlib.Path("reports/ai/localcms_safe_buttons_check.json")

DANGEROUS_PATTERNS = [
    re.compile(r'method\s*=\s*["\']POST["\']', re.IGNORECASE),
    re.compile(r'method\s*=\s*["\']DELETE["\']', re.IGNORECASE),
]
SAFE_LABEL_PATTERNS = [
    re.compile(r'dry.?run', re.IGNORECASE),
    re.compile(r'read.?only', re.IGNORECASE),
    re.compile(r'gate', re.IGNORECASE),
]


def scan_localcms():
    findings, safe_found = [], []
    if not LOCALCMS_ROUTES.exists():
        return ["localcms module not found"], []
    for f in LOCALCMS_ROUTES.rglob("*.py"):
        text = f.read_text(errors="ignore")
        for pat in DANGEROUS_PATTERNS:
            for m in pat.finditer(text):
                line = text[:m.start()].count('\n') + 1
                findings.append(f"{f.name}:{line} — {m.group()}")
        for pat in SAFE_LABEL_PATTERNS:
            if pat.search(text):
                safe_found.append(f.name)
    return findings[:10], list(set(safe_found))


def main():
    findings, safe = scan_localcms()
    status = "PASS" if not findings else "WARN"
    report = {
        "job_id": "localcms-safe-buttons-check",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "dangerous_patterns_found": len(findings),
        "safe_patterns_confirmed": len(safe),
        "findings": findings,
        "status": status,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"], "findings": len(findings),
                      "status": status}, indent=2))

if __name__ == "__main__":
    main()
