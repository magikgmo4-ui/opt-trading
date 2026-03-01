#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
from datetime import datetime

def read_text(p: Path) -> str:
    try: return p.read_text(errors="ignore")
    except Exception: return ""

def load_events(ndjson: Path, limit=2000):
    events=[]
    if not ndjson.exists(): return events
    for line in ndjson.read_text(errors="ignore").splitlines():
        line=line.strip()
        if not line: continue
        try: events.append(json.loads(line))
        except: pass
    return events[-limit:]

def extract_todos(text: str):
    out=[]
    for line in text.splitlines():
        s=line.strip()
        if s.startswith(("- [ ]","* [ ]")):
            out.append(s); continue
        if re.search(r"(@\s*faire|a\s*faire|todo|to\s*do|next\s*steps)", s, re.I):
            out.append(s)
    return out

def list_latest(p: Path, n=15):
    if not p.exists(): return []
    files=sorted([x for x in p.rglob("*") if x.is_file()], key=lambda x: x.stat().st_mtime, reverse=True)
    return [str(f) for f in files[:n]]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--student_archive", required=True)
    ap.add_argument("--out", required=True)
    args=ap.parse_args()

    repo=Path(args.repo)
    student=Path(args.student_archive)
    out=Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    stamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    journal_md = read_text(repo/"journal.md")
    dated=[]
    jdir=repo/"journal"
    if jdir.exists():
        for fp in sorted(jdir.glob("*.md")):
            dated.append(f"\n\n# {fp.name}\n" + read_text(fp))
    dated_txt="\n".join(dated)

    events = load_events(student/"events/events.ndjson", limit=1500)

    todos = extract_todos(journal_md) + extract_todos(dated_txt)
    for e in events[-600:]:
        t=f'{e.get("ts","")} [{e.get("module","")}] {e.get("title","")}: {e.get("message","")}'
        if any(k in t.lower() for k in ["@faire","a faire","todo","next","roadmap","audit","workflow","module","git_sync","sanity"]):
            todos.append(t)

    seen=set(); todos2=[]
    for t in [x.strip() for x in todos if x.strip()]:
        if t not in seen:
            seen.add(t); todos2.append(t)

    canon=out/"JOURNAL_CANON_FULL.md"
    todo=out/"TODO_CONSOLIDE_FULL.md"

    canon.write_text(
f"""# Journal Canon FULL — {stamp}

## Sources
- Repo: journal.md + journal/*.md
- Student archive bundle: events.ndjson + listings response/thinking/reports/audit

## Student archive: fichiers récents
### response (latest)
""" + "\n".join(list_latest(student/"response")) + """

### thinking (latest)
""" + "\n".join(list_latest(student/"thinking")) + """

## Timeline (events.ndjson — last 120)
""" + "\n".join([json.dumps(e, ensure_ascii=False) for e in events[-120:]]) + """

## journal.md (repo — head 300)
""" + "\n".join(journal_md.splitlines()[:300]) + """

## journaux datés (repo — head 200)
""" + "\n".join(dated_txt.splitlines()[:200]),
        encoding="utf-8"
    )

    todo.write_text("# TODO consolidé FULL (pending GO)\n\n" + "\n".join([f"- {t}" for t in todos2[:400]]), encoding="utf-8")
    print(str(canon))
    print(str(todo))

if __name__ == "__main__":
    main()
