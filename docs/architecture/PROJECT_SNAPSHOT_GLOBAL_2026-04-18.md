## Classification  
**diagnostic ponctuel — reconstruction mémoire opérationnelle**

## Rôle recommandé  
**Architecte système + Auditeur de continuité (par défaut)**

---

# 1. Besoin initial
Reconstituer une **vue consolidée réelle** :
- projets / sous-projets  
- architecture infra  
- chantiers actifs + objectifs  

---

# 2. Cible finale
Un **snapshot exploitable** pour :
- reprendre n’importe quel GO  
- éviter dépendance à la session  
- réaligner repo / runtime / doc  

---

# 3. Vue d’ensemble — Projets & Sous-projets

## 3.1 Projet principal (canonique)

### `opt-trading` (repo central)
**Rôle :**
- production trading
- orchestration modules
- base documentaire canonique

**Sous-modules majeurs :**
- `risk_engine` → calcul risque (RiskCalculator extrait du webhook)
- `derivatives_collector` → collecte marchés dérivés (V3→V13)
- `derivatives_analyzer` → analyse + export structuré
- `probability_engine` → synthèse probabiliste trading
- `desk_pro_*` → dashboard / scanner / vision
- `bot_vision` → ingestion screenshots → analyse

---

## 3.2 Projet consommateur UI

### `localcms`
**Rôle :**
- consumer UI de opt-trading
- exploration mémoire + modules
- futur cockpit utilisateur

**Sous-chantiers :**
- Shared Explorer V1 (lecture `/shared`)
- CMS Installer V1 (pipeline install modules)
- Memory Bricks (lecture structuré mémoire)

---

## 3.3 Infrastructure IA / Dev

### Stack multi-agents
- Trae → IDE principal (DEV cockpit)
- OpenCode → exécution / scripting
- OpenClaw → orchestration / gateway IA
- Claude Code → dev assisté Windows
- ChatGPT → supervision / stratégie

---

## 3.4 Projet runtime distant

### Telegram + Vision pipeline
- ShareX (Windows capture)
- → Telegram bot
- → Linux ingestion
- → `desk_analyze`
- → snapshot JSON exploitable

---

# 4. Structure Infra (réelle)

## 4.1 Machines

| Machine        | Rôle |
|----------------|------|
| `admin-trading` | serveur Linux production (/opt/trading) |
| `student`       | expérimentation / ML |
| `db-layer`      | data / OpenClaw |
| `cursor-ai`     | poste Windows principal |

---

## 4.2 Architecture runtime

``` 
[Android / Remote]
        ↓
       SSH
        ↓
      tmux
        ↓
 ├─ OpenCode (exec)
 ├─ shell (tests)
 ├─ OpenClaw (agents)
        ↓
 Telegram (contrôle)
```

---

## 4.3 Flux critique trading

``` 
TradingView / Screenshots
        ↓
ShareX (Windows)
        ↓
Telegram
        ↓
bot_vision (Linux)
        ↓
ingestion → snapshots.json
        ↓
desk_analyze
        ↓
decision / logs / stats
```

---

# 5. Chantiers en cours (actifs)

## 5.1 Trading / Data pipeline

### derivatives_collector (V3 → V13)
**Objectif :**
- robustesse collecte multi-sources
- fail-open orchestration
- métriques `stats.unknown`

**État :**
- V12 → ajout unknown
- V13 → verrouillage sémantique + tests

---

### derivatives_analyzer
**Objectif :**
- transformer collecte → insights exploitables

---

### probability_engine
**Objectif :**
- centraliser décision probabiliste trading

---

## 5.2 Bot Vision (ingestion marché)

**Objectif :**
- transformer screenshots → données exploitables

**Points clés :**
- pipeline stable
- notion de STALE basée sur timestamp

---

## 5.3 Desk trading

### desk_pro
**Objectif :**
- cockpit trading (scanner + dashboard)

---

## 5.4 LocalCMS (UI & mémoire)

### Chantier M1.x (important)

#### Shared Explorer V1
- lecture `/shared`
- read-only sécurisé

#### CMS Installer V1
Pipeline :
``` 
Scan → Inspect → Precheck → Backup → Staging → Validate → Install → Post-check
```

#### Extraction modules config (M1.2)
- SYS_CFG → PASS
- NET_CFG → prochain GO
- BACKEND_CFG → non touché

---

## 5.5 Gouvernance & workflow

### Chantiers doc / structure

- GO_INDEX consolidation
- REPRISE standardisation
- hiérarchie parent / sous-chantier fixée
- règle :
  - plan → doc → repo → reprise

---

## 5.6 Infra runtime distant

### tmux + agents
**Objectif :**
- continuité session
- pilotage distant sans perte état

---

## 5.7 Cockpit dual

**Architecture validée :**

| Cockpit | Rôle |
|--------|------|
| Trae | DEV / repo / doc |
| OpenClaw | trading runtime / orchestration |

---

# 6. État établi (ETABLI)

- repo `opt-trading` aligné sur `sot/mainline`
- modules critiques fonctionnels (risk, collector, analyzer)
- pipeline vision opérationnel
- LocalCMS structuré (tests PASS)
- workflow canonique posé (GO / REPRISE / doc)

---

# 7. Gap restant

## Technique
- finaliser derivatives_collector V13
- enrichir probability_engine (données macro / news)
- stats trading persistantes (DB type timescale / clickhouse)

## UI
- migration UI opt-trading → localcms

## Runtime
- stabilisation cockpit OpenClaw
- gestion permissions / docker / services

## Trading
- validation empirique stratégies (FVG / open / squeeze)
- automatisation backtests + logging

---

# 8. Next GO probables

- GO_LOCALCMS_M1_2_NET_CFG_EXTRACT  
- GO_DERIVATIVES_COLLECTOR_V13_CLOSE  
- GO_PROBABILITY_ENGINE_ENRICHMENT  
- GO_TRADING_STATS_PIPELINE  
- GO_UI_MIGRATION_OPTT_LOCALCMS  

---

# 9. Synthèse

Ton système est structuré en 3 couches :

### 1. Production (opt-trading)
- collecte → analyse → décision

### 2. Runtime (infra + bots)
- ingestion → orchestration → exécution

### 3. Interface (localcms)
- visualisation → interaction → mémoire

Avec une séparation claire :
- repo = vérité
- runtime = exécution
- IA = assistance / orchestration

---

# 10. Clôture

## ETABLI
- architecture globale cohérente
- chantiers critiques identifiés
- séparation DEV / OPS / runtime validée

## TODO
- finaliser V13 collector
- enrichir probabiliste (macro/news)
- migrer UI vers localcms
- structurer stats trading persistantes

## REPRISE
Repartir via :
- `docs/index/REPRISE.md`
- GO_LOCALCMS_M1_2_NET_CFG_EXTRACT
- ou GO_TRADING_STATS_PIPELINE

## MEM_CANDIDATE
Vue consolidée projets / infra / chantiers utilisable comme snapshot de reprise global.