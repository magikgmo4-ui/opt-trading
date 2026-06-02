"""Scan git-tracked files for secret/credential patterns."""
import json, re, subprocess, datetime, pathlib

REPORT_PATH = pathlib.Path("reports/ai/anti_leak_scan.json")

SECRET_PATTERNS = [
    (r'(?i)password\s*=\s*["\']?[^\s"\']{6,}', "password literal"),
    (r'(?i)secret\s*=\s*["\']?[^\s"\']{8,}', "secret literal"),
    (r'(?i)api[_-]?key\s*=\s*["\']?[^\s"\']{8,}', "api_key literal"),
    (r'(?i)private[_-]?key\s*=\s*["\']?[^\s"\']{8,}', "private_key literal"),
    (r'(?i)bearer\s+[A-Za-z0-9+/=_-]{20,}', "bearer token"),
    (r'AKIA[0-9A-Z]{16}', "AWS access key"),
    (r'ghp_[A-Za-z0-9]{36}', "GitHub PAT"),
    (r'xoxb-[0-9]+-[A-Za-z0-9]+', "Slack bot token"),
]

SKIP_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
                   '.pdf', '.zip', '.tar', '.gz', '.woff', '.woff2',
                   '.ttf', '.eot', '.pyc', '.lock'}
SKIP_PATHS = {'venv/', '.git/', 'node_modules/', '__pycache__/'}


def get_tracked_files():
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True, text=True, check=True
    )
    return [p for p in result.stdout.splitlines() if p.strip()]


def should_skip(path: str) -> bool:
    if pathlib.Path(path).suffix.lower() in SKIP_EXTENSIONS:
        return True
    return any(path.startswith(s) for s in SKIP_PATHS)


def scan_file(path: str) -> list[dict]:
    hits = []
    try:
        text = pathlib.Path(path).read_text(errors="ignore")
        for pattern, label in SECRET_PATTERNS:
            for m in re.finditer(pattern, text):
                line_no = text[:m.start()].count('\n') + 1
                # Ignore .env.example and test fixture files
                if '.env.example' in path or 'fixture' in path or 'test_' in path:
                    continue
                hits.append({"file": path, "line": line_no, "pattern": label,
                             "snippet": m.group()[:60]})
    except (OSError, UnicodeDecodeError):
        pass
    return hits


def main():
    files = get_tracked_files()
    scanned, findings = 0, []
    for f in files:
        if should_skip(f):
            continue
        scanned += 1
        findings.extend(scan_file(f))

    status = "PASS" if not findings else "WARN"
    report = {
        "job_id": "anti-leak-scan",
        "scanned_at": datetime.datetime.utcnow().isoformat() + "Z",
        "files_scanned": scanned,
        "findings_count": len(findings),
        "findings": findings[:20],  # cap output
        "status": status,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"], "scanned": scanned,
                      "findings": len(findings), "status": status}, indent=2))

if __name__ == "__main__":
    main()
