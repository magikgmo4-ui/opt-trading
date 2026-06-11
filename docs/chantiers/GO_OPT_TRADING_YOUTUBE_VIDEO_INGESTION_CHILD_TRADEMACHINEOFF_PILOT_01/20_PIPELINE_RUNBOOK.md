---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01_PIPELINE_RUNBOOK
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_CHILD_TRADEMACHINEOFF_PILOT_01
doc_type: pipeline_runbook
status: draft_reference
created_at: 2026-06-11
---

# 20_PIPELINE_RUNBOOK

## Principe

Le pilote doit prouver la chaine complete sur un echantillon borne. Le raw output
reste la source de verite; le parsed output est regenerable.

## Etapes

### 1. Registry

Creer ou mettre a jour `registry/youtube_sources.jsonl` avec une seule entree
`@trademachineoff` en `P0_PILOT`.

### 2. Candidate URLs

Lister 10 a 20 Shorts candidats. Le mode peut etre :

```text
latest
shorts_first
keyword
manual_seed
```

Chaque URL doit conserver :

```text
channel_handle
video_id
url
title
published_at si disponible
selection_reason
```

### 3. Raw metadata

Conserver un fichier par video :

```text
outputs/youtube/raw_metadata/<video_id>.json
```

Le fichier ne doit pas inventer les champs absents. Les champs manquants restent
`null`, `[]` ou `unknown` selon le contrat parent.

### 4. Transcript

Ordre de preference :

1. sous-titres manuels YouTube ;
2. sous-titres automatiques YouTube ;
3. transcription audio locale ;
4. fallback manuel pour fixture pilote.

La source de transcription doit etre conservee dans `subtitle_source`.

### 5. OCR

Extraire des frames de facon bornee, puis produire :

```text
outputs/youtube/ocr/<video_id>.jsonl
```

Chaque ligne doit contenir au minimum :

```json
{"video_id":"...","frame":"frame_000001.jpg","timestamp_sec":1,"text":"...","confidence":null}
```

### 6. Parser input

Consolider audio, OCR et metadata :

```text
outputs/youtube/parser_input/<video_id>.json
```

Champs attendus :

```text
video_id
url
title
description
spoken_transcript
screen_text
ocr_segments
subtitle_source
frame_sampling_rate
parser_profile
```

### 7. Parsed output

Produire une sortie derivee :

```text
outputs/youtube/parsed/<video_id>.json
```

Le parser ne doit jamais inventer `entry`, `stop_loss` ou `take_profits`.

## Commandes indicatives

Ces commandes sont indicatives et ne sont pas executees par ce patch :

```bash
yt-dlp --write-subs --write-auto-subs --sub-lang "en,fr" --skip-download "$VIDEO_URL"
ffmpeg -i input.mp4 -vf fps=1 outputs/youtube/frames/<video_id>/frame_%06d.jpg
tesseract frame_000001.jpg stdout
```

## Validation minimale

- Tous les JSON sont valides.
- Chaque `parser_input` reference son `video_id`.
- Chaque parsed output conserve `raw_evidence`.
- Les champs inconnus restent explicites.
- Les conflits audio/OCR sont notes au lieu d'etre resolus silencieusement.

