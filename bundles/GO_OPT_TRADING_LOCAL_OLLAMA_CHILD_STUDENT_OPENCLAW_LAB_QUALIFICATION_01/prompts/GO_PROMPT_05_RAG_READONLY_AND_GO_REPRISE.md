# GO_PROMPT_05_RAG_READONLY_AND_GO_REPRISE

## Objectif

Préparer un RAG local read-only sur les docs de continuité et valider l'aide à la reprise GO.

## Corpus initial

```text
docs/governance/
docs/index/
docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/
docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01/
```

## Sortie attendue RAG

```json
{
  "answer": "...",
  "sources": ["path#section"],
  "confidence": "low|medium|high",
  "remaining_gap": ["..."]
}
```

## Usage GO reprise

Le RAG doit aider à extraire :

```text
1_MASTER_TARGET=
7_CANONICAL_STATE=
11_KEY_DECISIONS=
12_INVARIANTS=
13_ESTABLISHED=
14_HYPOTHESIS=
15_REMAINING_GAP=
16_TODO=
17_RESUME_POINT=
GO_PROMPT=
```

## Contraintes

- read-only ;
- citations locales obligatoires ;
- pas d’écriture repo ;
- pas d’archives mélangées sans signalement ;
- pas de décision runtime ;
- pas de secrets dans corpus.

## Verdict

```text
EMBEDDINGS=PASS|FAIL|NOT_TESTED
RAG_READONLY=READY|LIMITED|LAB_ONLY|REJECT
GO_REPRISE_HELPER=READY|LIMITED|LAB_ONLY|REJECT
NEXT_STEP=
```
