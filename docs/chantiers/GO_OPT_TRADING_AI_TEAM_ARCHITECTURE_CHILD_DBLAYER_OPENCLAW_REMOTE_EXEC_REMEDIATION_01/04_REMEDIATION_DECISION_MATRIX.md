# 04_REMEDIATION_DECISION_MATRIX

## Objectif

Transformer les audits Phase 6 en decisions controlees par gap, sans relance runtime.

## Invariants

- Aucun runtime avant gate explicite.
- Aucun WAN.
- Aucun bridge.
- Aucun admin-trading.
- Aucun closeout DB_LAYER rouvert.
- Aucun index global modifie.
- Toute decision doit etre rattachee a une preuve d'audit.

## Matrice de decision

| Gap | Options | Decision | Gate | Evidence | Status |
|:----|:--------|:---------|:-----|:---------|:-------|
| identity | A — cle SSH pour `openclaw` / B — wrapper `sudo -> ghost -> ssh` / C — aligner token gateway | SELECTED: A | DOC_GATE_REQUIRED | 01_IDENTITY_AUDIT.md | REVIEW_REQUIRED |
| sandbox | A — assouplir sandbox / B — config OpenClaw / C — wrapper `openclaw -> sudo -> ghost -> ssh` | SELECTED: B | DOC_GATE_REQUIRED | 02_SANDBOX_AUDIT.md | REVIEW_REQUIRED |
| SSH alias | A — ajouter alias canonique / B — IP directe / C — recopier depuis docs | SELECTED: A | DOC_GATE_REQUIRED | 03_SSH_ALIAS_AUDIT.md | REVIEW_REQUIRED |

## Criteres de validation

### identity

Decision possible uniquement si :
- l'identite operateur cible est explicite ;
- le contexte machine est identifie ;
- aucune ambiguite entre utilisateur local, remote user, service user et repo owner.

### sandbox

Decision possible uniquement si :
- le perimetre autorise est borne ;
- les chemins autorises/interdits sont separes ;
- la remediation ne donne pas acces runtime elargi par defaut.

### SSH alias

Decision possible uniquement si :
- l'alias cible est nomme ;
- la cle ou methode d'acces est documentee sans secret ;
- le test prevu reste localise et reversible.

## Runtime gate

Aucune relance runtime n'est autorisee tant que les trois lignes suivantes ne sont pas passees a VALIDATED :

| Gate | Required |
|:-----|:---------|
| identity decision | VALIDATED |
| sandbox decision | VALIDATED |
| SSH alias decision | VALIDATED |

## NEXT_GO

1. Lire les trois audits.
2. Remplacer A / B / C par les options reellement presentes.
3. Selectionner une option par gap.
4. Creer ensuite un plan d'execution borne si les trois gates sont VALIDATED.
