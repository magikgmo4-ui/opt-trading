# CHECKLIST_EXECUTION

## Phase 0 — Repo

- [ ] Branche bundle active : `go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01`
- [ ] Bundle présent : `bundles/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/`
- [ ] Sous-GO créé ou cadré
- [ ] Indexation minimale appliquée immédiatement

## Phase 1 — Machine student/lab

- [ ] OS identifié
- [ ] CPU identifié
- [ ] RAM mesurée
- [ ] GPU/VRAM identifié si disponible
- [ ] disque libre vérifié
- [ ] verdict machine posé

## Phase 2 — Ollama

- [ ] `ollama --version`
- [ ] `ollama list`
- [ ] port `11434` local
- [ ] API version
- [ ] API tags
- [ ] chat simple
- [ ] JSON structuré

## Phase 3 — OpenAI/OpenClaw

- [ ] client OpenAI-compatible testé
- [ ] OpenClaw installé ou absent documenté
- [ ] provider local vérifié
- [ ] outils élevés désactivés ou statut inconnu documenté
- [ ] logs identifiés
- [ ] mode read-only évalué

## Phase 4 — RAG / reprise GO

- [ ] embeddings testés ou non testés documenté
- [ ] corpus read-only défini
- [ ] citations locales prévues
- [ ] aide reprise GO évaluée

## Phase 5 — Verdict

- [ ] `READY`
- [ ] `LIMITED`
- [ ] `LAB_ONLY`
- [ ] `REJECT`

## Stop conditions

Stop si :

- exposition publique détectée ;
- demande de shell libre ;
- demande de trading live ;
- demande d'écriture repo automatique ;
- OpenClaw exige des outils élevés non contrôlés ;
- secrets détectés dans les prompts ou corpus.
