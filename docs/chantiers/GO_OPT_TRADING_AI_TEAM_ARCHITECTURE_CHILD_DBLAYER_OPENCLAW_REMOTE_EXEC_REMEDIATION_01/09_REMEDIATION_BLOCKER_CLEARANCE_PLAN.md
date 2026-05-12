# 09_REMEDIATION_BLOCKER_CLEARANCE_PLAN

## Objectif

Planifier la levee controlee des blockers restants de la Phase 6 AI_TEAM db-layer/OpenClaw remote exec.

Ce document ne lance aucun runtime et ne modifie aucune configuration reelle.

## Etat courant des gates

| Gate | Status | Raison |
|:-----|:-------|:-------|
| identity | BLOCKED | `/home/openclaw/.ssh` absent |
| sandbox | BLOCKED | config OpenClaw sandbox non localisee |
| SSH alias | VALIDATED_CONFIG_PRESENT | alias `fantome` deja present dans `~/.ssh/config` |

## Runtime lock

```text
RUNTIME_REMAINS_BLOCKED
```

Runtime interdit tant que :

- identity != VALIDATED ;
- sandbox != VALIDATED ;
- SSH alias non confirme au minimum par resolution locale non-connective.

## Invariants

- Aucun secret dans le repo.
- Aucune cle privee copiee dans la documentation.
- Aucune connexion SSH reelle dans ce lot.
- Aucun runtime OpenClaw.
- Aucun WAN.
- Aucun bridge.
- Aucun admin-trading.
- Aucun closeout DB_LAYER rouvert.
- Aucun index global modifie.

---

## Bloc 1 — Clearance identity

### Blocker

`openclaw` existe, mais `/home/openclaw/.ssh` est absent.

### Objectif

Preparer un provisionnement SSH controle pour `openclaw`, sans secret repo.

### Commandes prevues

```bash
id openclaw
getent passwd openclaw
sudo install -d -m 700 -o openclaw -g openclaw /home/openclaw/.ssh
sudo install -m 600 -o openclaw -g openclaw /dev/null /home/openclaw/.ssh/config
sudo ls -ld /home/openclaw/.ssh
sudo ls -l /home/openclaw/.ssh/config
```

### Preuve attendue

- `/home/openclaw/.ssh` existe ;
- owner = `openclaw:openclaw` ;
- mode `.ssh` = `700` ;
- aucun secret cree dans le repo ;
- aucune cle privee copiee.

### Stop conditions

- `openclaw` absent ;
- home directory different de `/home/openclaw` sans justification ;
- sudo non autorise ;
- besoin de copier une cle privee dans le repo ;
- besoin de connexion SSH reelle.

### Gate cible

```text
identity = VALIDATED_PROVISIONING_READY
```

---

## Bloc 2 — Clearance sandbox

### Blocker

La config OpenClaw sandbox n'est pas localisee.

### Objectif

Localiser la surface de configuration OpenClaw/sandbox avant toute modification.

### Commandes prevues

```bash
find . -maxdepth 7 \
  \( -iname '*openclaw*' -o -iname '*sandbox*' -o -iname '*policy*' -o -iname '*allow*' -o -iname '*deny*' \) \
  -print

find "$HOME" -maxdepth 5 \
  \( -iname '*openclaw*' -o -iname '*sandbox*' \) \
  -print 2>/dev/null || true

grep -R "sandbox\|allow\|deny\|policy\|ssh\|remote" -n \
  .config config configs docs scripts 2>/dev/null || true
```

### Preuve attendue

- fichier ou surface config OpenClaw identifie ;
- type de config determine ;
- chemins autorises/interdits separables ;
- aucune necessite d'assouplissement global ;
- aucun impact hors AI_TEAM/db-layer.

### Stop conditions

- aucune config localisable ;
- seule solution = assouplir globalement le sandbox ;
- acces large requis ;
- modification hors perimetre ;
- besoin de runtime pour decouvrir la config.

### Gate cible

```text
sandbox = VALIDATED_CONFIG_SURFACE_FOUND
```

---

## Bloc 3 — Clearance SSH alias

### Etat

Alias `fantome` deja present :

```text
Host fantome
  HostName 192.168.0.191
  User fantome
```

### Objectif

Capturer une preuve locale non-connective.

### Commande prevue

```bash
ssh -G fantome | sed -n '1,120p'
```

### Preuve attendue

- `hostname 192.168.0.191` ;
- `user fantome` ;
- identity file visible si configure ;
- aucune connexion etablie.

### Stop conditions

- alias non resolu ;
- user different ;
- host different ;
- commande tente une connexion ;
- secret requis.

### Gate cible

```text
SSH alias = VALIDATED_NON_CONNECTIVE
```

---

## Matrice clearance

| Blocker | Action | Expected gate | Runtime allowed |
|:--------|:-------|:--------------|:----------------|
| identity | provisionnement `.ssh` controle | VALIDATED_PROVISIONING_READY | non |
| sandbox | localisation config | VALIDATED_CONFIG_SURFACE_FOUND | non |
| SSH alias | `ssh -G fantome` | VALIDATED_NON_CONNECTIVE | non |

## NEXT_GO

Creer ensuite :

```text
10_REMEDIATION_BLOCKER_CLEARANCE_EXECUTION_LOG.md
```

Role :

1. executer uniquement les commandes de clearance autorisees ;
2. capturer les preuves ;
3. mettre a jour `07_REMEDIATION_GATE_VALIDATION.md` ;
4. produire ensuite soit :

   - `11_REMEDIATION_APPLY_PLAN.md` si gates suffisantes ;
   - `11_REMEDIATION_STILL_BLOCKED_REPORT.md` si un blocker persiste.
