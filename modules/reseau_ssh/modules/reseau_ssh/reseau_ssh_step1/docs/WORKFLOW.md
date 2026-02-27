## Workflow (reseau_ssh)

Rules:
- One step = files delivered + short commands + minimal logs + journal update.
- Every module must ship: sanity_check.sh, *_cmd.sh, *_menu.sh.
- Always push Git + pass through Cursor AI + validate on student.

Step 1:
- Inventory + baseline validation (non-destructive)

Step 1b:
- Apply hostname normalization (unique hostnames) + SSH aliases everywhere
- Enable key-based auth full-mesh (or at least admin-trading -> all)

Step 2:
- WireGuard server/client configs + firewall rules
