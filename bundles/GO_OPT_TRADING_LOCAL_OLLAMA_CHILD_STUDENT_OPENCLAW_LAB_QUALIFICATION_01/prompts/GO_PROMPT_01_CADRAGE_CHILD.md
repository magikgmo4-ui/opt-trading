# GO_PROMPT_01_CADRAGE_CHILD

## Objectif

Créer le sous-GO de qualification lab/student pour Ollama + OpenClaw.

## GO

```text
GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01
```

## Actions

1. Partir de la branche parent Ollama ou créer une branche enfant dédiée si nécessaire.
2. Créer le dossier :

```text
docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/
```

3. Créer les fichiers :

```text
00_CADRAGE_CHILD.md
01_MACHINE_FACTS.md
02_OLLAMA_FACTS.md
03_OPENCLAW_FACTS.md
04_TEST_MATRIX.md
90_CLOSEOUT.md
```

4. Ajouter immédiatement la trace d'indexation minimale :
   - `BRANCH_STATE.md` si nouvelle branche dédiée ;
   - entrée index dédiée ou `GAP_INDEXATION` explicite.

## Contraintes

- doc-first ;
- aucun runtime patch au cadrage ;
- localhost only ;
- pas `admin-trading` server ;
- pas shell libre ;
- pas trading live.

## Sortie attendue

- cadrage enfant créé ;
- indexation minimale posée ;
- prochaine action = qualification machine student/lab.
