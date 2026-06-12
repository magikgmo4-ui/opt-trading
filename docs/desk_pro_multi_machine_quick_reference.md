# Desk Pro - Multi-Machine Quick Reference

## Commandes clés par machine
| Action | admin-trading | student | db-layer |
|---|---|---|---|
| **Health Check** | `sanity-desk-pro` | `sanity-desk-pro-student` | `sanity-desk-pro-db` |
| **Status** | `desk-pro status` | `desk-pro-student status` | `desk-pro-db status` |
| **Menu** | `menu-desk-pro` | `menu-desk-pro-student` | `menu-desk-pro-db` |
| **Dernier Run** | `desk-pro-last-run` | `desk-pro-student-shared-info` | `desk-pro-db-shared-info` |
| **Exécution** | `desk-pro-run-logged` | N/A | N/A |
| **Logs** | `desk-pro-tail-log` | N/A | N/A |
| **Export** | `desk-pro-copy-latest` | N/A | N/A |

---
## UI URLs — Source of Truth

### Access from db-layer / MSI (wg-mgmt)
- Perf UI: `http://10.66.66.1:8010/perf/ui`
- Desk Pro UI: `http://10.66.66.1:8010/desk/ui`
- Desk Pro Toolbox UI: `http://10.66.66.1:8010/desk/toolbox`

### Notes
- `curl -I` peut retourner `405 Method Not Allowed`; utiliser un `GET`.
- Le port `8000` correspond à `tv-webhook` et à sa doc, pas à l'hébergement UI.
- Le port `8501` n'est pas utilisé dans cette stack.

---
**Emplacements Clés**
- **Partage** : `/shared/desk_pro/latest/` (Mount sur student/db-layer, Source sur admin-trading)
- **Logs Admin** : `/opt/trading/data/logs/desk_pro/`

## RISKS

- À qualifier.
