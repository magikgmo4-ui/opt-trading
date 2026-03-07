# Desk Pro - Multi-Machine Quick Reference

| Action | admin-trading | student | db-layer |
|---|---|---|---|
| **Health Check** | `sanity-desk-pro` | `sanity-desk-pro-student` | `sanity-desk-pro-db` |
| **Status** | `desk-pro status` | `desk-pro-student status` | `desk-pro-db status` |
| **Menu** | `menu-desk-pro` | `menu-desk-pro-student` | `menu-desk-pro-db` |
| **Dernier Run** | `desk-pro-last-run` | `desk-pro-student-shared-info` | `desk-pro-db-shared-info` |
| **Exécution** | `desk-pro-run-logged` | N/A | N/A |
| **Logs** | `desk-pro-tail-log` | N/A | N/A |
| **Journal** | `desk-pro show-session-journal` | N/A | N/A |
| **Export** | `desk-pro-copy-latest` | N/A | N/A |

---
**Emplacements Clés**
- **Partage** : `/shared/desk_pro/latest/` (Mount sur student/db-layer, Source sur admin-trading)
- **Logs Admin** : `/opt/trading/data/logs/desk_pro/`
