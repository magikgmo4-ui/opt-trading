# 30_OPENCLAW_E2E_COMMAND_DISCOVERY

## Commandes decouvertes

| Commande | Pertinence E2E | Statut |
|---|---|---|
| `openclaw agent` | Commande principale pour un tour d'agent | Admissible |
| `openclaw gateway call` | Appels RPC gateway (health, status, cron) | Pas de methode prompt/model |
| `openclaw models` | Gestion modeles (set, list, status) | Pas de generate/run |
| `openclaw config` | Gestion config (get/set/unset) | Auxiliaire seulement |
| `openclaw tui` | Terminal UI interactive | Non utilisable sans TTY |

## Commande admissible

```
openclaw agent --to <E.164> --message <prompt> --json --timeout <s>
```

Options :
- `--to` : numero E.164 pour derivation de session (dummy accepte)
- `--message` : prompt texte
- `--json` : sortie JSON
- `--timeout` : timeout en secondes
- Sans `--deliver`, aucun envoi de message
- Sans `--channel`, pas de livraison WhatsApp/Telegram

## Risques
- `--local` exige des API keys shell (non utilisable)
- Gateway port config decale (18789 config vs 18790 reel)
- `auth-profiles.json` absent pour ollama (bloque l'utilisation du provider)

## Corrections necessaires avant E2E
1. Aligner `gateway.port` config sur 18790
2. Creer un profil auth minimal pour ollama (provider local, pas de vrai token)

## RISKS

- À qualifier.
