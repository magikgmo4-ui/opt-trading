# 06_REMEDIATION_EXECUTION_PLAN

## Objectif

Preparer le plan d'execution de la remediation Phase 6 AI_TEAM db-layer/OpenClaw remote exec, sans relance runtime.

## Decisions canonisees

| Gap | Decision | Statut |
|:----|:---------|:-------|
| identity | A — cle SSH pour `openclaw` | SELECTED |
| sandbox | B — config OpenClaw | SELECTED |
| SSH alias | A — ajouter alias canonique | SELECTED |

## Runtime lock

Aucune relance runtime n'est autorisee tant que les trois gates suivantes ne sont pas explicitement passees a `VALIDATED`.

| Gate | Status |
|:-----|:-------|
| identity doc gate | REQUIRED |
| sandbox doc gate | REQUIRED |
| SSH alias doc gate | REQUIRED |

## Perimetre du plan

Ce document prepare uniquement :

- les commandes prevues ;
- les prechecks ;
- le rollback ;
- les preuves attendues ;
- les stop conditions.

Il ne valide aucune gate et ne declenche aucune execution.

## Prechecks obligatoires

### Git

```bash
git status --short --branch
git log --oneline -5
git diff --stat origin/sot/mainline...HEAD
```

Attendu :

- branche dediee active ;
- aucun fichier non prevu ;
- aucun secret ;
- aucun changement hors dossier chantier.

### Secrets

```bash
git diff --cached
git diff
```

Attendu :

- aucune cle privee ;
- aucun token ;
- aucun mot de passe ;
- aucun host sensible non deja canonise ;
- aucune donnee runtime confidentielle.

### identity

Commandes prevues, non executees a ce stade :

```bash
id openclaw
getent passwd openclaw
ls -la /home/openclaw/.ssh
```

Preuve attendue :

- utilisateur `openclaw` identifiable ;
- home directory connu ;
- emplacement SSH borne ;
- aucun secret copie dans le repo.

Stop condition :

- user `openclaw` absent ;
- home directory ambigu ;
- permissions SSH non conformes ;
- besoin de secret non documentable.

### sandbox

Commandes prevues, non executees a ce stade :

```bash
find . -maxdepth 4 -iname '*openclaw*' -o -iname '*sandbox*'
grep -R "sandbox\|allow\|deny\|ssh" -n docs/ config/ 2>/dev/null || true
```

Preuve attendue :

- fichier ou surface de configuration identifiee ;
- chemins autorises/interdits separes ;
- aucune ouverture globale du sandbox ;
- modification strictement bornee a OpenClaw.

Stop condition :

- config introuvable ;
- seule option disponible = assouplissement global ;
- acces runtime elargi par defaut ;
- impact hors AI_TEAM/db-layer.

### SSH alias

Commandes prevues, non executees a ce stade :

```bash
ssh -G <ALIAS_CANONIQUE> | sed -n '1,80p'
```

Preuve attendue :

- alias canonique nomme ;
- host resolu ;
- user attendu ;
- identity file attendu ;
- aucune connexion reelle necessaire pour la premiere validation.

Stop condition :

- alias resout vers une cible inconnue ;
- user SSH different du modele retenu ;
- identity file absent ;
- commande necessitant un secret non documentable.

## Plan d'execution prevu

### Etape 1 — Identity

But : rendre l'identite `openclaw` compatible avec l'execution SSH ciblee.

Action prevue :

- valider l'existence du user ;
- valider le repertoire `.ssh` ;
- preparer l'association identity file sans exposer de secret ;
- documenter permissions attendues.

Gate attendue :

```text
identity doc gate = VALIDATED
```

### Etape 2 — Sandbox

But : configurer OpenClaw sans assouplir globalement le sandbox.

Action prevue :

- localiser la configuration OpenClaw ;
- ajouter uniquement les chemins necessaires ;
- refuser tout acces large non justifie ;
- documenter comportement attendu en echec.

Gate attendue :

```text
sandbox doc gate = VALIDATED
```

### Etape 3 — SSH alias

But : creer ou confirmer l'alias SSH canonique.

Action prevue :

- nommer l'alias ;
- verifier la resolution via `ssh -G` ;
- confirmer user, host, identity file ;
- eviter toute connexion remote avant validation des trois gates.

Gate attendue :

```text
SSH alias doc gate = VALIDATED
```

## Rollback prevu

Rollback documentaire :

```bash
git restore -- docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01/
```

Rollback config, si une etape ulterieure modifie reellement une configuration :

```bash
cp <CONFIG_FILE>.bak <CONFIG_FILE>
```

Rollback SSH alias, si une etape ulterieure ajoute reellement un alias :

```bash
# supprimer uniquement le bloc alias ajoute
# ne pas modifier les autres entrees SSH
```

Rollback cle/identity :

```bash
# ne jamais supprimer une cle existante sans preuve qu'elle a ete creee par ce chantier
# desactiver seulement l'association configuree si elle a ete ajoutee pendant la remediation
```

## Preuves attendues avant runtime

| Preuve                                  | Required |
| :-------------------------------------- | :------- |
| user `openclaw` confirme                | oui      |
| surface config OpenClaw confirmee       | oui      |
| alias SSH canonique resolu par `ssh -G` | oui      |
| aucun secret dans repo                  | oui      |
| rollback documente                      | oui      |
| stop conditions acceptees               | oui      |

## Stop conditions globales

Arret immediat si :

- secret requis dans le repo ;
- ambiguite sur l'utilisateur effectif ;
- sandbox doit etre ouvert globalement ;
- alias SSH pointe vers une cible non canonisee ;
- une commande runtime devient necessaire avant gates ;
- modification hors AI_TEAM/db-layer ;
- impact admin-trading, bridge, WAN ou closeout DB_LAYER.

## NEXT_GO

Creer ensuite `07_REMEDIATION_GATE_VALIDATION.md` seulement si le plan d'execution est relu et accepte.

Runtime reste bloque tant que :

```text
identity doc gate != VALIDATED
sandbox doc gate != VALIDATED
SSH alias doc gate != VALIDATED
```

## RISKS

- À qualifier.
