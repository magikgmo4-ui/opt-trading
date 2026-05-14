# 01_BUILDER_FIRST_JOB_GATE

## Objectif

Définir le premier job builder contrôlé via gateway OpenClaw V2, sans exécution dans ce document.

## État de départ

```text
Gateway V2 = UP_AND_STABLE
orchestrateur = ALIVE
builder = ALIVE
SSH réel = BLOCKED
remote command = BLOCKED
runtime job builder réel = PENDING_GATE
```

## Invariants

```text
Aucun SSH réel.
Aucune commande remote.
Aucun patch runtime.
Aucun secret dans le repo.
Aucun WAN.
Aucun bridge.
Aucun admin-trading.
Aucun closeout DB_LAYER rouvert.
Validation humaine obligatoire avant exécution.
```

---

## Job proposé

Demander au builder une sortie structurée strictement documentaire.

### Commande prévue

```bash
openclaw agent --agent builder \
  --message "Return a JSON object only with keys: status, role, constraints, next_step. status must be BUILDER_CONTROLLED_JOB_OK. Do not run commands. Do not modify files. Do not use SSH. Do not call remote systems." \
  --json
```

### Preuve attendue

Le builder doit répondre avec un payload contenant un JSON structuré :

```json
{
  "status": "BUILDER_CONTROLLED_JOB_OK",
  "role": "...",
  "constraints": "...",
  "next_step": "..."
}
```

### Interdictions

```text
Aucun SSH.
Aucune commande remote.
Aucun patch.
Aucun accès WAN.
Aucun secret.
Aucun changement fichier.
Aucun job multi-step autonome.
```

---

## Stop conditions

Arrêt immédiat si :

```text
- le builder tente d'exécuter une commande shell
- le builder demande un secret ou des credentials
- le builder propose SSH ou remote exec
- la réponse n'est pas un JSON structuré valide
- le gateway devient instable (health ko)
- une session non attendue apparaît sur un autre agent
- le builder sort du périmètre du message (lecture de fichiers, écriture, etc.)
```

---

## Gate humaine

```text
BUILDER_FIRST_CONTROLLED_JOB_REQUIRES_HUMAN_VALIDATION = true
```

Conditions d'approbation :

1. Opérateur confirme que le message est non destructif.
2. Opérateur confirme qu'aucune commande shell ne sera exécutée.
3. Opérateur accepte qu'une session soit créée dans `agents/builder/sessions/`.
4. Stop conditions comprises et opérateur prêt à intervenir.

---

## NEXT_GO

Si validation humaine reçue :

```text
02_BUILDER_FIRST_JOB_EXECUTION_LOG.md
```

Si refus ou blocage :

```text
02_BUILDER_FIRST_JOB_BLOCKED_REPORT.md
```
