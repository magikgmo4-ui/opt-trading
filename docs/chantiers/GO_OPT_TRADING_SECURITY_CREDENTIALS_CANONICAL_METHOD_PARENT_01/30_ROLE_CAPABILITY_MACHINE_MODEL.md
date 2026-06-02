# Role, Capability & Machine Model

## Machine Model
Chaque machine (ex: `fantome`, `admin-trading`) possède une liste de rôles assignés.
- `fantome`: `telegram_collector`, `git_dev`
- `admin-trading`: `datacenter`, `market_data_readonly`

## Role & Capability
Un rôle regroupe un ensemble de secrets (capabilities).
- Rôle `telegram_collector` -> accès à `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_BOT_TOKEN`.

## Job requirements
Chaque job script déclare ses besoins :
```yaml
job: telegram_collect_channel
requires_role: telegram_collector
```
