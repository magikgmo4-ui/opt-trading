# 10_PRE_SMOKE_STATE

## OpenClaw
- version : `2026.4.2 (d74a122)`
- user : `openclaw-lab`
- host : `student`

## Model status
```json
{
  "defaultModel": "ollama/deepseek-r1:1.5b",
  "resolvedDefault": "ollama/deepseek-r1:1.5b",
  "missingProvidersInUse": ["ollama"]
}
```

## Processus
```
openclaw-gateway  131763  Ssl  22:43  openclaw-gateway
```
Le gateway tourne en processus unique.

## tmux
Aucune session tmux active.

## Ports / listeners
```
LISTEN 127.0.0.1:18790 (gateway)
LISTEN 127.0.0.1:18792 (side-port)
LISTEN 127.0.0.1:11434 (Ollama)
LISTEN [::1]:18790     (gateway IPv6)
```
Tous loopback-only.

## Config gateway
- `gateway.port` : non defini (default 18789)
- `gateway.auth` : token mode
- Port reel du processus : 18790 (decalage vs config)

## RISKS

- À qualifier.
