# 03_TOOL_POLICY_PATCH_PLAN

## Objectif

Préparer le patch minimal de tool policy OpenClaw pour lever le blocage SSH/network sans modifier globalement `sandbox.mode`.

## Source

- `01_SANDBOX_SCHEMA_SOURCE_AUDIT.md`
- `02_SANDBOX_PATCH_DECISION_MATRIX.md`

## Pivot canonique

```text
Le blocage réel n'est pas sandbox.mode.
Le blocage réel est deny: ["group:runtime"] sur certains agents.
```

## Correction de l'audit précédent

La liste des agents portant `group:runtime` dans leur `deny` est plus précise que supposé :

| Agent | `group:runtime` dans deny | Evidence (ligne) |
| :--- | :--- | :--- |
| orchestrateur | **NON** — allow list explicite | `agents.json5:40` |
| builder | **OUI** | `agents.json5:65` |
| reviewer | **NON** — deny = `[browser, canvas, nodes, cron, gateway]` uniquement | `agents.json5:89` |
| lab | **OUI** | `agents.json5:111` |

Seuls `builder` et `lab` ont `group:runtime` bloqué.

## État actuel

| Surface | Statut |
| :--- | :--- |
| sandbox.mode | ne pas modifier |
| builder deny group:runtime | blocage confirmé |
| lab deny group:runtime | blocage confirmé |
| reviewer deny group:runtime | absent — pas bloqué par cette règle |
| orchestrateur | allow list ciblée — pas de deny runtime |
| patch global | déconseillé |
| elevated tools | déconseillé |
| runtime | bloqué |

## Décision de stratégie

```text
SELECTED_STRATEGY = AGENT_SCOPED_TOOL_POLICY_PATCH
```

## Option retenue provisoire

| Option | Statut | Condition |
| :--- | :--- | :--- |
| A — retirer `group:runtime` du deny de l'agent ciblé | PREFERRED | seulement si l'agent exact est confirmé |
| B — ajouter allow ciblé | FALLBACK | seulement si les noms d'outils exacts sont prouvés |
| C — patch global | REJECTED | trop large |
| D — elevated | REJECTED | surface de risque élevée |
| E — ne rien modifier | FALLBACK_BLOCKED | si agent cible non confirmé |

## Agent target gate

| Agent | `group:runtime` bloquant | Candidat patch | Gate |
| :--- | :--- | :--- | :--- |
| orchestrateur | NON | NON | skip |
| builder | OUI | POSSIBLE | `TARGET_AGENT_CONFIRMED` requis |
| reviewer | NON | NON | skip |
| lab | OUI | POSSIBLE | `TARGET_AGENT_CONFIRMED` requis |

Question à trancher dans `04_TOOL_POLICY_TARGET_AGENT_AUDIT.md` :

```text
Quel job OpenClaw nécessite SSH/network ?
builder ? lab ? les deux ?
```

## Patch autorisé uniquement si

```text
TARGET_AGENT_CONFIRMED = true
PATCH_SCOPE = single agent (builder OU lab, pas les deux sans justification)
RUNTIME = blocked
ROLLBACK = git restore modules/openclaw_config_modulaire/app/agents.json5
```

## Patch candidat — Option A

Retirer uniquement `group:runtime` du tableau `deny` de l'agent cible.

Exemple conceptuel pour `builder` :

```json5
// avant
deny: [
  "group:runtime",
  "browser",
  "canvas",
  "nodes",
  "cron",
  "gateway",
],

// après Option A
deny: [
  "browser",
  "canvas",
  "nodes",
  "cron",
  "gateway",
],
```

Ne pas appliquer à `lab` simultanément sans décision explicite séparée.

## Patch candidat — Option B

Ajouter des outils spécifiques dans `allow` seulement si les noms exacts sont prouvés.

```text
STATUS = BLOCKED_UNTIL_TOOL_NAMES_CONFIRMED
```

Noms probables non encore vérifiés localement : `ssh`, `exec_remote`, `network`, etc.

## Précheck avant patch

```bash
git status --short --branch
sed -n '1,260p' modules/openclaw_config_modulaire/app/agents.json5
grep -nE "id:|deny:|group:runtime" modules/openclaw_config_modulaire/app/agents.json5
```

## Rollback

```bash
git restore -- modules/openclaw_config_modulaire/app/agents.json5
```

## Stop conditions

Arrêt immédiat si :

* l'agent cible reste ambigu entre builder et lab ;
* le patch touche plusieurs agents sans décision explicite ;
* le patch modifie `sandbox.mode` ;
* le patch active elevated tools ;
* un runtime OpenClaw est requis pour valider le plan ;
* une connexion SSH réelle est demandée ;
* un secret est requis ;
* impact WAN, bridge, admin-trading ou closeout DB_LAYER.

## NEXT_GO

Créer ensuite :

```text
04_TOOL_POLICY_TARGET_AGENT_AUDIT.md
```

Rôle :

1. lire précisément les rôles de `builder` et `lab` dans la config et la doc module ;
2. identifier lequel des deux doit exécuter SSH/network selon l'architecture du job ;
3. décider `TARGET_AGENT_CONFIRMED` ;
4. autoriser ou bloquer le patch.
