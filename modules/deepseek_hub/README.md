# deepseek_hub — Menu unifié DeepSeek (Ollama)

## Objectif
- Un **menu unique** avec toutes les commandes utiles (thinking/response/events/logs/models/pull).
- Corrige les anciens modules:
  - `deepseek_thinking`: ajoute `tail`, et bascule sur `/api/chat` (champ `message.thinking` fiable)
  - `deepseek_response`: ajoute `tail`, et bascule sur `/api/chat`

## Contenu
- `modules/deepseek_hub/scripts/`
  - `deepseek_hub_menu.sh`   → menu unifié
  - `deepseek_hub_cmd.sh`    → commandes unifiées
  - `sanity_check_deepseek_hub.sh`
  - `apply_patches.sh`       → backup + patch des cmd existants
  - `install_shortcuts.sh`   → symlinks /usr/local/bin

- `modules/deepseek_hub/patches/`
  - `deepseek_thinking_cmd.sh`
  - `deepseek_response_cmd.sh`

## Installation (admin-trading recommandé)
1) Dézipper le bundle dans `/opt/trading` (merge safe).
2) Appliquer patch:
   - `bash /opt/trading/modules/deepseek_hub/scripts/apply_patches.sh`
3) Installer les raccourcis:
   - `MAKE_DEFAULT=1 bash /opt/trading/modules/deepseek_hub/scripts/install_shortcuts.sh`
4) Sanity:
   - `sanity-deepseek_hub`
5) Lancer:
   - `menu-deepseek` (si MAKE_DEFAULT=1) ou `menu-deepseek_hub`

## Rollback
- Les fichiers originaux patchés sont copiés dans:
  - `/opt/trading/_student_archive/workflow/patch_backups/deepseek_hub_<timestamp>/`

Pour revenir en arrière:
- `sudo install -m 0755 <backup>/deepseek_thinking_cmd.sh /opt/trading/modules/deepseek_thinking/scripts/deepseek_thinking_cmd.sh`
- `sudo install -m 0755 <backup>/deepseek_response_cmd.sh /opt/trading/modules/deepseek_response/scripts/deepseek_response_cmd.sh`
