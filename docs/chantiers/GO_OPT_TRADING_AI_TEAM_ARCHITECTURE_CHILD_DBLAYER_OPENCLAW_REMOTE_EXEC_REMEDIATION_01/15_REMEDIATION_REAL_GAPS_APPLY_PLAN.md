# 15_REMEDIATION_REAL_GAPS_APPLY_PLAN

## Objectif

Planifier la correction reelle des deux gaps restants reveles apres l'execution d'application commit `518c9c2c`.

## Verdict

```text
NO_CLOSEOUT_YET
REAL_GAPS_REMAIN
RUNTIME_REMAINS_BLOCKED
```

## Gaps restants

| Gap | Status | Evidence | Required action |
|:----|:-------|:---------|:----------------|
| openclaw SSH alias | BLOCKED | `sudo -u openclaw ssh -G fantome` resout `hostname fantome`, `user openclaw`, `identitiesonly no` | configurer `/home/openclaw/.ssh/config` |
| OpenClaw sandbox | BLOCKED | `agents.json5` contient `sandbox: { mode: "all", workspaceAccess: "rw", scope: "agent" }` | modifier le mode ou ajouter regle autorisee selon schema reel |
| ghost SSH alias | VALIDATED | `ssh -G fantome` sous ghost resout `192.168.0.191`, user `fantome`, identity `id_ed25519_fantome` | aucune action ghost requise |

## Runtime lock

Aucun job OpenClaw ne doit etre lance tant que :

- l'alias `fantome` ne resout pas correctement sous `openclaw`;
- le sandbox ne permet pas explicitement le chemin reseau/SSH requis;
- aucune connexion SSH reelle n'est autorisee avant gate explicite.

---

## Patch candidat 1 — SSH alias pour openclaw

### Objectif

Faire en sorte que l'utilisateur `openclaw` resolve `fantome` comme `ghost`.

### Fichier cible

```text
/home/openclaw/.ssh/config
```

### Contenu candidat

```sshconfig
Host fantome
  HostName 192.168.0.191
  User fantome
  IdentityFile /home/openclaw/.ssh/id_ed25519_fantome
  IdentitiesOnly yes
```

### Precondition critique

La cle privee ne doit pas etre creee, copiee ou documentee dans le repo.

Si `/home/openclaw/.ssh/id_ed25519_fantome` n'existe pas, creer un sous-lot separe de provisioning secret-safe ou utiliser une methode hors repo validee.

### Commandes de prevue prevues

```bash
sudo -u openclaw ssh -G fantome | sed -n '1,120p'
```

### Gate attendue

```text
OPENCLAW_SSH_ALIAS_GATE = VALIDATED_NON_CONNECTIVE
```

---

## Patch candidat 2 — sandbox OpenClaw

### Fichier cible

```text
modules/openclaw_config_modulaire/app/agents.json5
```

### Etat observe

```json5
sandbox: { mode: "all", workspaceAccess: "rw", scope: "agent" }
```

### Probleme

`mode = "all"` bloque l'acces reseau/SSH depuis l'agent OpenClaw.

### Action requise avant patch

Auditer le code ou la documentation locale pour determiner les valeurs supportees :

```bash
grep -RInE "sandbox.*mode|mode.*sandbox|workspaceAccess|scope|allow|deny|network|ssh" modules/openclaw_config_modulaire app config configs scripts docs 2>/dev/null || true
```

### Options possibles

| Option | Description | Statut |
|:-------|:------------|:-------|
| A | changer `sandbox.mode` vers une valeur supportee plus permissive mais bornee | A valider par schema/code |
| B | ajouter une regle `allow` ciblee pour SSH/network si le schema le supporte | A valider par schema/code |
| C | garder `mode="all"` et declarer le runtime impossible | fallback si aucune config sure |

### Gate attendue

```text
SANDBOX_NETWORK_SSH_GATE = VALIDATED_CONFIG_PATCH_READY
```

---

## Stop conditions

Arret immediat si :

- la cle privee doit etre copiee dans le repo ;
- la config SSH imprime un secret ;
- `ssh -G` tente une connexion reelle ;
- la seule solution sandbox est une ouverture globale non bornee ;
- `agents.json5` ne supporte aucune regle reseau/SSH ;
- un runtime OpenClaw devient necessaire pour valider le patch ;
- impact WAN, bridge, admin-trading ou closeout DB_LAYER.

## NEXT_GO

Creer ensuite :

```text
16_REMEDIATION_REAL_GAPS_EXECUTION_LOG.md
```

Role :

1. appliquer uniquement la config SSH `openclaw` si secret-safe ;
2. auditer puis patcher `agents.json5` uniquement si le schema est confirme ;
3. capturer les preuves ;
4. ne lancer aucun job OpenClaw runtime.
