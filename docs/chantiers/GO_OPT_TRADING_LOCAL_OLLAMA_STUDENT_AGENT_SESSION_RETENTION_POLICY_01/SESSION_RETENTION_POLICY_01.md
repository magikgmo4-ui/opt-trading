# SESSION_RETENTION_POLICY_01

Gestion des sessions agent OpenClaw / Ollama local CPU sur Student.

## Contexte

- Runtime local : `ollama/qwen2.5:0.5b-instruct` via Ollama CPU
- Contexte Ollama : `n_ctx=4096` tokens
- System prompt OpenClaw : ~3500 tokens
- Budget historique par session : ~600 tokens
- Au-delà : overflow → timeout silencieux

## Règles

### 1. Rotation de session

| Seuil | Action |
|-------|--------|
| > 10 runs | Archiver la session, en créer une nouvelle |
| > 7 jours | Rotation forcée même si < 10 runs |
| overflow détecté | Rotation immédiate |

### 2. Purge automatique

- Sessions archivées conservées 30 jours dans `/tmp/opencode/`
- Supprimer toute session avec `PROMPT_ERROR` en rafale (> 3 consécutifs)
- Ne pas conserver de session avec `input tokens = 0`

### 3. Détection overflow

Signes :
- `input: 0, output: 0` dans les métriques agent
- `"request timed out"` dans les logs gateway
- `n_ctx_seq (4096) < n_ctx_train (32768)` confirmé dans les logs Ollama

### 4. Seuils recommandés

| Métrique | Seuil d'alerte | Seuil critique |
|----------|:-------------:|:--------------:|
| Input tokens par run | > 3500 | > 3800 |
| Historique cumulé | > 500 tokens | > 600 tokens |
| Runs par session | > 8 | > 10 |
| PROMPT_ERROR consécutifs | 1 | 3 |

### 5. Smoke après purge

- Créer session vierge (archiver la courante si besoin)
- Prewarm : `curl /api/generate -d '{"model":"qwen2.5:0.5b-instruct","prompt":"warm"}'`
- Cold smoke : `openclaw agent --agent main --message "..."`
- Vérifier `durationMs < 180000`
- Si cold smoke FAIL après rotation → diagnostique provider, pas session

## Procédure de diagnostic session bloquée

1. `sudo cat /home/openclaw-lab/.openclaw/agents/main/sessions/<sessionId>.jsonl` | grep PROMPT_ERROR
2. Si > 3 PROMPT_ERROR consécutifs → archiver et forcer nouvelle session
3. Vérifier `input tokens = 0` dans les métriques
4. Vérifier n_ctx dans les logs Ollama
5. Après correction : relancer cold smoke

## Critères PASS/FAIL

| Critère | PASS | FAIL |
|---------|:----:|:----:|
| Runs avant rotation | ≤ 10 | > 10 |
| PROMPT_ERROR consécutifs | 0 | ≥ 3 |
| Input tokens | > 0 | = 0 |
| Cold smoke après rotation | < 180s | timeout |
| Warm smoke | < 60s | timeout |

## RISKS

- À qualifier.
