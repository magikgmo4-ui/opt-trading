# GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01

## Resume
Smoke E2E minimal OpenClaw → Ollama → deepseek-r1:1.5b sur student.

## Verdict
PASS

## Changements principaux
- E2E path confirme : `openclaw agent` → Gateway → ollama → deepseek-r1:1.5b → reponse recue
- `provider` confirme : `"ollama"` (pas anthropic)
- `missingProvidersInUse` : `["ollama"]` → `[]` (resolu via profil auth)
- `gateway.port` : `18790` (aligne config sur runtime)
- `auth-profiles.json` : cree avec profil ollama local
- Ollama direct baseline : OK
- Health : OK
- Local-only : confirme

## Limite
`deepseek-r1:1.5b` ne supporte pas le function calling (tools) — reponse `"does not support tools"`. Le chemin E2E est prouve mais le modele n'est pas adapte a un usage operationnel complet avec OpenClaw.

## Next GO
`GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_MODEL_EVALUATION_01`

## Dossier
`docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01/`
