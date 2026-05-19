# 60_PRODUCT_DEEP_RESEARCH

## 1_OBJECTIF
Comparer les produits utilisables pour construire une surface opérateur Android/IDE autour de `opt-trading`.

Le critère principal n'est pas le confort général, mais la capacité à soutenir ce flux:

```txt
Android tablet
-> operator UI / automation
-> Termux or SSH client
-> SSH
-> tmux
-> db-layer / admin-trading / cursor-ai / student
-> OpenClaw / OpenCode / trading infra
```

## 2_CRITERIA

| Critère | Sens pour le projet |
|---|---|
| SSH | Peut atteindre les machines sans runtime local lourd |
| tmux | Peut reprendre une session persistante |
| Offline/LAN | Utilisable sans dépendre d'un cloud tiers |
| Android background | Résiste aux politiques batterie/reboot |
| Sécurité | Évite secrets en clair et actions destructives directes |
| Debug | Permet de voir stdout/stderr/exit code ou état équivalent |
| UX cockpit | Boutons, profils, layouts opérateur |
| Maintenance | Facilité à documenter/reprendre dans IDE |

## 3_PRODUCT_MATRIX

| Produit | Rôle retenu | Forces | Limites | Verdict |
|---|---|---|---|---|
| Termux | shell Android + SSH | offline, scriptable, SSH/tmux natif | contraintes batterie, permissions Android | RETAIN V1 |
| Termux:Tasker | pont Tasker -> Termux | exécution scriptée, retours `%stdout/%stderr/%result` | permissions RUN_COMMAND, timeouts | RETAIN V1 |
| Tasker | orchestrateur Android | variables, conditions, profils, widgets | complexité, risque d'automations opaques | RETAIN V1/V2 |
| MacroDroid | automation simple | rapide, notifications, triggers faciles | moins flexible que Tasker | RETAIN V2 support |
| Unified Remote | raccourcis tactiles | simple, clavier/souris, boutons | pas une couche SSH/tmux robuste | OPTIONAL UI |
| Stream Deck Mobile | cockpit visuel | profils, boutons, UX opérateur | dépendance app/écosystème | RETAIN V2/V3 |
| Termius | SSH client dédié | multi-host propre, confort | moins scriptable que Termux | OPTIONAL fallback |
| RustDesk/RDP | visuel distant | utile pour UI ponctuelle | pas fait pour orchestration persistante | OPTIONAL visual |
| LocalCMS/Web UI | cockpit custom | alignable projet, extensible | nécessite implémentation | V3/PRO |

## 4_BENCHMARKS_REELS_A_FAIRE

Les benchmarks doivent rester non destructifs et reproductibles.

### 4.1 Latence opérateur
```bash
time ssh db-layer 'echo ok'
time ssh admin-trading 'tmux ls >/dev/null || true'
```

### 4.2 Résilience tmux
```bash
ssh db-layer 'tmux new -d -s android_probe || true; tmux ls; tmux kill-session -t android_probe || true'
```

### 4.3 Recovery Android
- reboot Android;
- ouvrir Termux;
- lancer `ssh db-layer 'echo ok'`;
- lancer `ssh db-layer 'tmux ls || true'`;
- noter délai de reprise.

### 4.4 Automation Tasker
Mesurer:
- délai bouton -> script Termux;
- présence `%stdout`;
- présence `%stderr`;
- `%result == 0` attendu sur health check.

## 5_SECURITY_NOTES

- Ne pas stocker de passphrase SSH dans Tasker.
- Ne pas exposer restart/kill sans confirmation.
- Séparer `READ_ONLY` et `WRITE_GATED`.
- Préférer scripts versionnés à commandes inline.
- Garder Android comme console opérateur, jamais runtime trading.

## 6_SELECTED_STACK

### V1
```txt
Termux + OpenSSH + tmux commands + Tasker + Termux:Tasker
```

### V2
```txt
V1 + MacroDroid notifications + Stream Deck Mobile / Unified Remote shortcuts
```

### V3_PRO
```txt
V2 + LocalCMS/Web cockpit + OpenClaw operator layer + status panels
```

## 7_FINAL_VERDICT

La meilleure pile projet est:

```txt
Termux = exécution
Tasker = orchestration Android
tmux = persistance
Stream Deck / Unified Remote = UI opérateur
LocalCMS/Web UI = cockpit PRO futur
```

Unified Remote reste utile comme panneau de raccourcis, mais ne doit pas devenir la colonne vertébrale du système.