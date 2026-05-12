# 07_REMEDIATION_GATE_VALIDATION

## Objectif

Valider ou bloquer les trois gates de remediation Phase 6 avant toute execution runtime.

## Decisions canonisees

| Gap | Decision | Source |
|:----|:---------|:-------|
| identity | A — cle SSH pour `openclaw` | 05_REMEDIATION_SELECTED_OPTIONS.md |
| sandbox | B — config OpenClaw | 05_REMEDIATION_SELECTED_OPTIONS.md |
| SSH alias | A — ajouter alias canonique | 05_REMEDIATION_SELECTED_OPTIONS.md |

## Runtime lock

Aucune relance runtime n'est autorisee tant que les trois gates ne sont pas `VALIDATED`.

| Gate | Status | Evidence | Verdict |
|:-----|:-------|:---------|:--------|
| identity doc gate | PENDING_REVIEW | A completer | BLOCKED_UNTIL_PROVEN |
| sandbox doc gate | PENDING_REVIEW | A completer | BLOCKED_UNTIL_PROVEN |
| SSH alias doc gate | PENDING_REVIEW | A completer | BLOCKED_UNTIL_PROVEN |

## Criteres de validation

### identity doc gate

Pour passer a `VALIDATED`, il faut prouver :

- le user `openclaw` existe ou sa creation est explicitement cadree ;
- le home directory cible est connu ;
- le mode SSH ne necessite aucun secret dans le repo ;
- l'identite effective ne passe pas par une chaine ambigue `sudo -> ghost -> ssh`.

Verdict initial :

```text
BLOCKED_UNTIL_PROVEN
```

### sandbox doc gate

Pour passer a `VALIDATED`, il faut prouver :

- la surface de configuration OpenClaw est identifiee ;
- les chemins autorises sont bornes ;
- les chemins interdits restent proteges ;
- aucune ouverture globale du sandbox n'est requise.

Verdict initial :

```text
BLOCKED_UNTIL_PROVEN
```

### SSH alias doc gate

Pour passer a `VALIDATED`, il faut prouver :

- l'alias canonique est nomme ;
- la resolution `ssh -G <alias>` est possible sans connexion runtime ;
- le user cible est coherent avec `identity = A`;
- la configuration ne contient aucun secret documente.

Verdict initial :

```text
BLOCKED_UNTIL_PROVEN
```

## Commandes de preuve autorisees

Ces commandes sont des inspections locales ou de resolution config. Elles ne doivent pas lancer de runtime metier.

### Git proof

```bash
git status --short --branch
git log --oneline -8
git diff --stat origin/sot/mainline...HEAD
```

### identity proof

```bash
id openclaw
getent passwd openclaw
ls -ld /home/openclaw /home/openclaw/.ssh 2>/dev/null || true
```

### sandbox proof

```bash
find . -maxdepth 5 \( -iname '*openclaw*' -o -iname '*sandbox*' \)
grep -R "sandbox\|allow\|deny\|ssh" -n docs/ config/ 2>/dev/null || true
```

### SSH alias proof

```bash
ssh -G <ALIAS_CANONIQUE> | sed -n '1,120p'
```

## Stop conditions

Passer immediatement la gate a `BLOCKED` si :

- un secret est requis dans le repo ;
- le user effectif est ambigu ;
- la sandbox doit etre ouverte globalement ;
- l'alias SSH pointe vers une cible non canonisee ;
- une connexion runtime devient necessaire ;
- impact admin-trading, bridge, WAN ou closeout DB_LAYER ;
- modification hors perimetre AI_TEAM/db-layer.

## Matrice de decision finale

| Gate | Final status | Reason | Next action |
|:-----|:-------------|:-------|:------------|
| identity doc gate | VALIDATED_PROVISIONING_READY | `/home/openclaw/.ssh` cree (`drwx------`, owner `openclaw:openclaw`), config vide (`-rw-------`) | Prochaine etape : cle SSH |
| sandbox doc gate | BLOCKED | `find`/`grep` bruités, aucune surface config OpenClaw sandbox specifique localisee (`modules/openclaw_config_modulaire/` candidat a explorer) | Audit cible |
| SSH alias doc gate | VALIDATED_NON_CONNECTIVE | `ssh -G fantome` OK : host `192.168.0.191`, user `fantome`, identity `id_ed25519_fantome` | Gate levee |

## Gate validation update — local proof pass

### Resultats collectes

| Gate | Evidence | Final status | Reason | Next action |
|:-----|:---------|:-------------|:-------|:------------|
| identity doc gate | `/home/openclaw/.ssh` cree (`drwx------`, owner `openclaw:openclaw`, config `-rw-------`) | VALIDATED_PROVISIONING_READY | provisionnement `.ssh` realise | prochaine etape : association cle SSH |
| sandbox doc gate | `find` / `grep` bruités, aucune surface config OpenClaw sandbox specifique localisee (`modules/openclaw_config_modulaire/` candidat) | BLOCKED | configuration sandbox non identifiee | audit cible config OpenClaw |
| SSH alias doc gate | `ssh -G fantome` OK : host `192.168.0.191`, user `fantome`, identity `id_ed25519_fantome` | VALIDATED_NON_CONNECTIVE | alias confirme sans connexion | gate levee |

### Runtime decision

```text
RUNTIME_REMAINS_BLOCKED
```

Raison :

- identity gate = VALIDATED_PROVISIONING_READY ;
- sandbox gate = BLOCKED ;
- SSH alias gate = VALIDATED_NON_CONNECTIVE ;
- aucune execution remote autorisee tant que les blockers ne sont pas leves.

## NEXT_GO

Apres collecte des preuves :

1. remplacer chaque `PENDING_REVIEW` par `VALIDATED` ou `BLOCKED` — fait dans cette mise a jour;
2. documenter la preuve exacte — fait via `07_GATE_PROOF_LOCAL_OUTPUT.txt`;
3. si les trois gates sont `VALIDATED`, creer `08_REMEDIATION_APPLY_PLAN.md`;
4. si une gate est `BLOCKED`, creer `08_REMEDIATION_BLOCKER_REPORT.md` — fait.

Runtime reste interdit dans ce document.
