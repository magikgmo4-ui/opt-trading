---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: crosscheck
repo: opt-trading
status: open
created_at: 2026-05-17
surface: doc-only
---

# 10_PR_AND_EXISTING_SURFACES_CROSSCHECK

---

## 1_OBJECTIF

Recroiser le cadre strategie avec les PR et surfaces existantes avant de figer
les documents de schema, lifecycle et consumers.

Conclusion structurante :

```text
Le cadre strategie doit etendre ObservationEvent et les consumers existants.
Il ne doit pas creer de pipeline parallele.
```

---

## 2_PR_CROSSCHECK

| PR | Etat | Fait etabli | Implication pour ce parent |
| --- | --- | --- | --- |
| `#524` ObservationEvent schema | MERGED, 2026-05-17 | Pose `ObservationEvent` V1 par run et `ObservationSummary`; mentionne l'ajout futur de `strategy_id`. | Le champ strategie devient extension canonique de `ObservationEvent`, pas un schema concurrent. |
| `#522` Product roadmap | MERGED, 2026-05-17 | Replace db-layer comme couche produit/support; cible input -> normalisation -> persistence -> query -> dashboard. | Les strategies doivent alimenter la data plane via observation enrichie. |
| `#514` Phase 1 observation | MERGED, 2026-05-17 | Observation 30 runs / 14 jours; dry-run only; no live / no Bitget / no Sheets auto. | Une strategie commence en observation et attend des preuves temporelles et volumetriques. |
| `#513` Kill switch + Telegram dry-run | MERGED, 2026-05-17 | Kill switch et Telegram dry-run testes; dispatcher dry-run ne poste pas. | Telegram strategie reste watch-only et dry-run tant que les gates ne sont pas satisfaites. |
| `#512` Paper mode expansion decision | MERGED, 2026-05-17 | Sequence C -> A en parallele -> B multi-signal apres seuils -> D live doc-only. | Les strategies suivent les seuils paper/multi-signal, elles ne les contournent pas. |
| `#510` Live readiness surface audit | MERGED, 2026-05-17 | Live readiness doc-only; criteres, refusal criteria, no activation. | Le dernier etat strategie est `LIVE_REVIEW_ONLY`, jamais live direct. |
| `#509` LocalCMS metrics dashboard | MERGED, 2026-05-17 | Ajoute `/metrics`, `/metrics/daily`, `_build_metrics()`, lecture daily journal. | LocalCMS strategy view doit consommer les memes journaux et metrics, en lecture seule. |

---

## 3_LOCAL_SURFACES_CROSSCHECK

| Surface | Evidence locale | Lecture canonique |
| --- | --- | --- |
| `scripts/tmux/sessions/screeners.sh` | Session `screeners` avec fenetres `tradingview`, `webhook`, `bot_vision`, `telegram`. | Les producteurs de signal existent deja; le cadre strategie doit les normaliser via `ObservationEvent`. |
| `modules/bot_vision_step2/app/bot_vision_step2.py` | Prompt OpenAI demande `bias`, `structure`, `supports`, `resistances`, `plan`, `invalidation`; artefacts `summary.json`, `analysis.txt`, `analysis.md`; Telegram optionnel. | Bot Vision est une source d'evidence et d'enrichissement, pas une source de decision autonome. |
| `modules/localcms/app/main.py` | `JOURNAL_DIR = data/journal/daily`; endpoints `/journal/daily`, `/journal/daily/{run_id}`, `/metrics`, `/metrics/daily`; `_build_metrics()` agrege P&L, win rate, observation thresholds et sync Sheets. | LocalCMS peut devenir consumer read-only strategie sans changer le producteur journal. |
| `modules/notification_dispatcher/app/events.py` | Template Telegram `signal_received` contient deja `Strategy: {strategy_id}`. | `strategy_id` est deja une notion attendue par Telegram; il faut formaliser son origine et ses gates. |
| `modules/notification_dispatcher/app/dispatcher.py` | `dry_run=True` retourne le message sans `requests.post`; live sans env vars retourne erreur controlee. | Watch signal strategie doit utiliser ce comportement pour rester non-executant. |

---

## 4_EXISTING_OBSERVATION_EVENT_FACTS

PR #524 documente :

| Element | Etat actuel |
| --- | --- |
| `ObservationEvent` | `run_id`, `session_id`, `run_date`, `started_at`, `status`, `dry_run`, `paper_mode`, `outcome`, `pnl_net`, `localcms_ok`, `closeout_required`, `ingested_at` |
| `ObservationSummary` | `total_runs`, `pass_count`, `fail_count`, `pnl_cumulative`, `win_rate`, `days_elapsed`, `runs_to_threshold`, `days_to_threshold`, `eligible` |
| Evolution prevue | ajout de champs comme `signal_ticker`, `strategy_id` |

Decision parent :

```text
strategy_id et strategy_version deviennent requis pour toute nouvelle strategie.
Les anciens runs peuvent rester sans ces champs; les nouveaux signaux strategie ne le peuvent pas.
```

---

## 5_GAPS_A_RESPECTER

| Gap | Decision |
| --- | --- |
| LocalCMS n'expose pas encore une vue strategie dediee | Definir requirements read-only, pas modifier runtime dans ce parent. |
| Perf Engine strategie non formalise | Definir inputs et metrics a partir de `ObservationEvent`. |
| Telegram peut afficher une strategie mais ne connait pas encore les gates | Ajouter protocole `WATCH`, pas `BUY/SELL`. |
| Bot Vision produit une lecture riche mais non canonique | Mapper en evidence, jamais en decision unique. |
| Google Sheets sync existe mais doit rester controle | Mapping export uniquement, pas write automatique. |

---

## 6_CANONICAL_DECISION

```text
Toute strategie candidate devient une Canonical Strategy Spec.
Toute observation strategie enrichit ObservationEvent.
Tout consumer lit ObservationEvent ou ses agregats.
Aucun module strategie ne cree sa propre chaine producteur -> decision -> execution.
```

## RISKS

- À qualifier.
