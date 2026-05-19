# 05_REMEDIATION_SELECTED_OPTIONS

## Objectif

Selectionner une option de remediation par gap Phase 6, a partir des audits reels, sans relance runtime.

## Decision synthese

| Gap | Option retenue | Decision | Gate | Evidence | Runtime |
|:----|:---------------|:---------|:-----|:---------|:--------|
| identity | A — cle SSH pour `openclaw` | SELECTED | DOC_GATE_REQUIRED | 01_IDENTITY_AUDIT.md | BLOCKED |
| sandbox | B — config OpenClaw | SELECTED | DOC_GATE_REQUIRED | 02_SANDBOX_AUDIT.md | BLOCKED |
| SSH alias | A — ajouter alias canonique | SELECTED | DOC_GATE_REQUIRED | 03_SSH_ALIAS_AUDIT.md | BLOCKED |

## identity — option A

### Selection

Utiliser une identite SSH propre a `openclaw`.

### Pourquoi

- Aligne l'executeur reel avec le compte cible.
- Evite un wrapper `sudo -> ghost -> ssh`.
- Reduit l'ambiguite entre user local, user remote, service user et repo owner.

### Gate avant execution

- Identifier le user exact utilise par OpenClaw.
- Documenter la methode SSH sans secret.
- Verifier qu'aucune cle privee, token ou credential n'est ajoute au repo.
- Definir un test non destructif avant toute commande runtime.

## sandbox — option B

### Selection

Configurer OpenClaw plutot que relacher globalement le sandbox.

### Pourquoi

- Evite l'assouplissement large du sandbox.
- Garde la remediation bornee a l'outil.
- Preserve une logique de moindre privilege.

### Gate avant execution

- Definir les chemins autorises.
- Definir les chemins explicitement interdits.
- Documenter le comportement attendu en echec.
- Confirmer que la configuration ne donne pas d'acces runtime elargi par defaut.

## SSH alias — option A

### Selection

Creer un alias SSH canonique.

### Pourquoi

- Plus stable que l'IP directe.
- Plus verifiable qu'une recopie depuis docs.
- Favorise une cible operatoire nommee et reutilisable.

### Gate avant execution

- Nommer l'alias canonique.
- Documenter le host cible sans secret.
- Verifier la resolution de configuration avant connexion reelle.
- Prevoir un test localise et reversible.

## Runtime gate global

Aucune relance runtime n'est autorisee tant que les trois gates suivantes ne sont pas validees :

| Gate | Status |
|:-----|:-------|
| identity doc gate | REQUIRED |
| sandbox doc gate | REQUIRED |
| SSH alias doc gate | REQUIRED |

## NEXT_GO

Creer `06_REMEDIATION_EXECUTION_PLAN.md` avec :
- commandes prevues ;
- prechecks ;
- rollback ;
- preuve attendue ;
- stop conditions ;
- interdiction runtime maintenue tant que les gates ne sont pas explicitement passees a VALIDATED.
