# 12_REMEDIATION_APPLY_PLAN

## Objectif

Planifier l'application controlee des remediations Phase 6 AI_TEAM db-layer/OpenClaw remote exec.

Ce document ne declenche aucune execution runtime.

## Etat des gates avant application

| Gate | Status | Evidence |
|:-----|:-------|:---------|
| identity | VALIDATED_PROVISIONING_READY | `/home/openclaw/.ssh` cree, mode 700, owner `openclaw:openclaw`; config `-rw-------` |
| sandbox | VALIDATED_CONFIG_SURFACE_FOUND | `modules/openclaw_config_modulaire/app/agents.json5` contient `sandbox { enforce, scope:"agent", allow, deny }` |
| SSH alias | VALIDATED_NON_CONNECTIVE | `ssh -G fantome` resout host `192.168.0.191`, user `fantome`, identity `id_ed25519_fantome` |

## Runtime lock

```text
RUNTIME_REMAINS_BLOCKED_UNTIL_EXECUTION_GATE
```

Aucune relance OpenClaw, aucune connexion SSH reelle et aucune commande remote ne sont autorisees dans ce document.

---

## Remediation 1 — identity key / openclaw SSH

### Etat actuel

- User `openclaw` existe.
- `/home/openclaw/.ssh` existe.
- Permissions corrigees :

  - `.ssh` : `700`
  - `config` : `600`
  - owner : `openclaw:openclaw`

### Application prevue

Configurer l'identite SSH de `openclaw` sans exposer de secret dans le repo.

### Commandes prevues

```bash
sudo ls -ld /home/openclaw/.ssh
sudo ls -l /home/openclaw/.ssh/config
sudo -u openclaw ssh -G fantome | sed -n '1,120p'
```

### Gate d'execution

```text
EXEC_GATE_IDENTITY = REQUIRED
```

La gate peut passer a `VALIDATED` seulement si :

- la resolution SSH sous `openclaw` fonctionne en mode non-connectif ;
- aucune cle privee n'est copiee dans le repo ;
- aucune donnee secrete n'est imprimee dans les logs ;
- aucune connexion SSH reelle n'est tentee.

### Stop condition

Stop immediat si :

- `sudo -u openclaw ssh -G fantome` echoue ;
- la resolution utilise une identite inattendue ;
- une cle privee doit etre deplacee manuellement ;
- un secret apparait dans la sortie.

---

## Remediation 2 — sandbox OpenClaw

### Etat actuel

Surface config localisee :

```text
modules/openclaw_config_modulaire/app/agents.json5
```

Champ pertinent :

```text
sandbox {
  enforce
  scope: "agent"
  allow
  deny
}
```

### Application prevue

Configurer uniquement les regles sandbox necessaires a l'agent ou a la surface OpenClaw concernee.

### Commandes prevues

Lecture avant modification :

```bash
sed -n '1,220p' modules/openclaw_config_modulaire/app/agents.json5
grep -nE "sandbox|enforce|scope|allow|deny|ssh|remote|path" modules/openclaw_config_modulaire/app/agents.json5
```

Modification prevue :

```text
A definir dans un patch separe apres validation EXEC_GATE_SANDBOX.
```

### Gate d'execution

```text
EXEC_GATE_SANDBOX = REQUIRED
```

La gate peut passer a `VALIDATED` seulement si :

- les regles `allow` sont minimales ;
- les regles `deny` restent protectrices ;
- aucune ouverture globale du sandbox n'est introduite ;
- le scope reste borne a `agent` ou a la cible strictement necessaire ;
- le diff est relu avant commit.

### Stop condition

Stop immediat si :

- la remediation exige `enforce=false` ;
- le scope doit devenir global ;
- les chemins autorises sont trop larges ;
- le patch impacte une surface hors AI_TEAM/db-layer.

---

## Remediation 3 — SSH alias fantome

### Etat actuel

Alias existant :

```text
Host fantome
  HostName 192.168.0.191
  User fantome
```

Resolution non-connective validee :

```text
host = 192.168.0.191
user = fantome
identity = id_ed25519_fantome
```

### Application prevue

Aucune creation d'alias necessaire pour le moment.

### Commande prevue

```bash
ssh -G fantome | sed -n '1,120p'
```

### Gate d'execution

```text
EXEC_GATE_SSH_ALIAS = VALIDATED_NON_CONNECTIVE
```

Reste interdit dans ce lot :

- `ssh fantome`
- commande remote
- test WAN
- test runtime OpenClaw

---

## Matrice d'application

| Remediation | Action | Gate | Runtime |
|:------------|:-------|:-----|:--------|
| identity | resolution SSH sous `openclaw` | EXEC_GATE_IDENTITY_REQUIRED | non |
| sandbox | patch minimal `agents.json5` | EXEC_GATE_SANDBOX_REQUIRED | non |
| SSH alias | conserver alias existant | EXEC_GATE_SSH_ALIAS_VALIDATED_NON_CONNECTIVE | non |

## Rollback prevu

### identity

```bash
# Ne supprimer aucune cle existante.
# Revenir uniquement sur les fichiers crees par ce chantier si necessaire.
sudo rm -f /home/openclaw/.ssh/config
sudo rmdir /home/openclaw/.ssh 2>/dev/null || true
```

### sandbox

```bash
git restore -- modules/openclaw_config_modulaire/app/agents.json5
```

### SSH alias

```bash
# Aucun rollback prevu si aucune modification SSH alias n'est faite.
```

## Stop conditions globales

Arret immediat si :

- secret requis dans le repo ;
- cle privee exposee ;
- connexion SSH reelle necessaire avant validation ;
- runtime OpenClaw demande ;
- sandbox doit etre assouplie globalement ;
- impact WAN, bridge, admin-trading ou closeout DB_LAYER ;
- modification hors perimetre AI_TEAM/db-layer.

## NEXT_GO

Creer ensuite :

```text
13_REMEDIATION_EXECUTION_GATE_REQUEST.md
```

Role :

1. demander explicitement la validation d'execution ;
2. lister les commandes exactes autorisees ;
3. confirmer que le runtime reste bloque sauf autorisation explicite ;
4. preparer ensuite seulement un `14_REMEDIATION_APPLY_EXECUTION_LOG.md`.

## RISKS

- À qualifier.
