---
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_REAL_RUNS_VALIDATION_01
doc_type: runbook
repo: opt-trading
status: open
created_at: 2026-05-23
---

# 10_RUNBOOK_STAGING

---

## 1_PRÉREQUIS

### Environnement Python

```bash
source venv/bin/activate
pip install playwright openai
playwright install chromium
```

### Variables d'environnement

```bash
export VISION_BOT_ENABLED=true
export VISION_AI_PROVIDER=openai
export OPENAI_API_KEY=<clé OpenAI>
```

Les clés API ne vont jamais dans le code — `.env` ou export shell uniquement.

### Répertoires de données

Créés automatiquement par `ensure_dirs()` au démarrage du script.
Chemin attendu : `data/vision/coinglass/` (raw/, normalized/, latest.json, events.jsonl)
Et : `data/deskpro/inputs/vision_context/coinglass/latest.json`

---

## 2_SÉQUENCE_RUNS

Exécuter 3 captures successives. Laisser ≥ 30 secondes entre chaque run
pour éviter le rate-limiting OpenAI Vision.

### Run 1

```bash
VISION_BOT_ENABLED=true \
VISION_AI_PROVIDER=openai \
OPENAI_API_KEY=$OPENAI_API_KEY \
python scripts/run_vision_capture.py
```

Vérifier la sortie :
```
capture DONE — N detections, freshness=fresh
```

### Run 2

Répéter la même commande.

### Run 3

```bash
VISION_BOT_ENABLED=true \
VISION_AI_PROVIDER=openai \
OPENAI_API_KEY=$OPENAI_API_KEY \
python scripts/run_vision_capture.py
```

### Avec Telegram (optionnel, --send)

```bash
VISION_BOT_ENABLED=true \
VISION_AI_PROVIDER=openai \
OPENAI_API_KEY=$OPENAI_API_KEY \
python scripts/run_vision_capture.py --send
```

---

## 3_VALIDATION

Après les 3 runs :

```bash
VISION_BOT_ENABLED=true \
python scripts/run_vision_capture.py --validate --required 3
```

Sortie attendue (exit 0) :
```
[validate] PASS — 3/3 runs qualified
  2026-05-23T...  PASS  ok
  2026-05-23T...  PASS  ok
  2026-05-23T...  PASS  ok
```

Critère PASS par run :
- ≥ 1 detection avec `confidence ≥ 0.60`
- `extracted_value` non-null
- `screenshot_ts` présent

---

## 4_VÉRIFICATION_DESK_PRO

Le service Perf Analytics (port 8010) doit être actif.

```bash
# Démarrer si nécessaire
python3 perf/perf_app.py &

# Vérifier l'endpoint vision
curl -s http://127.0.0.1:8010/desk/vision | python3 -m json.tool
```

Réponse attendue :
```json
{
  "ok": true,
  "vision": { "symbol": "BTCUSDT", "detections": [...], ... },
  "age_hours": 0.05
}
```

```bash
# Vérifier la présence du panel dans l'UI
curl -s http://127.0.0.1:8010/desk/ui | grep -i "Coinglass Vision"
```

---

## 5_VÉRIFICATION_FICHIERS

Après 3 runs, les fichiers suivants doivent exister :

```bash
# Screenshots bruts (1 par run)
ls data/vision/coinglass/raw/screenshot_*.png

# Normalisés (1 par run)
ls data/vision/coinglass/normalized/vision_*.json

# Latest (dernier run)
cat data/vision/coinglass/latest.json | python3 -m json.tool | head -20

# Events (3 entrées minimum)
wc -l data/vision/coinglass/events.jsonl
cat data/vision/coinglass/events.jsonl | tail -3

# Desk Pro input
cat data/deskpro/inputs/vision_context/coinglass/latest.json | python3 -m json.tool | head -10
```

---

## 6_CRITÈRES_ABORT

Stopper et documenter dans `20_RUN_EVIDENCE.md` si :
- Playwright ne peut pas charger coinglass.com (réseau, geo-block)
- OpenAI Vision retourne une erreur répétée (quota, clé invalide)
- 0 detections sur 2 runs consécutifs
- `--validate` retourne exit 1 après 5 tentatives

Dans ce cas : conserver les fichiers produits, documenter l'état dans
`90_REPRISE_POINT.md`, et rouvrir la session staging ultérieurement.

---

## 7_PARAMÈTRES_OPTIONNELS

```bash
# Symbole différent
python scripts/run_vision_capture.py --symbol ETHUSDT --timeframe 4H

# Attente Playwright plus longue (réseau lent)
python scripts/run_vision_capture.py --wait-ms 8000

# Logging verbose
LOG_LEVEL=DEBUG python scripts/run_vision_capture.py
```
