# 13_REMEDIATION_EXECUTION_GATE_REQUEST

## Objectif

Verrouiller les commandes exactes autorisees pour l'application des remediations Phase 6, sans encore les executer.

## Etat des gates avant execution

| Gate | Status | Preuve |
|:-----|:-------|:-------|
| identity | VALIDATED_PROVISIONING_READY | `/home/openclaw/.ssh` cree (700), config `-rw-------` |
| sandbox | VALIDATED_CONFIG_SURFACE_FOUND | `modules/openclaw_config_modulaire/app/agents.json5` : `sandbox {enforce, scope, allow, deny}` |
| SSH alias | VALIDATED_NON_CONNECTIVE | `ssh -G fantome` OK : host `192.168.0.191`, user `fantome` |

## Runtime lock

```text
RUNTIME_REMAINS_BLOCKED
NO_OPENCLAW_AGENT_EXECUTION
NO_SSH_CONNECTION
NO_REMOTE_COMMAND
```

## Commandes autorisees

Seules les commandes listees ci-dessous sont autorisees pour cette passe d'application. Toute commande hors liste necessite une mise a jour de ce document.

### Remediation 1 — identity key

```bash
# Resolution SSH sous openclaw (non-connective)
sudo -u openclaw ssh -G fantome | sed -n '1,120p'
```

**Interdit :** `ssh openclaw@fantome`, `sudo -u openclaw ssh fantome`, copie de cle privee.

### Remediation 2 — sandbox config

```bash
# Lecture avant modification
sed -n '1,220p' modules/openclaw_config_modulaire/app/agents.json5
grep -nE "sandbox|enforce|scope|allow|deny|ssh|remote|path" modules/openclaw_config_modulaire/app/agents.json5
```

**Interdit :** modifier `enforce`, elargir le scope, ou ouvrir le sandbox globalement.

### Remediation 3 — SSH alias

```bash
ssh -G fantome | sed -n '1,120p'
```

**Interdit :** `ssh fantome`, connexion SSH reelle, modification du `~/.ssh/config`.

## Gates d'execution

| Gate | Status | Condition |
|:-----|:-------|:----------|
| EXEC_GATE_IDENTITY | PENDING | `sudo -u openclaw ssh -G fantome` resolvable sans erreur |
| EXEC_GATE_SANDBOX | PENDING | Regles `allow`/`deny` identifiees et minimales |
| EXEC_GATE_SSH_ALIAS | VALIDATED_NON_CONNECTIVE | Alias deja fonctionnel |

## Decision

```text
APPLICATION_AUTHORIZED = NO
```

L'execution reelle n'est pas encore autorisee. Ce document doit etre relu et tranche par l'operateur avant toute commande.

## NEXT_GO

Apres validation de ce gate request :

```text
14_REMEDIATION_APPLY_EXECUTION_LOG.md
```

Role : executer uniquement les commandes autorisees, capturer les sorties, puis decider si le runtime peut etre relance pour un test de bout en bout.

## RISKS

- À qualifier.
