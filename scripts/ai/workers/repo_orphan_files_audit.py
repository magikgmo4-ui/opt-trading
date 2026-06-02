"""Find tracked Python/shell scripts with no import or reference in the codebase."""
import json, subprocess, pathlib, datetime

REPORT_PATH = pathlib.Path("reports/ai/repo_orphan_files_audit.json")
TARGET_EXTENSIONS = {'.py', '.sh'}
SKIP_DIRS = {'venv', '.git', '__pycache__', 'node_modules'}
SKIP_NAMES = {'__init__.py', 'conftest.py', 'setup.py'}
# Minimum lines threshold — very small stubs may be intentional
MIN_LINES = 5


def get_tracked_files():
    result = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True)
    return result.stdout.splitlines()


def build_reference_index(tracked: list[str]) -> set[str]:
    """Collect all base names mentioned in any tracked text file."""
    mentioned = set()
    text_exts = {'.py', '.sh', '.md', '.txt', '.yml', '.yaml', '.json', '.toml'}
    for path in tracked:
        if pathlib.Path(path).suffix not in text_exts:
            continue
        try:
            content = pathlib.Path(path).read_text(errors='ignore')
            mentioned.update(content.split())
        except OSError:
            pass
    return mentioned


def main():
    tracked = get_tracked_files()
    ref_index = build_reference_index(tracked)

    candidates = []
    for path in tracked:
        p = pathlib.Path(path)
        if p.suffix not in TARGET_EXTENSIONS:
            continue
        if p.name in SKIP_NAMES:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        try:
            lines = p.read_text(errors='ignore').splitlines()
        except OSError:
            continue
        if len(lines) < MIN_LINES:
            continue
        # Check if basename or stem mentioned anywhere
        if p.name not in ref_index and p.stem not in ref_index:
            candidates.append(path)

    report = {
        "job_id": "repo-orphan-files-audit",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "tracked_scripts": sum(1 for p in tracked
                               if pathlib.Path(p).suffix in TARGET_EXTENSIONS),
        "orphan_candidates": len(candidates),
        "candidates": candidates[:30],
        "status": "WARN" if candidates else "PASS",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"],
                      "orphan_candidates": len(candidates),
                      "status": report["status"]}, indent=2))

if __name__ == "__main__":
    main()
