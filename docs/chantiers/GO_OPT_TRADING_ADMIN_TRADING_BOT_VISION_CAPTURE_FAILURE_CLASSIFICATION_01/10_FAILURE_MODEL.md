# 10_FAILURE_MODEL

## Status

| Status           | Description                                      |
| ---------------- | ------------------------------------------------ |
| `ready`          | Capture réussie et visuellement exploitable      |
| `blocked`        | Timeout ou erreur technique avant screenshot     |
| `invalid_visual` | Screenshot réussi mais contenu inexploitable     |

## Blocked reasons

| Reason                 | Déclencheur                           |
| ---------------------- | ------------------------------------- |
| `PAGE_GOTO_TIMEOUT`    | page.goto() dépasse le timeout_ms     |
| `PAGE_GOTO_ERROR`      | page.goto() échoue (DNS, SSL, etc.)   |
| `SCREENSHOT_ERROR`     | page.screenshot() échoue              |
| `OUTPUT_WRITE_ERROR`   | Écriture du PNG sur disque échoue     |

## Visual status

| Status                    | Déclencheur                                   |
| ------------------------- | --------------------------------------------- |
| `unchecked`               | Vérification visuelle désactivée              |
| `pass`                    | Tous les checks passent                       |
| `too_small`               | Fichier PNG < 1 KB                            |
| `blank_or_uniform`        | PNG < 15 KB (uniforme possible)               |
| `loading_state_detected`  | DOM contient "loading"/"spinner"/etc.         |
| `possible_spinner`        | document.readyState !== "complete"            |
