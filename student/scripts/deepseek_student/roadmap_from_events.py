import json, os, datetime, pathlib, subprocess

EVENTS="/opt/trading/_student_archive/events/events.ndjson"
OUTDIR="/opt/trading/_student_archive/roadmap"
MODEL=os.environ.get("DEEPSEEK_MODEL","deepseek-r1:1.5b")
N=int(os.environ.get("EVENT_N","200"))

def tail(n):
  a=[]
  try:
    with open(EVENTS,"r",encoding="utf-8") as f:
      for line in f:
        line=line.strip()
        if not line: continue
        try: a.append(json.loads(line))
        except: pass
  except FileNotFoundError:
    return []
  return a[-n:]

events=tail(N)
prompt="Tu es \"DeepSeek étudiant\". Réponds en FRANÇAIS.\n" \
"Fais une ROADMAP Markdown: Contexte, Etat actuel, Modules, Roadmap(MVP->V1->V2), Risques, Checklist.\n\n" \
"EVENEMENTS(JSON):\n"+json.dumps(events, ensure_ascii=False)

pathlib.Path(OUTDIR).mkdir(parents=True, exist_ok=True)
ts=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
outf=f"{OUTDIR}/roadmap_{ts}.md"

payload=json.dumps({"model":MODEL,"prompt":prompt,"stream":False})
res=subprocess.run(["curl","-sS","http://127.0.0.1:11434/api/generate","-d",payload],capture_output=True,text=True)
out=(res.stdout or "").strip()
try:
  data=json.loads(out) if out else {}
  text=(data.get("response") or out or (res.stderr or "")).strip()
except:
  text=out or (res.stderr or "")
open(outf,"w",encoding="utf-8").write(text+"\n")
print(outf)
