---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_LOCAL_OPERATIONAL_RUNBOOK_01_RUNBOOK
doc_type: runbook
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_LOCAL_OPERATIONAL_RUNBOOK_01
parent_go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_FIRST_LOCAL_EXECUTION_RUN_01
machine: fantome
status: pass
lifecycle_stage: operational_documentation
topic_keys:
  - openclaw
  - builder
  - runbook
  - local_operations
  - constraints
  - gate_conditions
source_kind: canonical
updated_at: 2026-05-14
---

# OPENCLAW_BUILDER_LOCAL_OPERATIONAL_RUNBOOK_01

## 1_OBJECTIF

Documenter l'usage operationnel local valide du builder OpenClaw V2, formaliser les commandes autorisees, les limites strictes en vigueur, et les conditions necessaires avant toute future levee du blocage remote/SSH.

Ce runbook est le point d'entree unique pour tout operateur (humain ou agent) souhaitant utiliser le builder en mode local sur `fantome`.

## 2_HISTORIQUE DE LA CHAINE

| PR | GO | Objet | Statut |
|----|----|-------|--------|
| #389 | SANDBOX_SCHEMA_DISCOVERY | Decouverte du schema sandbox | PASS |
| #400 | FIRST_CONTROLLED_JOB | Definition de la gate du 1er job | PASS_GATED |
| #401 | FIRST_LOCAL_EXECUTION | Plan d'execution locale/sandbox | PASS_GATED |
| #410 | FIRST_LOCAL_EXECUTION_RUN | Execution reelle locale (audit) | PASS |

