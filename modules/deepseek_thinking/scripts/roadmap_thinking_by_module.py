import json, os, datetime, pathlib, subprocess, tempfile

EVENTS = "/opt/trading/_student_archive/events/events.ndjson"
MODEL  = os.environ.get("DEEPSEEK_MODEL", "deepseek-r1:1.5b")
MOD    = os.environ.get("MOD", "desk_pro")
N      = int(os.environ.get("EVENT_N", "40"))
OUTDIR = f"/opt/trading/_student_archive/thinking/{MOD}"

def load_tail_filtered(mod: str, n: int):
    items = []
    try:
        with open(EVENTS, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                if str(o.get("module", "")) == mod:
                    items.append(o)
    except FileNotFoundError:
        return []
    return items[-n:]

events = load_tail_filtered(MOD, N)

prompt = (
    "RÉPONDS EN FRANÇAIS. THINKING UNIQUEMENT.\n"
    "Tu es l'assistant ROADMAP (raisonnement). Donne le raisonnement détaillé en Markdown.\n"
    "Règles: structuré, technique, étapes.\n"
    "Sections: Hypothèses, Analyse des événements, Ce qui manque, Plan détaillé, Risques, Tests/validation.\n"
    f"MODULE: {MOD} | N_EVENTS: {N}\n\n"
    "EVENEMENTS(JSON):\n" + json.dumps(events, ensure_ascii=False)
)

pathlib.Path(OUTDIR).mkdir(parents=True, exist_ok=True)
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
outf = f"{OUTDIR}/roadmap_thinking_{ts}.md"

payload = json.dumps({
    "model": MODEL,
    "prompt": prompt,
    "stream": False,
    "options": {"num_predict": 600}
})

tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
tmp.close()

try:
    subprocess.run(
        ["timeout", "300s", "curl", "-sS", "http://127.0.0.1:11434/api/generate", "-d", payload],
        check=False,
        stdout=open(tmp.name, "w", encoding="utf-8")
    )
    raw = open(tmp.name, "r", encoding="utf-8").read().strip()
    data = json.loads(raw) if raw else {}
    thinking = (data.get("thinking") or "").strip()
    open(outf, "w", encoding="utf-8").write((thinking if thinking else "# EMPTY_THINKING\n") + "\n")
    print(outf)
finally:
    try:
        os.unlink(tmp.name)
    except Exception:
        pass
