# OT-SVC-01 — REPORT

## 1. MÉTHODOLOGIE
Audit des modules `registry` et des dossiers `systemd/` réels pour cartographier les modes d'exécution.

## 2. DÉCOUVERTES
- La majorité des modules sont **ON-DEMAND** (CLI/Scripts).
- Seuls 3 modules sont conçus pour être résidents (Services/Timers) :
    1.  `vision_bot` (Service Watch)
    2.  `desk_retention` (Timer 10min)
    3.  `shared_sshfs_permanent` (Service SSHFS foreground)

## 3. POINT D'ATTENTION
- `shared_sshfs_permanent` utilise une approche "Service" (`sshfs -f`) au lieu de "Mount Unit". C'est fonctionnel mais moins standard pour Systemd.
- `desk_snapshot_ingest` a le code pour être un service (Watch loop) mais pas le fichier `.service` dans le repo.

## 4. CONCLUSION
La distinction est claire :
- **Outils Opérateur & Moteurs** = ON-DEMAND.
- **Monitoring & Infra** = SERVICE/TIMER.

Cette clarté permet de simplifier les runbooks (pas besoin de vérifier `systemctl status` pour un moteur de probabilité, par exemple).

**Status : MAP ÉTABLIE.**
