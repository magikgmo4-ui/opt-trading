---
doc_id: GO_DESKPRO_VOICE_OPERATOR_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_DESKPRO_VOICE_OPERATOR_01
status: open
role: VOICE_INTERFACE_ARCHITECT
created_at: 2026-06-14
---

# GO_DESKPRO_VOICE_OPERATOR_01

## Objet

Construire un **Operateur Vocal Opt-Trading Monitor-Only** servant de couche d'interaction vocale au-dessus de l'ecosysteme deja existant : DeskPro, perf_app, webhook_server, LocalCMS, Watchlists, Telegram, OpenClaw (plus tard).

L'operateur vocal n'est **pas un moteur d'analyse**. C'est **une interface de consultation, navigation, synthese et lecture vocale**.

## 1_MASTER_TARGET

```text
Pouvoir parler au systeme :
  "Etat systeme"
  "Resume SPCX"
  "Alertes Telegram"
  "Rapport marche"
  "Analyse BTC"
  "Analyse Gold"
  "Setups actifs"
  "Score probabiliste"

et recevoir une reponse vocale.
```

Cout cible: ~30 USD/mois API (OpenAI Realtime).

## 7_CANONICAL_STATE

```text
Infrastructure existante:
  - DeskPro (setups, scores, probabilites, rapports)
  - perf_app :8010 (analytics API)
  - webhook_server :8000 (TV webhook)
  - LocalCMS :8700 (system cockpit)
  - Telegram (alertes, signaux)
  - Watchlists
  - OpenClaw (future integration)

Gaps:
  - Aucune couche vocale
  - Pas de contrat API unique pour consultation
  - Pas d'intent router vocal
  - Pas de synthèse audio
  - Pas d'inventaire des endpoints DeskPro exploitables
```

## 3_INITIAL_NEED

```text
Objectif initial :

Pouvoir parler au système :

"État système"
"Résumé SPCX"
"Alertes Telegram"
"Rapport marché"
"Analyse BTC"
"Analyse Gold"
"Setups actifs"
"Score probabiliste"

et recevoir une réponse vocale.

Avec un coût raisonnable (~30 USD/mois API).
```

## 4_MASTER_PROJECT_PLAN

Architecture finale :

```text
Sources de vérité
        │
        ▼

 ┌───────────────┐
 │    DeskPro    │
 └───────┬───────┘
         │

 ┌───────────────┐
 │   LocalCMS    │
 └───────┬───────┘
         │

 ┌───────────────┐
 │   Watchlists  │
 └───────┬───────┘
         │

 ┌───────────────┐
 │ Telegram/Data │
 └───────┬───────┘
         │

 ┌───────────────┐
 │ perf_app/API  │
 └───────┬───────┘
         │

         ▼

 ┌──────────────────────┐
 │ Voice Operator Layer │
 └──────────┬───────────┘
            │

     OpenAI Realtime

            │

      Voix utilisateur
```

## 6_FINAL_TARGET

```text
DESKPRO_VOICE_OPERATOR_V1

Un operateur vocal fonctionnel:
  - Lit les donnees DeskPro sans les calculer
  - Route les intents vocaux vers les bonnes sources
  - Synthetise des reponses audio en francais
  - Fonctionne sur cursor-ai (Windows) avec micro + audio output
  - Monitor-only, aucune execution de trade
```

## 8_VALIDATED_PLAN

### Roadmap

```text
Lot A — Audit DeskPro: cartographier setups, scores, rapports, alertes
Lot B — Contrat API: /read/setup, /read/score, /read/report, /read/alerts
Lot C — Voice Engine: menu vocal, intent router, response formatter
Lot D — OpenAI Realtime: connexion API, streaming audio, TTS/STT
Lot E — Tests: BTC, Gold, SPCX, Telegram, Watchlists
```

### Lot A — Audit DeskPro

Cartographier :

```text
Setups
Scores
Rapports
Alertes
System state
```

### Lot B — Contrat API

Créer :

```text
/read/setup
/read/score
/read/report
/read/alerts
/read/system
```

### Lot C — Voice Engine

Créer :

```text
Voice Menu (6 sections)
Intent Router
Response Formatter
```

### Lot D — OpenAI Realtime

Connecter :

```text
OpenAI Realtime API
WebSocket streaming
Audio input/output
```

### Lot E — Tests

Tests :

```text
BTC
Gold
SPCX
Telegram
Watchlists
Multi-symbol
```

