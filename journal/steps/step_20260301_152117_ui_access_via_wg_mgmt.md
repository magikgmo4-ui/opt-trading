# Step — UI access via wg-mgmt (2026-03-01)
Objectif: utiliser wg-mgmt (10.66.66.1) pour accéder aux UIs (port 8010) depuis db-layer/MSI.
Constat: ping OK. curl -I donne 405 car HEAD non supporté (GET only) -> attendu.
Next: valider GET 200 sur /perf/ui, /desk/ui, /desk/toolbox + ouvrir dans navigateur.
