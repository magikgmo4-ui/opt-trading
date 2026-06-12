# PARENT_CHANTIERS_CLOSEOUT_REOPEN_ACTION_LIST_01

## 1_MASTER_TARGET
Decider le traitement operationnel des parents ambigus issus de l'audit.

## 7_CANONICAL_STATE
- Repo : `opt-trading`
- Branche : `sot/mainline`
- HEAD : `b59281b117fb05304fb2479ff171ef371c5cadb7`
- Audit source : `docs/reports/PARENT_CHANTIERS_PRODUCT_SURFACE_STATUS_AUDIT_01.md`
- Dirty state resume : worktree sale hors scope avec modifications suivies existantes et nombreux non suivis; aucun changement apporte aux index globaux dans cette passe
- Date : `2026-05-17`

## DECISION_TABLE

| Parent | Decision | Confiance | Preuve principale | Action suivante | Risque |
|---|---|---:|---|---|---|
| `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | `ARCHIVE_CANDIDATE` | 0.83 | `90_CLOSEOUT.md` indique `closeout_draft_only` + `03_READONLY_SMOKE_VALIDATION.md` confirme `VALIDATION_PASS_DRAFT_ONLY` + `02_READONLY_SMOKE_EXEC_REPORT.md` donne `VERDICT_DRAFT_ONLY` | Preserver le dossier comme trace de phase; ouvrir un GO distinct si une continuation technique devient valide | Double lecture possible entre "clos en draft" et "encore ouvert"; pas assez canonique pour un `CLOSEOUT` dur |
| `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01` | `CLOSEOUT` | 0.96 | `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_CLOSEOUT_01.md` confirme `WARNING_ONLY_CONFIRMED` + run reel `25956668749` + PR/children merges | Canoniser la fermeture documentaire; ne pas rouvrir sauf nouveau besoin explicite de permissions / schema | Risque faible: le statut final n'est pas encore propage dans les indexes courants |
| `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01` | `CLOSEOUT` | 0.94 | `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_CLOSEOUT_01.md` confirme les PR #466/#469 mergées, le workflow warning-only et le schema-validation artifact | Canoniser la fermeture documentaire; traiter le child schema manquant comme gap documentaire a part | Risque moyen: un child attendu (`JSON_SCHEMA_01`) manque au chemin reference |

## 1. GO_OPT_TRADING_STRICT_WORKERS_PARENT_01

### 13_ESTABLISHED
- Le parent existe par dossier, inbox et branch state canonique.
- Le cadrage initial impose un mode doc-only et une autonomie etroite, sans runtime.
- `03_READONLY_SMOKE_VALIDATION.md` confirme `VALIDATION_PASS_DRAFT_ONLY`.
- `90_CLOSEOUT.md` fige explicitement la phase comme `CLOSEOUT_PARENT_DRAFT_ONLY` et recommande un GO distinct pour la suite.

### 14_HYPOTHESIS
- Le parent est probablement termine en tant que phase documentaire, mais pas encore propulse dans une surface canonique unique.
- Le prochain travail devrait etre un GO separe, pas une reapertura du meme parent.

### 15_REMAINING_GAP
- La fermeture n'est pas encore alignee partout sur les index canoniques.
- La presence de la branche active et du dossier sur la ligne courante entretient une ambiguite de statut.

### DECISION
- `ARCHIVE_CANDIDATE`

### ACTION_LIST
- Conserver le parent comme trace de phase DRAFT_ONLY.
- Ne pas rouvrir ce parent pour du PATCH_DRAFT.
- Si continuation utile, ouvrir un GO distinct et borne.

### NEXT_GO
- `GO_OPT_TRADING_STRICT_WORKERS_CHILD_OR_FOLLOWUP_01` si et seulement si un nouveau besoin technique est valide.

---

## 2. GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01

### 13_ESTABLISHED
- Le parent a un dossier canonique, un inbox et un closeout parent dedie.
- Le closeout confirme la chaine warning-only, la preuve de run reel et le statut `WARNING_ONLY_CONFIRMED`.
- Les children structurants sont listes comme merges dans le closeout.
- Aucun runtime, secret, service ou index global n'est demande pour cette fermeture.

### 14_HYPOTHESIS
- Le statut canonique a propager dans `GO_INDEX.md` / `GO_CLOSED_INDEX.md` est probablement `CLOSED` ou `PASS` documentaire.
- Le parent doit rester reference, pas base active brute.

### 15_REMAINING_GAP
- La propagation canonique du closeout manque encore dans les index courants.
- Le parent resume encore via dossier et closeout draft, pas via un statut final uniformise.

### DECISION
- `CLOSEOUT`

### ACTION_LIST
- Canoniser la fermeture parent dans la continuité documentaire.
- Ne pas rouvrir ce parent sauf nouveau besoin explicite de permissions ou de securite runtime.
- Garder les gaps futurs dans des GO distincts.

### NEXT_GO
- `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01` pour la suite logique deja identifiee, si besoin de formalisation machine-readable.

---

## 3. GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01

### 13_ESTABLISHED
- Le parent est documente par un dossier initial et un closeout parent dedie.
- Les PR #466 et #469 sont citees comme merges stabilisants.
- Le workflow warning-only, le validateur schema et l'artefact de validation sont prouvés dans le closeout.
- Le closeout indique explicitement une sequence `CLOSED_FULL_SEQUENCE`.

### 14_HYPOTHESIS
- Le parent est termine comme phase schema/report, meme si le child schema source attendu manque au chemin reference.
- La suite logique ne doit pas rouvrir le meme parent mais traiter le gap en child ou en correction documentaire separée.

### 15_REMAINING_GAP
- Le fichier canonique attendu `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01.md` n'a pas ete retrouve.
- Aucune propagation canonique finale n'est encore visible dans les index courants.

### DECISION
- `CLOSEOUT`

### ACTION_LIST
- Canoniser la fermeture parent.
- Documenter le child schema manquant comme gap independant.
- Ne pas rouvrir le parent pour ce gap sans GO explicite.

### NEXT_GO
- `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01` uniquement si la restauration du child devient prioritaire.

## DIRTY_WORKTREE_IMPACT

### DIRTY_SCOPE_RELEVANT
- Aucun fichier non suivi clairement rattache a ces 3 parents n'a ete identifie dans cette passe.

### DIRTY_SCOPE_EXTERNAL
- `docs/index/BRANCH_STATE.md`
- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
- `webhook_server.py`
- multiples fichiers non suivis sous `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_*`
- multiples fichiers non suivis sous `docs/chantiers/GO_OPT_TRADING_DB_LAYER_*`
- multiples fichiers non suivis sous `docs/index/inbox/GO_OPT_TRADING_ADMIN_TRADING_*`
- multiples fichiers non suivis sous `docs/index/inbox/GO_OPT_TRADING_DB_LAYER_*`

## 16_TODO
1. Valider ou corriger la decision `ARCHIVE_CANDIDATE` pour `STRICT_WORKERS_PARENT_01`.
2. Canoniser les deux parents OpenClaw en closeout documentaire si l'on veut aligner les index.
3. Reprendre ensuite la reconciliation du worktree dirty hors scope.

## 17_RESUME_POINT
Reprendre a partir de cette liste, puis traiter d'abord `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` comme cas de decision prioritaire avant toute reconciliation du worktree dirty.

## 18_TO_DOCUMENT
- TAGS : `decision_list`, `closeout`, `archive_candidate`, `runtime_security`, `strict_workers`
- Blocs a extraire : table de decision; gaps documentaires; next step par parent

## 19_TO_REMEMBER
MEM_CANDIDATE:
- [Parent ambiguous decision map] : `STRICT_WORKERS` -> `ARCHIVE_CANDIDATE`; `RUNTIME_SECURITY` -> `CLOSEOUT`; `POLICY_REPORT_SCHEMA` -> `CLOSEOUT`.

SAVE_MEMORY:
- Aucun enregistrement memoire durable sans validation utilisateur explicite.

## RISKS

- À qualifier.
