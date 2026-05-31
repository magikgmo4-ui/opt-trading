---
doc_id: OPENCLAW_LOOP_FORMAT_05
doc_type: loop_contract_format
segment: human_gate
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_LOOP_CONTRACT_01
updated_at: 2026-05-30
---

# FORMAT 5 — Gate humain : Validation opérateur

## Rôle

L'opérateur humain répond à la synthèse OpenClaw (FORMAT 4) avec une décision
explicite. Cette décision est le seul mécanisme qui autorise un merge, un push,
ou une relance de la boucle. OpenClaw ne peut jamais s'auto-approuver.

## Schéma (YAML)

```yaml
gate_response:
  # Obligatoires
  job_id: string            # repris du FORMAT 1
  instruction_id: string    # repris du FORMAT 2
  decision: enum            # APPROVE | REJECT | RESTART
  decided_at: string        # ISO 8601
  decided_by: string        # identifiant opérateur (ex: "ghost", "operator")
  motif: string             # raison de la décision (obligatoire dans tous les cas)

  # Si RESTART
  correction: string | null  # ce qui doit changer dans le prochain job spec

  # Si APPROVE avec merge
  authorize_merge: bool      # true = OpenClaw peut soumettre la PR
  authorize_push: bool       # true = OpenClaw peut push (avec --force-with-lease si nécessaire)
```

## Décisions

| Décision | Signification | Effet sur la boucle |
| --- | --- | --- |
| `APPROVE` | Opérateur valide le résultat | OpenClaw peut merger/pusher si autorisé |
| `REJECT` | Opérateur rejette — abandon | Boucle close, aucune action sur le repo |
| `RESTART` | Opérateur veut une relance avec corrections | OpenClaw génère un nouveau FORMAT 1 avec la correction |

## Templates

### APPROVE

```yaml
gate_response:
  job_id: "JOB_YYYYMMDD_NNN"
  instruction_id: "INSTR_YYYYMMDD_NNN_A"
  decision: "APPROVE"
  decided_at: "2026-05-30T00:00:00Z"
  decided_by: "ghost"
  motif: "résultat conforme à l'intent, fichiers vérifiés"
  correction: null
  authorize_merge: true
  authorize_push: false
```

### REJECT

```yaml
gate_response:
  job_id: "JOB_YYYYMMDD_NNN"
  instruction_id: "INSTR_YYYYMMDD_NNN_A"
  decision: "REJECT"
  decided_at: "2026-05-30T00:00:00Z"
  decided_by: "ghost"
  motif: "résultat hors scope — fichiers non attendus modifiés"
  correction: null
  authorize_merge: false
  authorize_push: false
```

### RESTART

```yaml
gate_response:
  job_id: "JOB_YYYYMMDD_NNN"
  instruction_id: "INSTR_YYYYMMDD_NNN_A"
  decision: "RESTART"
  decided_at: "2026-05-30T00:00:00Z"
  decided_by: "ghost"
  motif: "intent mal interprété"
  correction: "restreindre scope à docs/openclaw/ uniquement, ignorer modules/"
  authorize_merge: false
  authorize_push: false
```

## Règles absolues

```
1. OpenClaw ne s'auto-approuve jamais.
2. authorize_merge = true uniquement si decision = APPROVE.
3. authorize_push = true uniquement si decision = APPROVE et --force-with-lease accepté.
4. motif obligatoire dans tous les cas — pas de gate silencieuse.
5. RESTART exige une correction non nulle.
6. Une gate REJECT close la boucle — aucune action sur le repo ne suit.
```

## Modes d'échec segment 5

| Erreur | Cause | Résolution |
| --- | --- | --- |
| `SELF_APPROVE` | OpenClaw tente de s'approuver | Violation — stopper immédiatement |
| `MISSING_MOTIF` | motif vide ou null | Exiger un motif explicite |
| `RESTART_NO_CORRECTION` | RESTART sans correction | Fournir le champ correction |
| `APPROVE_WITH_MERGE_ON_FAIL` | authorize_merge sur verdict FAIL | Impossible — bloquer |

## Chaîne de commandement

```
APPROVE → OpenClaw exécute merge/push dans les limites autorisées → boucle termine
REJECT  → boucle ferme → aucune action repo
RESTART → OpenClaw génère FORMAT 1 corrigé → nouvelle itération boucle
```