**Commit de reference :** `eaa72d6` (sot/mainline, merge PR #410)

## 3_MODE_LOCAL_VALIDE

Le builder OpenClaw a ete valide en mode strictement local/sandbox avec les caracteristiques suivantes :

### 3.1 Surface d'execution

```yaml
surface: repo local opt-trading (/home/fantome/opt-trading)
scope: docs/chantiers/ (audit structurel)
mode: read-only
dry_run: obligatoire par defaut
```

### 3.2 Commandes autorisees

Toute commande locale non destructive de lecture de l'etat du repo est autorisee sous reserve des contraintes ci-dessous.

Commandes explicites autorisees :

| Commande | Description | Risque |
|----------|-------------|--------|
| `ls docs/chantiers/` | Lister les chantiers | FAIBLE |
| `find docs/chantiers/ -type f` | Compter les fichiers | FAIBLE |
| `grep -r PATTERN docs/chantiers/` | Rechercher dans les docs | FAIBLE |
| `git status` | Verifier l'etat du repo | FAIBLE |
| `git log --oneline` | Lire l'historique | FAIBLE |
| `git show HASH:path` | Lire un fichier dans un commit | FAIBLE |
| `git diff` | Comparer les branches | FAIBLE |
| Audit structurel programmatique | Compter, classifier, verifier | FAIBLE |

### 3.3 Commandes interdites (BLOCKED en permanence)

```text
- SSH vers toute machine distante
- Connexion a un serveur remote
- Acces WAN (curl, wget, http, etc.)
- Execution de code non valide
- Modification de fichiers hors livrables GO documentes
- Acces a des fichiers .env, credentials, secrets
- Interaction avec des systemes de trading live
- Bridge vers admin-trading
- Patch runtime non gate
- Invocation du builder agent sans validation humaine prealable
```

## 4_CONTRAINTES_STRICTES (INVARIANTS)

Ces contraintes sont heritees des GOs #400 et #401 et restent en vigueur pour toute operation locale :

```text
[x] Aucun SSH reel
[x] Aucune commande remote
[x] Aucun patch runtime sans gate explicite
[x] Aucun secret dans le repo ou les commandes
[x] Aucun WAN
[x] Aucun bridge
[x] Aucun admin-trading
[x] Aucun closeout DB_LAYER rouvert
[x] Validation humaine obligatoire avant toute execution
[x] Dry-run obligatoire par defaut
[x] Read-only sauf livrables GO documentes
```

## 5_CONDITIONS_DE_LEVEE_DU_BLOCAGE_REMOTE

Le passage du mode local au mode remote/SSH est **BLOCKED**. Les conditions suivantes doivent etre satisfaites de maniere cumulable avant toute tentative de levee :

### 5.1 Preuves techniques

```text
[ ] CLI openclaw installe et fonctionnel sur fantome
[ ] Gateway V2 verifie en direct (pas seulement documente)
[ ] Orchestrateur verifie joignable et stable
[ ] Builder agent repond a un message dry-run non destructif en local
[ ] Toutes les stop-conditions du GO #400 sont testees et actives
```

### 5.2 Preuves de securite

```text
[ ] Audit de securite de la surface SSH cible complete
[ ] Cle SSH dediee, scope limite, sans acces sudo
[ ] Firewall / iptables verifie pour la machine cible
[ ] Pas de secrets transitant en clair
[ ] Approbation humaine explicite et documentee
```

### 5.3 Preuves de gouvernance

```text
[ ] GO specifique ouvert pour le passage en remote (GO child distinct)
[ ] Plan de rollback defini et accepte
[ ] Toutes les parties prenantes notifiees
[ ] Gate documentee et approuvee (format GO #400)
```

## 6_STOP_CONDITIONS

Arret immediat de toute operation builder si :

```text
- Le builder tente d'executer une commande shell non autorisee
- Le builder demande un secret ou des credentials
- Le builder propose SSH ou remote exec
- Le builder sort du perimetre read-only defini
- Le gateway devient instable
- Une session non attendue apparait sur un autre agent
- Une commande echoue de maniere inattendue
- Un fichier est modifie sans validation prealable
```

## 7_PATTERN_DE_JOB_STANDARD

Tout job builder local doit suivre ce gabarit :

```yaml
job_id: BUILDER_LOCAL_XXX
type: sandbox_read_only  # ou dry_run
scope: repo-local
command: "commande explicite non destructive"
ssh: 0
remote: 0
wan: 0
secrets: 0
write: 0  # ou "livrables GO documentes uniquement"
risk: FAIBLE
dry_run: true
validation_humaine: true
cadre: conforme au runbook OPENCLAW_BUILDER_LOCAL_OPERATIONAL_RUNBOOK_01
```

### 7.1 Etapes standard

1. Verifier l'etat du repo (`git status` propre)
2. Verifier la branche active (doit etre la branche du GO)
3. Confirmer la surface locale (pas de SSH/remote/WAN)
4. Executer la commande en read-only ou dry-run
5. Collecter les sorties dans `reports/ai/builder/`
6. Verifier `git status` post-execution (doit etre propre)
7. Rediger le closeout
8. PR + merge dans `sot/mainline`

## 8_ETAT_ACTUEL (SORTIE DE CHAINE)

```text
OpenClaw Builder = FIRST_LOCAL_EXECUTION_RUN_COMPLETE
remote/SSH = BLOCKED
Gateway V2 = stable (documente)
CLI openclaw = non installe sur fantome
tmux = non disponible localement
Prochaine etape recommandee = installation CLI openclaw + test dry-run local
```

## 9_REFERENCE_CROISEE

- `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_FIRST_CONTROLLED_JOB_01/01_BUILDER_FIRST_JOB_GATE.md` (sot/mainline)
- `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_FIRST_LOCAL_EXECUTION_01/OPENCLAW_BUILDER_FIRST_LOCAL_EXECUTION_PLAN_01.md` (sot/mainline)
- `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_FIRST_LOCAL_EXECUTION_RUN_01/OPENCLAW_BUILDER_FIRST_LOCAL_EXECUTION_RUN_REPORT_01.md` (sot/mainline)
- `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md` (branche active)

## 10_VERDICT

```text
PASS

GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_LOCAL_OPERATIONAL_RUNBOOK_01

Runbook operationnel local redige. Usage local valide documente. Contraintes formalisees.
Conditions de levee du blocage remote definies. Aucun SSH, remote, WAN, ou secret.
```

## RISKS

- À qualifier.
