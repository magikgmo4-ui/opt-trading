# 50_LIMITS_AND_NEXT_GO

## Limites restantes
- `deepseek-r1:1.5b` ne supporte pas le function calling (tools) — OpenClaw attend des outils, ce qui limite l'utilite operationnelle du modele
- Le profil auth ollama est un api_key dummy (pas de vrai mecanisme d'auth — acceptable car Ollama est local sans auth)
- `gateway.port` a du etre aligne manuellement (18790) — le port par defaut 18789 n'etait pas celui du processus
- `auth-profiles.json` a du etre cree manuellement — le dry-run et le switch apply n'avaient pas anticipe cette dependance
- Pas de trading reel
- Pas d'orchestrator
- Pas de listener LAN
- `db-layer` et `admin-trading` hors perimetre
- `missingProvidersInUse` est desormais vide `[]` — le profil auth a resolu le statut missing

## Signification de missingProvidersInUse ["ollama"] (resolu)
Avant creation du profil auth, `ollama` apparaissait dans `missingProvidersInUse` avec status `missing`. Cela signifiait qu'OpenClaw ne trouvait pas de credentials pour le provider ollama, meme si Ollama n'exige pas d'auth. La creation d'un profil `api_key` (meme avec une cle dummy) a suffi a resoudre ce statut.

## Next GO recommande
`GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_MODEL_EVALUATION_01`

Objectif : evaluer les modeles Ollama disponibles compatibles avec le function calling pour une utilisation operationnelle avec OpenClaw. Identifier un modele candidat plus adapte que deepseek-r1:1.5b.

## RISKS

- À qualifier.