## 9_SELECTED_SOLUTION

### Separation stricte des responsabilites

**DeskPro** — responsable de :

```text
collecte
fusion
validation
notation
scoring
setups
probabilites
risque
```

**Operateur vocal** — responsable de :

```text
lecture
navigation
resume
requetes vocales
synthese audio
```

### Menu vocal final

```text
SECTION 1 — Systeme:
  Etat systeme, Services actifs, Derniers runs,
  Erreurs critiques, Sante infrastructure

SECTION 2 — Marches:
  Rapport marche, Analyse BTC, Analyse Gold,
  Analyse ETH, Analyse SPCX,
  Analyse watchlist IA, Analyse watchlist spatial

SECTION 3 — Alertes:
  Alertes Telegram, Alertes TradingView,
  Alertes DeskPro, Alertes critiques

SECTION 4 — Setups:
  Setups actifs, Setup BTC, Setup Gold, Setup SPCX,
  Setups A+, Setups A, Setups invalides

SECTION 5 — Probabilites:
  Scores probabilistes, Top score,
  Top 5 opportunites, Risques eleves,
  Invalidations proches, TP/SL actifs

SECTION 6 — Rapports:
  Rapport quotidien, Rapport hebdomadaire,
  Rapport portefeuille, Rapport watchlist,
  Resume DeskPro
```

## 10_SELECTED_SETUP

```text
Phase 1 — cursor-ai (Windows):
  Micro, OpenAI Realtime, Voice Operator,
  REST APIs internes, Audio Output

Phase 2 — Connexion:
  DeskPro, LocalCMS, perf_app, Telegram, Watchlists

Phase 3 — Connexion:
  OpenClaw

Phase 4 — Mobile:
  Telephone, WebRTC, LiveKit (optionnel)
```

## 11_KEY_DECISIONS

- L'operateur vocal ne calcule pas les setups.
- L'operateur vocal ne calcule pas les scores probabilistes.
- DeskPro reste la source de verite.
- Aucune logique de trading dans l'operateur vocal.
- Lecture uniquement (read-only).
- Monitor-only — aucun ordre reel.
- Validation humaine obligatoire.
- La machine cible est cursor-ai (Windows) car c'est la seule avec micro + audio.

## 12_INVARIANTS

```text
Monitor-only.
Aucun ordre reel.
Aucun clic automatique.
Aucune execution de trade.
```

```text
L'operateur vocal ne calcule pas les setups.
```

```text
L'operateur vocal ne calcule pas les scores probabilistes.
```

```text
DeskPro reste la source de verite.
```

```text
Validation humaine obligatoire.
```

## 13_ESTABLISHED

Deja disponible :

```text
Infrastructure multi-machines
Telegram
perf_app
webhook_server
DeskPro
LocalCMS
Watchlists
OpenClaw (future integration)
```

## 14_HYPOTHESIS

A valider :

```text
Les endpoints DeskPro exposent deja tous les setups et scores.
```

Si non :

```text
Creer une couche API de lecture.
```

## 15_REMAINING_GAP

Il manque principalement :

```text
1. Inventaire des donnees DeskPro

2. Contrat API unique

3. Menu vocal

4. Prototype Realtime OpenAI

5. Liaison DeskPro ↔ Voice Operator
```

## 16_TODO

### Lot A — Audit DeskPro

Cartographier :

```text
Setups
Scores
Rapports
Alertes
System state
```

### Lot B — Contrat API

Créer :

```text
/read/setup
/read/score
/read/report
/read/alerts
/read/system
```

### Lot C — Voice Engine

Créer :

```text
Voice Menu (6 sections)
Intent Router
Response Formatter
```

### Lot D — OpenAI Realtime

Connecter :

```text
OpenAI Realtime API
WebSocket streaming
Audio input/output
TTS fallback (ElevenLabs/OpenAI TTS)
```

### Lot E — Tests

Tests :

```text
BTC
Gold
SPCX
Telegram
Watchlists
Multi-symbol
```

## 17_RESUME_POINT

```text
DeskPro = cerveau metier

Voice Operator = couche vocale

Aucune logique de trading dans l'operateur vocal

Lecture uniquement

Monitor-only

Validation humaine obligatoire
```

La prochaine etape logique est un **audit complet de DeskPro pour identifier precisement ou resident les setups, scores probabilistes, alertes et rapports afin de definir le contrat API unique que l'operateur vocal lira.**
