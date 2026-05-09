# vision_bot (Bot Vision) — Inbox/Outbox via ShareX (Windows) + SFTP (admin-trading)

Objectif: permettre à Windows (ShareX) d'envoyer des captures d'écran vers **admin-trading** (headless) via SFTP,
puis générer une sortie **.md** (et éventuellement JSON) dans un dossier outbox.

Le module est **fonctionnel sans API**:
- Engine par défaut: **OCR (tesseract CLI si présent)** → extrait du texte de la capture
- Sinon fallback: **dummy** (placeholder)

Ensuite, tu peux brancher n'importe quel "moteur" via `VISION_BOT_ENGINE=shell` + une commande custom (ex: ollama llava, curl OpenAI, etc.).

## Dossiers (par défaut)
- Inbox  : `/srv/sftp/shared_files/shared/vision_inbox`
- Outbox : `/srv/sftp/shared_files/shared/vision_outbox`
- Processed: `/srv/sftp/shared_files/shared/vision_processed`
- Logs   : `/opt/trading/_work/vision_bot/vision_bot.log`
- State  : `/opt/trading/_work/vision_bot/state.json`

## Installation (sur admin-trading)
1) Dézipper le patch à la racine du repo:
   ```bash
   cd /opt/trading
   unzip -o /srv/sftp/shared_files/shared/<ZIP>   # ou scp puis unzip
   ```

2) Installer les raccourcis globaux:
   ```bash
   sudo bash modules/vision_bot/scripts/install_shortcuts.sh
   ```

3) Initialiser dossiers inbox/outbox:
   ```bash
   cmd-vision_bot init
   ```

4) Sanity check:
   ```bash
   sanity-vision_bot
   ```

## Usage
- Traitement 1 passe (recommandé au début):
  ```bash
  cmd-vision_bot run_once
  ```

- Mode "watch" (boucle polling):
  ```bash
  cmd-vision_bot watch
  # logs:
  cmd-vision_bot tail
  ```

## Wrapper unifié de chaîne

Le lot `VISION_RUNTIME_CONSOLIDATION_IMPL_01` ajoute un point d'entree pair-safe :

```bash
cmd-vision sanity
cmd-vision paths
cmd-vision status
cmd-vision capture-once
cmd-vision analyze-latest
menu-vision
```

Ce wrapper n'efface ni `cmd-vision_bot` ni `cmd-bot_vision_step2`.
Il orchestre simplement la paire canonique transitoire sans changer les services.

## ShareX (Windows) — envoi des captures
Dans ShareX:
- Destinations -> Custom uploader -> **SFTP**
- Host: IP de `admin-trading`
- User: `ghost` (ou ton user SFTP)
- Key: ta clé SSH
- Remote folder: `/srv/sftp/shared_files/shared/vision_inbox`
- Nom fichier conseillé: `{yyyy}-{MM}-{dd}_{HH}-{mm}-{ss}_{rn:6}.png`

Résultats: ouvrir `/srv/sftp/shared_files/shared/vision_outbox` via WinSCP/SFTP.

## Config (optionnel)
Variables (env) supportées (avec defaults):
- `VISION_BOT_INBOX`
- `VISION_BOT_OUTBOX`
- `VISION_BOT_PROCESSED`
- `VISION_BOT_ENGINE` = `ocr` | `dummy` | `shell`
- `VISION_BOT_POLL_SEC` (watch loop) = 2
- `VISION_BOT_PROMPT_DEFAULT` (si engine shell)
- `VISION_BOT_SHELL_CMD` (si engine shell) — placeholders: `{image}` `{prompt}`

Exemple engine shell (à adapter selon ton outil):
```bash
export VISION_BOT_ENGINE=shell
export VISION_BOT_SHELL_CMD='ollama run llava "Analyse ce screenshot: {prompt}" --image "{image}"'
```
(commande juste illustrative — ajuste au CLI exact sur ta machine)

## Notes sécurité
- Le module ne supprime pas les fichiers par défaut: il les déplace vers `vision_processed`.
- Les outputs sont écrits dans l’outbox sous forme `.md` + `.txt` (texte brut).

## Statut de famille
- `vision_bot` est retenu comme point d'entree capture / inbox-outbox de la chaine operatoire transitoire
- il opere avec `bot_vision_step2`, qui porte l'analyse Vision / Telegram et la generation d'artefacts
- `bot_vision` reste la verticale historique `step1`
