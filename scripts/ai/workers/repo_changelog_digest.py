"""Git log digest for last 24h — commits, files changed, authors."""
import json, subprocess, datetime, pathlib

REPORT_PATH = pathlib.Path("reports/ai/repo_changelog_digest.json")


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True, check=False).stdout.strip()


def main():
    since = "24 hours ago"
    log = run(["git", "log", f"--since={since}", "--oneline",
                "--format=%H|%s|%an|%ai"])
    commits = []
    for line in log.splitlines():
        if '|' in line:
            sha, subj, author, date = line.split('|', 3)
            commits.append({"sha": sha[:8], "subject": subj, "author": author, "date": date})

    files_changed = run(["git", "diff", "--name-only",
                         f"HEAD@{{24 hours ago}}", "HEAD"]) if commits else ""
    file_list = [f for f in files_changed.splitlines() if f]

    report = {
        "job_id": "repo-changelog-digest",
        "period": since,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "commit_count": len(commits),
        "commits": commits[:20],
        "files_changed_count": len(file_list),
        "files_changed": file_list[:30],
        "status": "PASS",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2))
    print(json.dumps({"job_id": report["job_id"], "commits": len(commits),
                      "files_changed": len(file_list), "status": "PASS"}, indent=2))

if __name__ == "__main__":
    main()
