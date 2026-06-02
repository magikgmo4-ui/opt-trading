"""Audit docs/chantiers/ — open GOs, stale GOs, missing acceptance reports."""
import json, pathlib, re, datetime

CHANTIERS_DIR = pathlib.Path("docs/chantiers")
REPORT_PATH = pathlib.Path("reports/ai/repo_go_index_audit.json")
STALE_DAYS = 30


def extract_frontmatter(text: str) -> dict:
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}
    result = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            result[k.strip()] = v.strip()
    return result


def main():
    open_gos, missing_acceptance, stale_gos = [], [], []
    total = 0

    for go_dir in sorted(CHANTIERS_DIR.iterdir()):
        if not go_dir.is_dir():
            continue
        init_doc = go_dir / "00_INITIAL_PROJECT_DOC.md"
        acceptance = go_dir / "20_ACCEPTANCE_REPORT.md"
        if not init_doc.exists():
            continue
        total += 1
        fm = extract_frontmatter(init_doc.read_text())
        status = fm.get("status", "unknown")
        go_id = fm.get("go_id", go_dir.name)
        opened_at = fm.get("opened_at", "")

        if status == "open":
            open_gos.append(go_id)
            if not acceptance.exists():
                missing_acceptance.append(go_id)
            # Check stale
            if opened_at:
                try:
                    opened = datetime.datetime.fromisoformat(opened_at)
                    age = (datetime.datetime.utcnow() - opened).days
                    if age > STALE_DAYS:
                        stale_gos.append({"go_id": go_id, "age_days": age})
                except ValueError:
                    pass

    report = {
        "job_id": "repo-go-index-audit",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "total_gos": total,
        "open_count": len(open_gos),
        "open_gos": open_gos,
        "missing_acceptance_count": len(missing_acceptance),
        "missing_acceptance": missing_acceptance,
        "stale_count": len(stale_gos),
        "stale_gos": stale_gos,
        "status": "WARN" if stale_gos or missing_acceptance else "PASS",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"], "total": total,
                      "open": len(open_gos), "stale": len(stale_gos),
                      "missing_acceptance": len(missing_acceptance),
                      "status": report["status"]}, indent=2))

if __name__ == "__main__":
    main()
