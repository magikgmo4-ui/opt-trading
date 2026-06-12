# PROMPT IDE MASTER — BOTPRESS OPERATOR

## OBJECTIF

Implémenter un opérateur Botpress connecté au pipeline trading existant sans casser les invariants.

## CONTEXTE

Pipeline cible :
Telegram → Botpress → OpenClaw → student/Labs → LONA → opt-trading

## CONTRAINTES

- Aucun trade réel
- Aucun push Git
- Aucun accès exchange
- Botpress = orchestration uniquement

## LIVRABLES ATTENDUS

1. Actions Botpress
2. Gateway OpenClaw
3. Intents + routing
4. Format réponse standard
5. Logs opt-trading

## EXECUTION

1. Lire README du chantier parent
2. Lire architecture cible
3. Implémenter gateway OpenClaw
4. Implémenter actions Botpress
5. Tester E2E

## VALIDATION

- Analyse Telegram fonctionne
- Réponse structurée retournée
- Aucune action dangereuse exécutée

## RISKS

- À qualifier.
