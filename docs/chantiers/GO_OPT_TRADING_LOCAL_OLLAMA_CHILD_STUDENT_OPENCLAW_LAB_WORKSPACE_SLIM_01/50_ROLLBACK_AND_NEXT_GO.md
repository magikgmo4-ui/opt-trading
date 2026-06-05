# 50_ROLLBACK_AND_NEXT_GO

## Rollback
- **Non execute** — tous les tests smoke passent, health OK, local-only confirme
- Backup complet disponible : `/home/openclaw-lab/openclaw_lab_backups/workspace_slim_01/`
- Rollback possible a tout moment :
  ```
  cp -a /home/openclaw-lab/openclaw_lab_backups/workspace_slim_01/main.bak/* /home/openclaw-lab/.openclaw/agents/main/
  cp /home/openclaw-lab/openclaw_lab_backups/workspace_slim_01/openclaw.json.bak /home/openclaw-lab/.openclaw/openclaw.json
  openclaw gateway stop && pkill openclaw-gateway
  restart gateway
  ```

## Config finale
```json
{
  "tools": {
    "profile": "minimal"
  },
  "agents": {
    "defaults": {
      "llm": { "idleTimeoutSeconds": 300 },
      "timeoutSeconds": 300
    }
  }
}
```

## Workspace final
- AGENTS.md : 150 chars
- SOUL.md : 59 chars
- BOOTSTRAP.md : 36 chars
- TOOLS.md : 44 chars
- IDENTITY.md : 50 chars
- USER.md : 37 chars
- HEARTBEAT.md : 22 chars

## Modele final actif
- `ollama/qwen2.5:3b-instruct`
- Provider : `ollama`

## Limites restantes
1. Skills (4837 chars) non desactivables — restent injectes dans le system prompt
2. Non-project context (~11,800 chars) est le plancher — OpenClaw internal prompt
3. Le modele qwen2.5:3b prend ~48s pour repondre a un prompt simple (acceptable, sous 180s)
4. Bonjour mDNS toujours actif sur le gateway (log "bonjour: advertised gateway")
5. SSH LAN direct (192.168.0.142) ne fonctionne plus — seul VPN (10.66.66.3) est accessible

## Next GO recommande
- Aucun next GO immediat — cet objectif est atteint
- Si besoin futur : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_BONJOUR_DISABLE` — desactiver l'annonce Bonjour/mDNS du gateway

## RISKS

- À qualifier.
