# First Run Smoke Plan

Pour tester le fonctionnement sans exposer de secrets :

1.  **Mock Env** : Exporter des valeurs bidon dans le shell actuel.
    ```bash
    export TELEGRAM_API_ID=123
    export TELEGRAM_API_HASH=abc
    export TELEGRAM_BOT_TOKEN=bot123
    export TELEGRAM_SESSION_PATH=/tmp/mock.session
    ```
2.  **Validator Run** :
    ```bash
    python3 scripts/env/validate_credentials.py --machine fantome --job telegram_collect_channel
    ```
3.  **App Logic Check** : Vérifier que l'application (ex: `e2e_telegram_smoke.py`) utilise bien `os.getenv` ou le resolver pour charger ces variables.
