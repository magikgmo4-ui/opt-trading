# Current Parser Output Audit

## Scope

Audit des sorties de chaque parseur dans `modules/telegram_screener/parser/`.

---

## 1. Trade parser (`trade_parser.py`)

**Entree :** `raw_text: str`

**Sortie :** `ScreenerSignal | None`

**Champs peuples :**
- `source_channel` (propaged)
- `signal_type` = `SignalType.TRADE`
- `timestamp` (propaged ou now)
- `parsed_at` (now)
- `raw_text` (copie)
- `pair`, `direction`, `price`, `sl`, `tp`, `size`, `confidence`

**Champs vides :**
- `category` = None (non applicable pour trade)
- `metadata` = {} (vide)

**Analyse :**
- Produit deja un `ScreenerSignal` complet.
- Aucune transformation necessaire pour le pipeline existant.
- Pour le normalizer : peut etre passe tel quel ou reconverti en `SignalCandidate` puis reboucle.

---

## 2. News parser (`news_parser.py`)

**Entree :** `raw_text: str`

**Sortie :** `ScreenerSignal | None`

**Champs peuples :**
- `source_channel`, `signal_type` = `NEWS`, `timestamp`, `parsed_at`, `raw_text`, `category`, `confidence`

**Champs vides :**
- `pair`, `direction`, `price`, `sl`, `tp`, `size` = None

**Analyse :**
- Produit deja un `ScreenerSignal`.
- Pas d'information de trading (pair, direction, prix) → le normalizer doit marquer `parse_status` comme `PARTIAL` si transforme en `SignalCandidate`.

---

## 3. Alpha parser (`alpha_parser.py`)

**Entree :** `raw_text: str`

**Sortie :** `ScreenerSignal | None`

**Champs peuples :**
- `source_channel`, `signal_type` = `ALPHA`, `timestamp`, `parsed_at`, `raw_text`, `pair`, `confidence`, `metadata["message"]`

**Champs vides :**
- `direction`, `price`, `sl`, `tp`, `size`, `category` = None

**Analyse :**
- Produit deja un `ScreenerSignal`.
- Signal qualitatif sans direction ni prix → `parse_status` = `PARTIAL` en `SignalCandidate`.

---

## 4. Coinglass parser (`coinglass_parser.py`)

**Entree :** `RawMessage` (dataclass)

**Sortie :** `dict[str, Any] | None` (schema `telegram_trade_signal_candidate.v1`)

**Champs peuples dans le dict :**
- `schema`, `source_channel`, `message_timestamp`, `raw_text_ref`
- `asset`, `symbol`, `direction`, `entry`, `leverage`, `exchange_source`
- `confidence`, `parse_status`, `parse_errors`, `notional_usd`

**Champs systematiquement None :**
- `tp1`, `tp2`, `tp3`, `stop_loss`, `timeframe`

**Analyse :**
- **NE produit PAS** un `ScreenerSignal` (contrairement aux 3 autres parseurs).
- Sortie en dict brut, schema `telegram_trade_signal_candidate.v1`.
- C'est le principal moteur du besoin de normalisation : il faut un adaptateur `dict` -> `SignalCandidate` -> `ScreenerSignal`.

---

## Synthese

| Parser | Format sortie | Peut integrer pipeline directement |
|--------|--------------|-----------------------------------|
| trade  | `ScreenerSignal` | Oui |
| news   | `ScreenerSignal` | Oui |
| alpha  | `ScreenerSignal` | Oui |
| coinglass | `dict` | Non |

**Constats :**
1. `coinglass_parser.py` est le seul parseur qui ne s'integre pas directement.
2. Il faut un modele intermediaire (`SignalCandidate`) pour unifier les 4 formats.
3. Le normalizer doit accepter `SignalCandidate` ET le dict coinglass.
