# Registry Schema Draft

## credentials.yaml
```yaml
credentials:
  - id: telegram_bot_token_main
    provider: telegram
    type: api_token
    env_var: TELEGRAM_BOT_TOKEN
    validation: "^[0-9]+:[a-zA-Z0-9_-]+$"
    rotation_policy: 90d
```

## roles.yaml
```yaml
roles:
  - id: telegram_collector
    credentials:
      - telegram_bot_token_main
      - telegram_api_id
      - telegram_api_hash
```

## machines.yaml
```yaml
machines:
  - id: fantome
    roles:
      - telegram_collector
      - git_dev
```
