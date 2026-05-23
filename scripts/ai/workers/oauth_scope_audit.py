import json, re
from pathlib import Path
from collections import Counter

scope_patterns = [
    (r'scope["\':\s]+([a-zA-Z_.-]+)', "inline_scope"),
    (r'oauth_scopes?\s*[=:]\s*[\'"]([^\'"]+)[\'"]', "oauth_assign"),
    (r'permissions?\s*[=:]\s*[\'"]([^\'"]+)[\'"]', "permission_assign"),
    (r'(https://www\.googleapis\.com/auth/[a-zA-Z.]+)', "google_api_scope"),
]

findings = []
scopes_found = Counter()

# Scan config files and docs for scope references
scan_dirs = [
    Path("config"),
    Path("docs/governance"),
    Path("docs/chantiers"),
]

for scan_dir in scan_dirs:
    if not scan_dir.exists():
        continue
    for f in sorted(scan_dir.rglob("*")):
        if not f.is_file():
            continue
        if f.suffix not in (".md", ".yml", ".yaml", ".json", ".py", ".cfg", ".conf", ".ini", ".example"):
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except:
            continue
        for pattern, label in scope_patterns:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                val = m.group(1).strip()
                if len(val) > 3 and len(val) < 120:
                    scopes_found[f"{label}:{val}"] += 1

result = {
    "job_id": "oauth-scope-audit",
    "files_scanned": len([f for d in scan_dirs if d.exists() for f in d.rglob("*") if f.is_file() and f.suffix in (".md", ".yml", ".yaml", ".json", ".py", ".cfg", ".conf", ".ini", ".example")]),
    "scope_references_found": len(scopes_found),
    "scope_details": [{"scope": k, "count": v} for k, v in scopes_found.most_common(20)],
    "findings": [],
    "status": "PASS",
}

if len(scopes_found) > 50:
    result["findings"].append(f"high scope reference count ({len(scopes_found)}), review needed")
if not scopes_found:
    result["findings"].append("no scope references found — audit coverage uncertain")
    result["status"] = "WARN"

print(json.dumps(result, indent=2))
