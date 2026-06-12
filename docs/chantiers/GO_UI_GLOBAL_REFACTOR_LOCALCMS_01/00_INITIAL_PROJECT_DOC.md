# GO UI GLOBAL REFACTOR LOCALCMS 01 — Initial Project Doc

## 1. Resume executif

Ce chantier refactorise l'ensemble des surfaces UI du repo `opt-trading-clean` vers un systeme coherent, stable et reutilisable. Inspecte en profondeur le 2026-06-12 sur l'etat post-PR #1130 (SpaceX Command Center).

### Etat des lieux

- **3 services** servent des pages HTML : `perf_app.py` (8010), `webhook_server.py` (8000), et `modules/localcms/app/main.py` monte dans perf_app
- **13 routes HTML** et **34 routes JSON** liees aux UI
- **25 fonctions** generent du HTML inline (f-strings exclusivement)
- **17 blocs CSS inline** repartis dans les strings Python — aucun fichier `.css` dedie
- **Aucun moteur de template** (pas de Jinja2) — tout est en f-strings Python
- **2 systemes de layout concurrents** : Light (LocalCMS, `#f5f5f7`) et Dark (perf, webhook, `#0a0e14`)
- **6 pages avec auto-refresh** (2s a 60s selon la page)
- **3 chemins redondants** pour generer du HTML SpaceX
- **0 helpers Python partages** pour la generation HTML — duplication massive de `<style>`, badges, cards

### Objectif

Un design system minimal, server-rendered, base sur le style LocalCMS Apple-light comme style canonique, avec des helpers partages exploitables par tous les modules sans casser l'existant.

---

## 2. Inventaire UI complet

### 2.1 Routes HTML (13 routes)

