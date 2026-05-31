# 20_CAPTURE_CONTRACT

## Objectif

Definir le contrat de capture pour rendre les screenshots reproductibles et
utilisables par la couche d'analyse.

## Points a valider

- viewport
- frequence
- sections
- full-page vs crop
- multi-capture
- reproductibilite
- fichiers 0-byte / `.uploading` interdits

## Contrat de capture actuel observe dans le repo

Le runtime `capture_headless.js` impose deja :

- viewport par defaut `1920x1080`
- `screenshot_mode = viewport`
- status de capture : `ready`, `blocked`, `invalid_visual`
- visual status : `pass`, `possible_spinner`, `blank_or_uniform`,
  `too_small`, `loading_state_detected`, `unchecked`
- garde-fou taille mini : `MIN_FILE_SIZE = 1024`
- write atomique `.uploading -> final`
- sidecar JSON avec :
  - `producer`
  - `capture_mode`
  - `page_id`
  - `source`
  - `symbol`
  - `timeframe`
  - `url`
  - `status`
  - `visual_status`
  - `wait_until`
  - `timeout_ms`
  - `post_load_wait_ms`
  - `screenshot_mode`
  - `viewport`
  - `created_at_utc`
  - `output_png`
  - `output_json`

## Sources P1 a cadrer en priorite

### TradingView charts

Sources deja observees dans les profils :

- `BTCUSDT.P` / H1
- `BINANCE:BTCUSDT` / H1
- `BINANCE:BTCUSDTPERP` / H1
- `BYBIT:BTCUSDT.P` / H1
- `OANDA:XAUUSD` / H1

Parametres deja utilises :

- `page_id`
- `source = tradingview`
- `wait_until = domcontentloaded` ou `load`
- `post_load_wait_ms = 5000` a `15000`
- `timeout_ms = 45000` a `60000`
- `screenshot_mode = viewport`
- `visual_check_enabled = true`

Contrat recommande P1 TradingView :

| Champ | Regle recommandee |
|---|---|
| `page_id` | obligatoire, stable par strategie de capture |
| `source` | `tradingview` |
| `symbol` | obligatoire |
| `timeframe` | obligatoire |
| `url` | obligatoire, version canonique de la page |
| `wait_until` | `domcontentloaded` par defaut, `load` si page lourde |
| `post_load_wait_ms` | >= 10000 si overlays/scripts tardifs |
| `timeout_ms` | 45000-60000 |
| `visual_check_enabled` | `true` |

### Coinglass pages

Sources deja observees dans les profils :

- `LiquidationData?coin=BTC`
- `FundingRate/BITCOIN`

Contrat recommande P1 Coinglass :

| Champ | Regle recommandee |
|---|---|
| `page_id` | obligatoire |
| `source` | `coinglass` |
| `symbol` | obligatoire |
| `timeframe` | valeur logique de board (`FLOW` observe) |
| `url` | URL canonique board/page |
| `wait_until` | `domcontentloaded` |
| `post_load_wait_ms` | >= 15000 pour stabiliser widgets |
| `timeout_ms` | 60000 |
| `visual_check_enabled` | `true` |

## Matrice de validation capture P1

| Source | Validation minimale | Echec bloquant |
|---|---|---|
| TradingView chart | screenshot lisible, timeframe visible, chart principal present | blank, spinner, chart absent, image trop petite |
| Coinglass board | captures widgets attendus, texte exploitable, board coherente | page chargee partiellement, anti-bot, widgets manquants |

## Decision full-page vs crop

- etat actuel observe : `viewport` uniquement
- recommandation P1 : conserver `viewport` comme base canonique tant qu'aucun
  mapping par zones n'est fige
- extension P2 : autoriser `crop` ou `multi-capture` par source quand une page
  contient plusieurs sections utiles non lisibles dans un viewport unique

## Frequence recommandee

- baseline existante : timer 10 min sur le runtime historique
- P1 : conserver une frequence moderee compatible avec screenshots stables
- a documenter par source si certaines pages ont une cinetique plus lente ou plus rapide

## Preuves attendues

- captures identiques sur runs comparables
- zones d'interet conformes au mapping source
- sortie exploitable par OCR / vision sans retraitement manuel
- sidecar JSON coherent avec les metadonnees de capture
- aucun fichier 0-byte, aucun `.uploading` stale residuel
