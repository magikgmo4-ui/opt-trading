---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01_TRIGGER_OPTIONS
doc_type: trigger_and_scheduling_options
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 30_TRIGGER_AND_SCHEDULING_OPTIONS - Trigger and Scheduling Options

## Matrice

| Option | Declencheur | Avantage | Risque | Precondition | Recommandation |
| --- | --- | --- | --- | --- | --- |
| Timer systemd Desk Pro | timer periodique | simple a operer | active le runtime trop tot | timer spec + observabilite | plus tard |
| Worker CLI manuel puis timer | commande manuelle d'abord | validation progressive | demande plus d'operations manuelles | dry-run impl | **oui** |
| Trigger apres `desk_bridge` | snapshot frais quasi garanti | bonne proximite des donnees visuelles | couplage fort au bridge | contrat de hook / wrapper | plus tard |
| Trigger apres `signal_event` | reaction rapide au signal | riche pour event-driven | risque de snapshots non encore frais | normalisation + buffering | non en premier |
| Batch periodique read-only | boucle periodique sans action live | robustesse, simplicite | peut analyser du stale | definition freshness/gates | **oui** |
| Dry-run permanent avant live | meme trigger qu'automatisation future | securite maximale | demande phase supplementaire | dry-run outputs + observabilite | **obligatoire** |

## Lecture des options

- Le meilleur premier pas n'est pas un timer systemd actif
- Le meilleur premier pas est un **worker CLI dry-run** reutilisable manuellement puis branchable plus tard a un timer
- Le second choix le plus sain est un **batch periodique read-only** base sur fichiers frais
- Les options evenementielles (`signal_event` ou `desk_bridge`) doivent venir apres validation du worker et de ses gates

## Recommendation de scheduling

1. D'abord un runner dry-run manuel
2. Ensuite une spec de timer dediee
3. Ensuite seulement un timer systemd non-live
4. Enfin un smoke runtime gate avant tout mode plus autonome