| # | Fichier | Route | Methode | Fonction | Theme | Auto-refresh |
|---|---------|-------|---------|----------|-------|--------------|
| 1 | `perf/perf_app.py:62` | `/` | GET | `unified_index()` | Dark (#0a0e14) | Non |
| 2 | `perf/perf_app.py:585` | `/perf/ui` | GET | `perf_ui()` | Dark (#0b0d10) | 5s opt-in |
| 3 | `webhook_server.py:748` | `/dash` | GET | `dash()` | Dark (#0b1020) | 2s XHR |
| 4 | `modules/localcms/app/main.py:1074` | `/` (cms) | GET | `ui_index()` | Light (#f5f5f7) | 30s |
| 5 | `modules/localcms/app/main.py:562` | `/metrics` | GET | `metrics_html()` | Light (#f5f5f7) | Non |
| 6 | `modules/localcms/app/main.py:1074` | `/journal` | GET | `journal_html()` | Light (#f5f5f7) | Non |
| 7 | `modules/localcms/app/main.py:1074` | `/journal/{run_id}` | GET | `journal_detail_html()` | Light (#f5f5f7) | Non |
| 8 | `modules/localcms/app/main.py:1074` | `/credentials` | GET | `credentials_html()` | Light (#f5f5f7) | Non |
| 9 | `modules/localcms/app/main.py:1710` | `/signals` | GET | `signals_page()` | Dark (#0d1117) | 30s |
| 10 | `modules/localcms/app/main.py:1987` | `/spacex` | GET | `spacex_html()` | Light (#f5f5f7) | 60s |
| 11 | `modules/desk_pro/api/routes.py:457` | `/desk/ui` | GET | `ui()` | Light (#fff) | Non |
| 12 | `modules/desk_pro/api/routes.py:323` | `/desk/toolbox` | GET | `desk_toolbox()` | Light (#fff) | Non |
| 13 | `modules/desk_pro/api/routes.py:561` | `/desk/spacex/ui` | GET | `desk_spacex_ui()` | Light (#f5f5f7) | 60s |

### 2.2 Routes JSON liees aux UI (34 routes)

**perf_app (4)** : `/perf/summary`, `/perf/open`, `/perf/trades`, `/perf/event`
**webhook_server (4)** : `/api/state`, `/api/events`, `/api/metrics`, `/api/risk/status`
**localcms (17)** : `/health`, `/menu`, `/menu/state`, `/runtime/tmux`, `/runtime/tmux/live`, `/data-center/health`, `/journal/daily`, `/journal/daily/{run_id}`, `/metrics/daily`, `/credentials/json`, `/signals/summary`, `/signals`, `/signals/channels`, `/vision/summary`, `/backtest/summary`, `/backtest/csv`, `/spacex/json`
**desk_pro (15)** : `/desk/health`, `/desk/status`, `/desk/errors`, `/desk/alerts`, `/desk/alert/test`, `/desk/snapshot`, `/desk/form`, `/desk/vision`, `/desk/vision/news`, `/desk/vision/screener`, `/desk/vision/telegram-claim`, `/desk/spacex`, `/desk/spacex/snapshot`, `/desk/spacex/command-center`, `/desk/logs/latest`

### 2.3 Fonctions de generation HTML (25 fonctions)

| Fichier | Fonction(s) | Type |
|---------|------------|------|
| `modules/desk_pro/ui/page.py` | `render_ui_html()` | Page complete (618 lignes) |
| `modules/localcms/app/main.py` | `_metrics_html()`, `_journal_html()`, `_journal_detail_html()`, `_credentials_html()`, `_spacex_html()`, `signals_page()` (inline), `ui_index()` (inline) | Pages completes |
| `modules/localcms/app/main.py` | `_pnl_badge()`, `_verdict_badge()`, `_closeout_badge()`, `_cred_status_badge()`, `_cred_update_cmd()`, `STATUS_BADGES` | Fragments HTML |
| `modules/ipo_tracking/ui/spacex_page.py` | `render_static_page()`, `write_static_page()` | Page statique (42 lignes) |
| `modules/ipo_tracking/reports.py` | `write_ui()`, `write_daily_report()` | Generation fichier (43 lignes) |
| `modules/ipo_tracking/reports/__init__.py` | `write_ui()` (duplique) | Generation fichier |
| `modules/desk_pro_dashboard/app/desk_pro_dashboard.py` | `render_html()`, `export_html()` | Export batch (355 lignes) |
| `webhook_server.py` | `DASH_HTML` (constante inline) | Page complete (~200 lignes HTML) |
| `perf/perf_app.py` | `unified_index()` inline, `perf_ui()` inline | Pages completes (~500+ lignes HTML) |
| `modules/desk_pro/api/routes.py` | `desk_toolbox()` inline, `desk_spacex_ui()` inline | Pages completes |

### 2.4 Fichiers CSS et blocs inline (17 blocs + 5 fichiers standalone)

**Aucun fichier `.css` dedie n'existe dans le repo.** Tout est inline dans `<style>` blocks.

| Fichier | Bloc(s) | Theme |
|---------|---------|-------|
| `perf/perf_app.py` | 2 blocs (landing + perf/ui) | Dark |
| `webhook_server.py` | 1 bloc (DASH_HTML) | Dark |
| `modules/desk_pro/ui/page.py` | 1 bloc | Light (#fff) |
| `modules/desk_pro/api/routes.py` | 2 blocs (toolbox + spacex/ui) | Light |
| `modules/localcms/app/main.py` | 7 blocs (ui, metrics, journal, journal_detail, signals, credentials, spacex) | 6 Light + 1 Dark |
| `modules/desk_pro_dashboard/app/desk_pro_dashboard.py` | 1 bloc | Dark (#111) |
| `modules/ipo_tracking/reports.py` | 1 bloc | Dark (#0b0d12) |
| `modules/ipo_tracking/reports/__init__.py` | 1 bloc (duplique) | Dark |
| `modules/ipo_tracking/ui/spacex_page.py` | 1 bloc inline | Dark (#0b0f14) |

Fichiers HTML standalone avec CSS :
- `ui/spacex_desk/index.html` (SPCX Command Center — peut etre ecrase par `spacex_page.py`)
- `modules/hf_free_platform/spaces/portal_static/index.html` (HF Portal)
- `registry/cockpit/automation/index.html` (mockup design)
- `docs/screenshots/desk_ui.html`, `desk_toolbox.html` (snapshots doc)

---

## 3. Cartographie des patterns

### 3.1 Layout

Deux systemes concurrents identifiables :

**Systeme Light (LocalCMS canonique) — 7 pages**
- `body` : `#f5f5f7` background, `#1d1d1f` text
- Sidebar 240px fixe (`.layout: grid 240px 1fr`) avec `position: sticky`
- Sidebar : `#1d1d1f` fond fonce, texte `#f5f5f7`
- `.nav-item` : flex, gap 8px, padding 6px 10px, border-radius 8px
- `.main` : padding 24px 32px, max-width 1200px
- `.summary-bar` : flex, gap 16px, wrap

**Systeme Dark (webhook, perf, signals, ipotracking, desk_dashboard) — 7+ pages**
- `body` : `#0a0e14` a `#0b1020`, texte clair
- Pas de sidebar
- Cards avec `#121820`, border `#1e2733`
- Pas de layout grid fixed — body-centered

### 3.2 Cards

| Module | Classe | Background | Border | Border-radius | Padding |
|--------|--------|-----------|--------|---------------|---------|
| LocalCMS (Light) | `.card-row` | `#fff` | `1px solid #e6e6e6` | 12px | 16px |
| LocalCMS (Light) | `.summary-card` | `#fff` | `1px solid #e6e6e6` | 12px | 16px |
| LocalCMS (Light) | `.domain-card` | `#fff` | `1px solid #e6e6e6` | 12px | 14px 16px |
| perf (Dark) | `.card` | `#121820` | `1px solid #1e2733` | 14px | 20px |
| Desk Pro (Light) | `.card` | none | `1px solid #ddd` | 10px | 14px |
| webhook (Dark) | `.card` | none | `1px solid #1a2540` | 14px | 18px |

### 3.3 Badges / Status chips

**LocalCMS (Light) — systeme de badges le plus complet et coherent :**
- `.badge` base : inline-block, padding 2px 8px, border-radius 999px, font-size 11px, font-weight 600
- `.badge-up` : green `#d1fae5` / `#065f46` (WIN, APPROVED, ✓ CLOSED, operational)
- `.badge-down` : red `#ffe4e6` / `#9f1239` (LOSS, REJECTED, ⚠ PENDING)
- `.badge-minimal` : yellow `#fef3c7` / `#92400e` (BREAKEVEN)
- `.badge-unknown` : gray `#f3f4f6` / `#6b7280`
- `.badge-critical` : yellow, font-size 10px
- `.badge-noncrit` : blue `#e0e7ff` / `#3730a3`
- `.badge-impl` : blue `#dbeafe` / `#1e40af`
- `.badge-partial` : yellow
- `.badge-to_build` : purple `#f3e8ff` / `#6b21a8`
- `.badge-closed` : gray `#e5e7eb` / `#374151`
- `.badge-deprecated` : pink `#fce7f3` / `#9d174d`
- `.cred-set` : green pill `#d1fae5` / `#065f46`
- `.cred-absent` : red pill `#ffe4e6` / `#9f1239`
- `.cred-unknown` : gray pill `#f3f4f6` / `#6b7280`
- `.cred-future` : indigo pill `#e0e7ff` / `#3730a3`

**Desk Pro — systeme minimal :**
- `.pill` : inline-block, padding 2px 8px, border 1px solid #ddd, border-radius 999px, font-size 12px

**perf (Dark) — systeme different :**
- `.chip` / `.status-chip` : border-radius 8px, pas de pill shape

**webhook (Dark) — minimal :**
- `.badge.buy` / `.badge.sell` / `.badge.ok` / `.badge.stale` — border-radius 20px

### 3.4 Tables

Toutes les tables partagent un pattern similaire mais avec des CSS dupliquees :

| Propriete | LocalCMS Light | Desk Pro Light | perf Dark | webhook Dark |
|-----------|---------------|----------------|-----------|-------------|
| width | 100% | 100% | 100% | 100% |
| border-collapse | collapse | collapse | separate | collapse |
| background | `#fff` | transparent | transparent | transparent |
| border | `1px solid #e6e6e6` | none | `1px solid #1e2733` | none |
| border-radius | 12px | 0 | 14px | 12px |
| overflow | hidden | none | hidden | hidden |
| th | `#fafafa`, uppercase 11px | border-bottom only | uppercase 9px | uppercase 11px |
| td padding | 10px 12px | 6px 6px | 10px 12px | 8px 12px |
| font-size | 13px | 13px | 12px | 13px |

### 3.5 Buttons / Links

**LocalCMS :**
- `.links-bar a` : padding 4px 10px, border 1px solid #ddd, border-radius 8px, font-size 12px
- `.nav-item` : styled as links in sidebar

**Desk Pro :**
- `button` : padding 10px 12px, border 1px solid #333, border-radius 10px, background #111, color #fff
- `.action-link` : padding 4px 10px, border 1px solid #ddd, border-radius 8px, font-size 12px
- `.action-btn` : similar to button, font-size 12px

**perf (Dark) :**
- Inline button styling, no dedicated class

### 3.6 Refresh patterns

Trois mecanismes distincts :
1. **`setTimeout(() => location.reload(), N)`** — LocalCMS (30s/60s), Desk Pro SpaceX (60s)
2. **`setInterval(refresh, N)` avec XHR** — webhook (2s), perf/ui (5s opt-in)
3. **`setInterval(load, N)` avec fetch JS** — `ui/spacex_desk/index.html` (60s)

### 3.7 Duplications identifiees

1. **CSS block `* { box-sizing: border-box; margin: 0; padding: 0; }`** — duplique dans TOUTES les pages LocalCMS (credentials, metrics, journal, journal_detail, main ui, spacex, signals)
2. **Sidebar CSS complete** — dupliquee 6 fois dans `localcms/app/main.py`
3. **`.badge`, `.badge-up`, `.badge-down`** — dupliques dans metrics, journal, journal_detail, main ui
4. **`.summary-card` CSS** — duplique dans credentials, metrics, journal, spacex, main ui
5. **`.links-bar` CSS** — duplique dans credentials, journal, spacex, main ui
6. **`table, th, td` CSS** — duplique dans credentials, metrics, journal, journal_detail, main ui
7. **SpaceX HTML** — 3 generateurs : `spacex_page.py`, `reports.py`, `reports/__init__.py` produisent des sorties similaires
8. **Badge functions** — `_pnl_badge()`, `_verdict_badge()`, `_closeout_badge()` sont isolees dans `localcms/app/main.py`, inaccessibles aux autres modules
9. **colors hex litterales** — `#f5f5f7`, `#1d1d1f`, `#e6e6e6`, `#333`, `#ccc`, `#ddd`, `#eee` repartis dans tout le code en dur

### 3.8 Risques

- **Espace de noms CSS pollue** : pas de scoping, conflits possibles entre pages
- **CSS inconsistante** : 17 blocs inline = 17 versions legerement differentes des memes regles
- **Maintenance penible** : modifier un badge necessite de toucher 5 fichiers
- **Redondance SpaceX** : modifier le layout SpaceX necessite de changer 3 fichiers + les routes live-served
- **Pas de fallback/garde** : si un bloc CSS est casse, l'impact est localise mais detecte tardivement

---

## 4. Design System Minimal (« OT-Core »)

### 4.1 Principes

- **Server-rendered only** — pas de JS framework, pas de build step
- **Compatible LocalCMS** — le design system herite du style Apple-light LocalCMS comme base canonique
- **CSS via constantes Python** — pas de fichier CSS separe, mais des constantes Python partageables dans `shared/`
- **Light par defaut, Dark optionnel** — les helpers produisent du Light; un parametre `theme="dark"` peut etre ajoute ultérieurement
- **Aucune dependance externe** — zero npm, zero CDN
- **Preservation du auto-refresh** existant

### 4.2 Composants definis

#### `shared/html_helpers.py`

```python
# Layout
def page_shell(title: str, content: str, *, sidebar: str = "", refresh_s: int = 0) -> str
def sidebar_nav(title: str, *, links: list[tuple[str, str, bool]]) -> str

# Cards
def card(content: str, *, accent: str = None) -> str
def summary_card(label: str, value: str, *, accent: str = None) -> str
def kpi_grid(cards: list[str]) -> str

# Badges
def badge(label: str, variant: str = "neutral") -> str  # up/down/neutral/minimal/critical/noncrit/info
def status_pill(label: str, variant: str = "neutral") -> str

# Tables
def table(headers: list[str], rows: list[list[str]], *, bordered: bool = True) -> str

# Sections
def section_title(title: str) -> str
def links_bar(links: list[tuple[str, str]]) -> str

# Refresh
def auto_refresh_script(seconds: int) -> str
def auto_refresh_xhr(interval_s: int, fetch_func: str, render_func: str) -> str
```

#### `shared/html_design_system.py`

```python
# CSS reset commun
CSS_RESET = "..."

# Couleurs
COLORS = {
    "bg": "#f5f5f7",
    "text": "#1d1d1f",
    "sidebar_bg": "#1d1d1f",
    "sidebar_text": "#f5f5f7",
    "card_bg": "#fff",
    "card_border": "#e6e6e6",
    # ... etc
}

# Classes standard
STANDARD_CSS = "..."  # tout le CSS partage

# Themes
LIGHT_CSS = "..."
DARK_CSS = "..."
```

### 4.3 Conventions de classes

| Classe | Usage | Herite de |
|--------|-------|-----------|
| `.layout` | Sidebar + main grid | LocalCMS existant |
| `.sidebar` | Nav column | LocalCMS existant |
| `.main` | Content area | LocalCMS existant |
| `.card` | Boite generique | LocalCMS existant |
| `.summary-card` | Carte KPI avec nombre | LocalCMS existant |
| `.badge` + `.badge-{variant}` | Status pill | LocalCMS existant |
| `.badge-up`, `.badge-down`, `.badge-neutral` | Semantique | Nouvelles, basees sur existant |
| `table` | Table standard | LocalCMS existant |
| `.links-bar` | Barre de liens | LocalCMS existant |
| `.notice` | Alert box | LocalCMS existant |
| `.section-title` | Titre de section | LocalCMS existant |

### 4.4 Usage

Avant (duplication) :
```python
# Chaque page LocalCMS duplique 40-60 lignes de CSS
return f"""<!DOCTYPE html>
<html><head>...<style>
  * {{ box-sizing: border-box; ... }}
  .layout {{ display: grid; grid-template-columns: 240px 1fr; ... }}
  .sidebar {{ background: #1d1d1f; ... }}
  .badge {{ display: inline-block; ... }}
  .badge-up {{ background: #d1fae5; ... }}
  ...40+ more lines...
</style></head>..."""
```

Apres (Batch C) :
```python
from shared.html_helpers import page_shell, badge, table, card, auto_refresh_script
from shared.html_design_system import STANDARD_CSS

content = card("Hello") + badge("OK", "up") + table(["A","B"], [["1","2"]])
return page_shell("Title", content, sidebar=my_sidebar, refresh_s=30, css=STANDARD_CSS)
```

---

## 5. Plan de refactor incremental

### Batch A — Helpers communs (IMMEDIAT, ce patch)
**Fichiers touches** : `shared/html_helpers.py` (nouveau), `shared/html_design_system.py` (nouveau), `docs/chantiers/GO_UI_GLOBAL_REFACTOR_LOCALCMS_01/` (documentation)
**Changements** : Ajout des helpers et constantes, zero modification de pages existantes
**Risques** : Aucun — nouveau code non importe par l'existant
**Tests** : `python3 -c "from shared.html_helpers import badge, card, table; print(badge('OK', 'up'))"`
**Rollback** : `rm shared/html_helpers.py shared/html_design_system.py`

### Batch B — Pages a faible risque (Credentials + Journal)
**Fichiers touches** : `modules/localcms/app/main.py` (pages credentials, journal, journal_detail)
**Changements** : Remplacer CSS inline par `STANDARD_CSS`, remplacer badges/utils par helpers partages. Sortie HTML identique visuellement.
**Risques** : Faible — pages a faible trafic, bien testees
**Tests** : `pytest tests/e2e/test_daily_session_journal_html.py -v`
**Rollback** : `git checkout modules/localcms/app/main.py`

### Batch C — Dashboards principaux (Central UI + Metrics + SpaceX)
**Fichiers touches** : `modules/localcms/app/main.py` (ui_index, metrics, spacex)
**Changements** : Utiliser helpers, remplacer CSS inline, reduire duplication
**Risques** : Moyen — pages a fort trafic, verifier layout identique
**Tests** : `pytest tests/ -k "desk_pro or localcms" -v`
**Rollback** : `git checkout modules/localcms/app/main.py`

### Batch D — Command centers + Desk Pro
**Fichiers touches** : `modules/desk_pro/ui/page.py`, `modules/desk_pro/api/routes.py`, `perf/perf_app.py`, `webhook_server.py`
**Changements** : Utiliser helpers, remplacer CSS inline
**Risques** : Eleve — cœur operationnel
**Tests** : Smoke complet `./scripts/smoke.sh`
**Rollback** : `git checkout` sur les fichiers concernes

### Batch E — Nettoyage duplication SpaceX
**Fichiers touches** : `modules/ipo_tracking/reports.py`, `modules/ipo_tracking/reports/__init__.py`, `modules/ipo_tracking/ui/spacex_page.py`
**Changements** : Fusionner les 3 generateurs en 1 canonique, supprimer les dupliques
**Risques** : Moyen — verifier que `write_static_page()` et `write_ui()` ne sont pas appeles par des scripts
**Tests** : `grep -rn "write_static_page\|write_ui\|render_static_page" --include="*.py" --include="*.sh" | grep -v __pycache__`
**Rollback** : Restaurer les 3 fichiers

### Batch F — Documentation + Tests
**Fichiers touches** : `docs/ARCHITECTURE.md`, ajout de `docs/UI_DESIGN_SYSTEM.md`, `tests/test_html_helpers.py`
**Changements** : Documenter le design system, ajouter tests unitaires pour chaque helper
**Risques** : Aucun
**Tests** : `pytest tests/test_html_helpers.py -v`

---

## 6. Premier patch minimal (Batch A) — Applique

### Fichiers crees

1. **`shared/html_helpers.py`** — Fonctions reutilisables pour generer du HTML
   - `badge(label, variant)` — pill semantique (up/down/neutral/minimal/critical/noncrit/info/impl/partial/to_build/closed/deprecated/cred_set/cred_absent/cred_future/cred_unknown)
   - `card(content, accent)` — conteneur card
   - `summary_card(label, value, accent)` — carte KPI
   - `table(headers, rows, bordered)` — table formatee
   - `section_title(title)` — titre de section
   - `links_bar(links)` — barre de liens
   - `auto_refresh_script(seconds)` — script JS auto-refresh
   - `page_shell(title, content, sidebar, refresh_s)` — shell page complete
   - `sidebar_nav(title, links)` — sidebar nav
   - `kpi_grid(cards)` — grille de summary_cards

2. **`shared/html_design_system.py`** — Constantes CSS partagees
   - `CSS_RESET` — box-sizing reset
   - `COLORS` — palette canonique
   - `LIGHT_CSS` — CSS standard Apple-light (sidebar, cards, badges, tables, links, notices)
   - `DARK_CSS` — theme sombre optionnel
   - `TABLE_CSS` — style table autonome
   - `BADGE_CSS` — tous les variants de badges
   - `CARD_CSS` — styles des cards

### Validation

```bash
python3 -c "from shared.html_helpers import *; print(badge('OK', 'up'))"
python3 -c "from shared.html_design_system import LIGHT_CSS; print(len(LIGHT_CSS))"
pytest tests/ -x -q 2>&1 | tail -5
```

### Non modifie

- Aucune page existante n'est modifiee
- Aucune route n'est touchee
- Aucun CSS existant n'est retire
- Les helpers sont strictement additifs

---

## 7. Commandes de test

```bash
# Syntax check
python3 -c "import shared.html_helpers; import shared.html_design_system; print('OK')"

# Tests existants
python3 -m pytest tests/ -x -q

# Verification routes HTML
grep -rn "response_class=HTMLResponse" --include="*.py" | grep -v __pycache__ | wc -l

# Smoke
./scripts/verify_all.sh
```

---

## 8. Checklist de validation manuelle

- [ ] `python3 -c "from shared.html_helpers import *"` passe sans erreur
- [ ] `python3 -c "from shared.html_design_system import *"` passe sans erreur
- [ ] Tous les tests existants passent (`pytest tests/ -q`)
- [ ] `./scripts/verify_all.sh` passe
- [ ] Aucune route HTML n'a disparu (`grep -c "response_class=HTMLResponse"`)
- [ ] Aucun fichier existant n'a ete modifie

---

## 9. Risques restants

| Risque | Probabilite | Impact | Mitigation |
|--------|------------|--------|------------|
| Regressions visuelles au Batch C | Moyenne | Moyen | Tests de regression visuelle existants (`test_ui_visual_regression_smoke.py`) |
| Conflit CSS entre helpers et inline existant | Faible | Faible | On n'active les helpers que progressivement, page par page |
| Performance (strings plus longs) | Negligeable | Negligeable | Python f-strings deja utilises partout, overhead identique |
| Breaking change sur badges (Batch B) | Faible | Eleve | Verifier exhaustivement que les classes CSS produites sont identiques avant merge |
| Perte de donnees affichees (Batch D, perf) | Faible | Critique | Comparer sortie HTML avant/apres pour chaque page touchee |

---

## 10. Prochaine etape recommandee

1. **REVIEW** ce document et les fichiers `shared/html_helpers.py` + `shared/html_design_system.py`
2. **APPROUVER** le Batch A pour merge dans `sot/mainline`
3. **PLANIFIER** le Batch B (Credentials + Journal) — le plus safe pour valider l'approche
4. **NE PAS** forcer les Batches C-F sans validation du Batch B en production
