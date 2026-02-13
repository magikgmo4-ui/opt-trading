#!/usr/bin/env python3
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from openai import OpenAI

JOURNAL_PATH = os.environ.get("JOURNAL_PATH", "/opt/trading/journal.md")
TZ_NAME = os.environ.get("JOURNAL_TZ", "America/Montreal")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.2")

SYSTEM = """Tu es un assistant de journalisation.
Transforme un dump brut d'une conversation ChatGPT en une entrée de journal de bord concise, actionnable et fidèle.

Format STRICT (Markdown) :

## <YYYY-MM-DD HH:MM> — <TITRE>
1) Objectifs:
2) Actions:
3) Décisions:
4) Commandes / Code:
5) Points ouverts (next):

Règles:
- Français.
- Factuel, fidèle au texte.
- Pas de blabla.
- Si une section est vide: écrire "—".
- Commandes/code en blocs ``` quand pertinent.
"""

def now_local() -> str:
    tz = ZoneInfo(TZ_NAME)
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M")

def main():
    if len(sys.argv) < 2:
        print('Usage: journal_from_paste.py "Titre de session"   (puis coller le chat, Ctrl-D)')
        sys.exit(2)

    title = sys.argv[1].strip()
    raw = sys.stdin.read().strip()

    if not raw:
        print("Aucun texte reçu. Colle le chat puis Ctrl-D.")
        sys.exit(1)

    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY non défini. Exemple: export OPENAI_API_KEY='sk-...'\n")
        sys.exit(1)

    ts = now_local()

    prompt = f"""TITRE: {title}
DATE: {ts} ({TZ_NAME})

CONVERSATION (brut):
{raw}
"""

    client = OpenAI()
    resp = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
    )

    entry = (getattr(resp, "output_text", "") or "").strip()
    if not entry:
        print("Réponse vide reçue de l'API.")
        sys.exit(1)

    os.makedirs(os.path.dirname(JOURNAL_PATH), exist_ok=True)
    with open(JOURNAL_PATH, "a", encoding="utf-8") as f:
        f.write("\n" + entry + "\n")

    print(f"✅ Journal mis à jour: {JOURNAL_PATH}")

if __name__ == "__main__":
    main()
