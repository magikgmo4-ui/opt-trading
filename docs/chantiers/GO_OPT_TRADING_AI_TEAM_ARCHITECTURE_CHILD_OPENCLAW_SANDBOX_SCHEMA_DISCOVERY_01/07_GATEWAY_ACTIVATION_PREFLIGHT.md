# 07_GATEWAY_ACTIVATION_PREFLIGHT

## Objectif

Préparer le preflight d'activation gateway OpenClaw avec la configuration effective V2 actuelle, sans migration brute de la configuration repo V1.2.1.

## Source

- `06_TOOL_POLICY_DEPLOYMENT_RISK_MATRIX.md`

## Verdict source

```text
DEPLOYMENT_NO_GO_FOR_V121_RAW
SELECTED_DIRECTION = GATEWAY_PREFLIGHT_ON_DEPLOYED_V2
```

## Runtime lock

```text
NO_OPENCLAW_RUNTIME
NO_GATEWAY_START_YET
NO_REMOTE_COMMAND
NO_SSH_CONNECTION
READ_ONLY_PREFLIGHT_ONLY
```

---

## Audit local — résultats

### Git precheck

```text
Branch: go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_SANDBOX_SCHEMA_DISCOVERY_01
HEAD: f599e7de
Status: propre
```

### Config V2 effective — structure

```text
top_keys: ['agents', 'auth', 'commands', 'gateway', 'messages', 'meta', 'tools', 'wizard']
gateway.mode: local
gateway.port: not set → défaut 18789
gateway.bind: not set → défaut loopback
gateway.auth.mode: token
gateway.token_present: true [REDACTED]
agents_count: 4
tools_keys: ['web']
```

### Gateway command discovery

```text
CLI : /home/ghost/.npm-global/bin/openclaw 2026.3.11
Subcommand gateway disponible : OUI
```

Commandes clés identifiées :

| Commande | Effet |
| :--- | :--- |
| `openclaw gateway run` | démarre en foreground (pas de service) |
| `openclaw gateway start` | démarre via service systemd |
| `openclaw gateway status` | affiche statut service + probe |
| `openclaw gateway probe` | vérifie l'accessibilité WS |
| `openclaw gateway stop` | arrête le service |
| `openclaw gateway install` | installe le service systemd |

### Gateway status — état actuel

```text
Service: systemd (disabled)
File logs: /tmp/openclaw/openclaw-2026-05-13.log
Config: ~/.openclaw/openclaw.json
Bind: loopback (127.0.0.1), port=18789
Runtime: stopped (state inactive, sub dead, last exit 0)
Probe: ECONNREFUSED 127.0.0.1:18789
Reachable: NO
```

```text
GATEWAY_STATUS = STOPPED
SERVICE_INSTALLED = NO (systemd not installed)
```

### Doctor — constats

```text
State integrity:
  - Multiple state directories detected (peut fragmenter l'historique de session) :
    - /home/openclaw/.openclaw  ← ancienne dir utilisateur openclaw (lié au path mismatch repo V1.2.1)
    - ~/.openclaw               ← dir active pour user ghost

Security: aucun avertissement canal.

Gateway: not running.
Gateway service: not installed.
Gateway target: ws://127.0.0.1:18789
```

**Note importante — multiple state dirs :**

```text
/home/openclaw/.openclaw = ancienne state dir (user openclaw)
/home/ghost/.openclaw    = state dir active (user ghost)
```

Ceci confirme le path mismatch identifié dans `06_TOOL_POLICY_DEPLOYMENT_RISK_MATRIX.md`. La state dir du user `openclaw` est détectée mais inactive. Elle correspond aux paths référencés dans le repo V1.2.1 (`agentDir: "/home/openclaw/.openclaw/..."`).

### Sandbox effective proof

```text
agentId: builder
mode: off, sessionIsSandboxed: false
allow (default): exec, process, read, write, edit, apply_patch, ...
source: "default"
```

---

## Questions tranchées

| Question | Verdict | Evidence |
| :--- | :--- | :--- |
| Gateway command disponible ? | **OUI** | `openclaw gateway --help` |
| Config V2 lisible sans secret leak ? | **OUI** | python3 inspection — token non imprimé |
| Gateway actuellement démarré ? | **NON** | ECONNREFUSED 18789, status=stopped |
| Service systemd installé ? | **NON** | "Gateway service not installed" |
| Démarrage foreground isolable ? | **OUI** | `openclaw gateway run` (foreground, ctrl+C pour stop) |
| Démarrage implique runtime job auto ? | **À CONFIRMER** | commande gateway run à inspecter en lot suivant |
| Rollback simple disponible ? | **OUI** | ctrl+C (foreground) ou `openclaw gateway stop` |
| Multiple state dirs problème ? | **MINEUR** | `/home/openclaw/.openclaw` inactif, ne bloque pas gateway |

---

## Commande de démarrage identifiée

```bash
openclaw gateway run
```

Mode : foreground. Le processus reste au premier plan. Stop : `Ctrl+C` ou signal SIGINT.

Flags optionnels utiles :

```bash
openclaw gateway run --verbose   # logs détaillés
openclaw gateway run --port 18789 --bind loopback  # explicite
```

**Ne pas utiliser dans ce lot.** Documenter uniquement pour le lot suivant.

---

## Preflight verdict

```text
PREFLIGHT_STATUS = PASS
GATEWAY_ACTIVATABLE = YES
METHOD = openclaw gateway run (foreground)
CONFIG_SOURCE = ~/.openclaw/openclaw.json (V2)
NO_MIGRATION_V121_REQUIRED
NO_DOCKER_REQUIRED (sandbox mode off)
ROLLBACK = Ctrl+C ou kill processus
```

---

## Risque résiduel — multiple state dirs

```text
/home/openclaw/.openclaw est présent mais inactif.
Le doctor OpenClaw le signale comme fragmenteur d'historique session.
Ce répertoire correspond aux anciens agentDirs du repo V1.2.1.
Il ne bloque pas le gateway mais peut créer de la confusion.
ACTION_RECOMMENDED = documenter, ne pas supprimer dans ce lot.
```

---

## NEXT_GO

```text
08_GATEWAY_ACTIVATION_EXECUTION_PLAN.md
```

Rôle :

1. Planifier le démarrage `openclaw gateway run` de façon contrôlée ;
2. Définir l'ordre des vérifications post-démarrage (`gateway status`, `gateway probe`, `sandbox explain`) ;
3. Définir les conditions d'arrêt immédiat ;
4. Préparer le rollback explicite ;
5. Ne démarrer le gateway que si validation humaine obtenue.

## RISKS

- À qualifier.
