---
doc_id: GO_DESKPRO_VOICE_OPERATOR_01_LOT_D_REALTIME
doc_type: implementation_report
repo: opt-trading
go_id: GO_DESKPRO_VOICE_OPERATOR_01
status: completed
created_at: 2026-06-15
lot: D
---

# 40_LOT_D_OPENAI_REALTIME

## Architecture

```text
Microphone (push-to-talk)
    │
    ▼
audio_io.record_audio()     → WAV bytes
    │
    ▼
openai_realtime_client.speech_to_text()   → texte fr
    │
    ▼
intent_router.route()       → RoutedIntent
    │
    ▼
read_api_client.call()      → /read/* endpoint
    │
    ▼
openai_realtime_client.text_to_speech()   → MP3 bytes
    │
    ▼
audio_io.play_audio()       → haut-parleur
```

## Fichiers

```text
modules/voice_operator/realtime/
  __init__.py
  openai_realtime_client.py   (131 lignes)  — Whisper STT + TTS API
  audio_io.py                  (211 lignes)  — record/play, push-to-talk
  voice_session.py             (190 lignes)  — orchestration

modules/voice_operator/cli/
  voice_operator_realtime.py   (98 lignes)   — CLI vocal
```

## Dependances

```bash
pip install sounddevice numpy    # audio capture/playback
pip install pydub                # MP3 playback (optionnel)
export OPENAI_API_KEY=sk-...      # requis pour STT + TTS
```

## Usage

```bash
# Interactive push-to-talk
python -m modules.voice_operator.cli.voice_operator_realtime

# Single text command
python -m modules.voice_operator.cli.voice_operator_realtime "Etat systeme"

# Text-mode only (pas de micro)
python -m modules.voice_operator.cli.voice_operator_realtime --text

# Lister peripheriques audio
python -m modules.voice_operator.cli.voice_operator_realtime --devices

# Choisir la voix
python -m modules.voice_operator.cli.voice_operator_realtime --voice nova

# Cout estime
python -m modules.voice_operator.cli.voice_operator_realtime --cost
```

## Flux d'une session

```
1. Appuyer sur ENTRÉE pour parler
2. Parler ("Etat systeme", "Setup BTC", etc.)
3. Appuyer sur ENTRÉE pour arreter l'enregistrement
4. Whisper transcrit
5. Intent router identifie l'intent
6. /read/* est appele
7. TTS synthetise la reponse
8. Audio joue dans le haut-parleur
```

## Fallback

- Sans `OPENAI_API_KEY` → texte uniquement (STT/TTS desactive)
- Sans `sounddevice` → texte uniquement (pas de micro/haut-parleur)
- La CLI fonctionne dans tous les cas en mode texte

## Cout estime

| Operation | Cout |
|-----------|------|
| Whisper STT | ~$0.006/min |
| TTS | ~$0.015/1K caracteres |
| Session typique | ~$0.001-0.003 |

~30 USD/mois pour usage regulier (~1000 sessions).

## Mode

- **Monitor-only** — affiche "MONITOR-ONLY" dans toutes les sorties
- **Validation humaine obligatoire** — rappele dans chaque reponse
- **Push-to-talk** — pas d'ecoute continue (privacy + cout)
- **Aucun ordre** — impossible de declencher un trade via la voix
