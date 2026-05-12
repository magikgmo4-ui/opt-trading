# 08_REMEDIATION_BLOCKER_REPORT

## Objectif

Documenter les blockers restants apres la passe de preuve locale Phase 6 AI_TEAM db-layer/OpenClaw remote exec.

## Verdict synthese

```text
APPLY_PLAN_NOT_AUTHORIZED
RUNTIME_REMAINS_BLOCKED
```

## Gate status

| Gate | Status | Evidence | Blocker |
|:-----|:-------|:---------|:--------|
| identity | BLOCKED | user `openclaw` existe, home `/home/openclaw`, mais `/home/openclaw/.ssh` absent | provisionnement SSH `openclaw` requis |
| sandbox | BLOCKED | aucune surface config OpenClaw sandbox clairement localisee | audit config cible requis |
| SSH alias | VALIDATED_CONFIG_PRESENT | `Host fantome` deja present dans `~/.ssh/config` | validation locale `ssh -G fantome` encore a capturer |

## identity blocker

### Preuve

- `openclaw` existe.
- Home : `/home/openclaw`.
- Repertoire SSH attendu : `/home/openclaw/.ssh`.
- Statut : absent.

### Impact

La decision `identity = A — cle SSH pour openclaw` ne peut pas etre appliquee tant que l'espace SSH de `openclaw` n'est pas provisionne.

### Action requise

Preparer un lot separe pour :

- creer `/home/openclaw/.ssh` si absent ;
- appliquer les permissions attendues ;
- definir l'association de cle sans copier de secret dans le repo ;
- documenter rollback.

## sandbox blocker

### Preuve

- Recherche locale bruitee.
- Aucune config OpenClaw sandbox clairement identifiee.

### Impact

La decision `sandbox = B — config OpenClaw` ne peut pas etre appliquee tant que la surface de configuration n'est pas localisee.

### Action requise

Preparer un audit cible :

- fichiers config OpenClaw ;
- chemins autorises/interdits ;
- comportement d'echec ;
- preuve qu'aucun assouplissement global n'est requis.

## SSH alias status

### Preuve

`~/.ssh/config` contient deja :

```text
Host fantome
  HostName 192.168.0.191
  User fantome
```

### Impact

Le gap initial "alias absent" est resolu cote configuration existante.

### Limite

La validation complete doit encore capturer une resolution locale non-connective :

```bash
ssh -G fantome | sed -n '1,120p'
```

Cette commande ne doit pas etablir de connexion SSH.

## Runtime lock

Aucune relance runtime n'est autorisee.

Runtime reste bloque tant que :

| Gate | Required final status |
|:-----|:----------------------|
| identity | VALIDATED |
| sandbox | VALIDATED |
| SSH alias | VALIDATED_CONFIG_PRESENT ou VALIDATED_NON_CONNECTIVE |

## Stop conditions maintenues

Arret immediat si :

- secret requis dans le repo ;
- creation de cle privee demandee dans la documentation ;
- sandbox necessite une ouverture globale ;
- connexion SSH reelle requise ;
- impact admin-trading, bridge, WAN ou closeout DB_LAYER ;
- modification hors perimetre AI_TEAM/db-layer.

## NEXT_GO

Creer un lot separe :

```text
09_REMEDIATION_BLOCKER_CLEARANCE_PLAN.md
```

Objectif :

1. lever blocker identity par provisionnement SSH controle pour `openclaw`;
2. localiser config OpenClaw sandbox;
3. capturer `ssh -G fantome` sans connexion;
4. revenir ensuite a `07` pour revalider les gates.
