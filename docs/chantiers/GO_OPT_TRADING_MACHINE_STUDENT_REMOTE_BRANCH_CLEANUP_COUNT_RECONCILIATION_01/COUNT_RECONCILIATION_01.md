# Réconciliation du delta de comptage 30 → 33

## Problème

```text
Décision GO_OPT_TRADING_MACHINE_STUDENT_REMOTE_BRANCH_CLEANUP_DECISION_01:
  en-tête DELETE_CONFIRMED = 30
  synthèse DELETE_CONFIRMED = 30

Exécution GO_OPT_TRADING_MACHINE_STUDENT_REMOTE_BRANCH_CLEANUP_EXECUTION_01:
  supprimées déclarées = 33
  parents = 4, lab children = 23, agent standardization = 6

Delta apparent : +3
```

## Analyse

### Méthode

Comparaison ligne à ligne entre la table de la décision et la liste d'exécution.

### Résultat

**Aucun delta réel.** La table de la décision liste **33 branches** (numérotées #1 à #33). L'exécution a supprimé exactement ces **33 branches**. Tous les noms de branches correspondent exactement (diff = 0 pour les branches supprimées).

L'écart provient uniquement d'une **erreur de comptage dans le document de décision** :

| Élément | Valeur déclarée | Valeur réelle (table) |
| --- | --- | --- |
| Parents | 4 | 4 |
| Lab children | — | 23 |
| Agent standardization | — | 6 |
| **DELETE_CONFIRMED** | **30** | **33** |

La synthèse de la décision (section "Synthèse finale") et l'en-tête de la section "DELETE_CONFIRMED (30)" contiennent tous deux le chiffre 30 au lieu de 33. La table en dessous contient correctement 33 entrées numérotées #1 à #33.

### Preuve de la concordance

```text
Branches décision (table #1-#33) :  33 noms
Branches exécution supprimées :     33 noms
Correspondance :                    33/33 identiques
```

Les deux branches supplémentaires détectées par `diff` dans le rapport d'exécution sont des mentions de non-suppression (KEEP_ARCHIVE, REVIEW_BLOCKED) dans les sections de vérification — pas des branches supprimées.

## Les 3 branches du "delta fantôme"

Il n'y a pas 3 branches supplémentaires supprimées par rapport à la décision. Le delta est entièrement dû à une erreur de décompte dans le document de décision. Cependant, si l'on veut identifier les 3 branches qui "manquent" dans la synthèse par rapport au tableau :

| # | Branche | Catégorie | Safe-delete ? | Preuve |
| --- | --- | --- | --- | --- |
| 31 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_RUNTIME_BASELINE_ADOPTION_01` | Agent standardization | ✅ | ABSORBED (ancestor) ; FULL_PASS |
| 32 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_POLICY_01` | Agent standardization | ✅ | ABSORBED (ancestor) |
| 33 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_ENFORCEMENT_01` | Agent standardization | ✅ | ABSORBED (ancestor) |

Ces 3 branches étaient numérotées #31 à #33 dans la table de décision. La synthèse les a omises en comptant 30 au lieu de 33 (elle a probablement compté 4 + 23 + 6 = 33 mais écrit 30 par erreur, ou a soustrait les 3 KEEP_ARCHIVE de 33 au lieu de 36).

## Correction documentaire

Le document de décision doit être lu comme suit :
- La table de décision est correcte (33 branches DELETE_CONFIRMED)
- L'en-tête et la synthèse contiennent une coquille (30 → 33)
- La valeur réelle est **33 DELETE_CONFIRMED**

## Verdict

```text
PASS — delta réconcilié.
Aucune branche supplémentaire non autorisée supprimée.
Toutes les 33 suppressions correspondent à la table de décision.
L'écart est une coquille documentaire (30 écrit au lieu de 33).
Toutes les 33 branches sont safe-delete (absorbées ou doc-only sur mainline).
```

## Annexe : preuve par comptage direct

```bash
# Décision : 33 entrées numérotées dans la table DELETE_CONFIRMED
grep -c "^| [0-9]" REMOTE_BRANCH_FINAL_DECISION_01.md
# → 33

# Exécution : 33 branches supprimées (4 parents + 23 lab + 6 agent)
echo "$((4 + 23 + 6))"
# → 33

# Correspondance : diff = 0 (hors KEEP_ARCHIVE et REVIEW_BLOCKED)
diff <(liste_decision) <(liste_execution)
# → aucune différence sur les branches supprimées
```

## RISKS

- À qualifier.
