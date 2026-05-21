---
doc_id: GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01_POLICY
doc_type: security_policy
go_id: GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01
status: draft
---

# 50_DENY_BY_DEFAULT.md

## Principe deny-by-default

Toute action automatisée est refusée sauf si explicitement autorisée par :

1. Une règle dans la permission matrix (G01)
2. Un approval HITL valide (G07)
3. Un app bridge contract (G04)
4. Un job packet explicite pour read-only workers (G02)

## Règles

```yaml
deny_by_default:
  enabled: true
  exceptions:
    - lecture seule (READ_*) toujours autorisée
    - dry-run toujours autorisé (ne modifie rien)
    - actions L0-L2 en mode NORMAL
  blocked:
    - écriture sans approval HITL
    - écriture sans contrat bridge
    - tout write_gated sans dual confirm pour L6+
    - accès API sans scope OAuth défini (30_OAUTH_SCOPES.md)
```

## Enforcement

- Appliqué par chaque worker avant exécution
- Checké avant chaque write_gated
- Loggé dans le ledger (G06) avec status BLOCKED
