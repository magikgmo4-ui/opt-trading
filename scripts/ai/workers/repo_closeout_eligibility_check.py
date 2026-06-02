"""Find GOs eligible to close: acceptance PASS but initial_doc still open."""
import json, pathlib, re, datetime

CHANTIERS_DIR = pathlib.Path("docs/chantiers")
REPORT_PATH = pathlib.Path("reports/ai/repo_closeout_eligibility.json")


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
    eligible = []
    total = 0

    for go_dir in sorted(CHANTIERS_DIR.iterdir()):
        if not go_dir.is_dir():
            continue
        init_doc = go_dir / "00_INITIAL_PROJECT_DOC.md"
        acceptance = go_dir / "20_ACCEPTANCE_REPORT.md"
        if not init_doc.exists() or not acceptance.exists():
            continue
        total += 1
        init_fm = extract_frontmatter(init_doc.read_text())
        acc_fm = extract_frontmatter(acceptance.read_text())

        init_status = init_fm.get("status", "")
        acc_status = acc_fm.get("status", "")
        go_id = init_fm.get("go_id", go_dir.name)

        if init_status == "open" and acc_status in ("PASS", "PASS_WITH_FINDINGS", "PASS_WITH_FOLLOWUP"):
            eligible.append({
                "go_id": go_id,
                "init_status": init_status,
                "acceptance_status": acc_status,
                "closed_at": acc_fm.get("closed_at", ""),
            })

    report = {
        "job_id": "repo-closeout-eligibility-check",
        "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
        "total_checked": total,
        "eligible_count": len(eligible),
        "eligible": eligible,
        "status": "WARN" if eligible else "PASS",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"], "eligible": len(eligible),
                      "status": report["status"]}, indent=2))

if __name__ == "__main__":
    main()
