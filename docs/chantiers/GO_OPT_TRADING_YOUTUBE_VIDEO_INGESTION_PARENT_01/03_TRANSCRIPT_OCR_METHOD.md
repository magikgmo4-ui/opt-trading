---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01_TRANSCRIPT_OCR_METHOD
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
doc_type: transcript_ocr_method
status: reference
created_at: 2026-06-06
surface: youtube_video_ingestion
---

# 03_TRANSCRIPT_OCR_METHOD

## Objectif

Capturer les deux couches d'information des vidéos trading courtes :

```text
audio parlé
+ texte / chiffres / annotations affichés à l'écran
```

Les Shorts trading peuvent contenir des données critiques uniquement visibles à l'écran : actif, entrée, SL, TP, timeframe, indicateurs, prix, flèches, annotations.

## Méthode transcription

Ordre de préférence :

```text
1. sous-titres manuels YouTube
2. sous-titres automatiques YouTube
3. Whisper / faster-whisper local
4. fallback manuel sur échantillon
```

## Commandes de base

Lister les vidéos :

```bash
yt-dlp --flat-playlist --dump-json "https://youtube.com/@trademachineoff/shorts" > outputs/youtube/raw_metadata/trademachineoff_index.jsonl
```

Télécharger audio et sous-titres :

```bash
yt-dlp \
  --write-subs \
  --write-auto-subs \
  --sub-lang "en,fr" \
  --sub-format "vtt/srt/best" \
  --extract-audio \
  --audio-format mp3 \
  -o "outputs/youtube/audio/%(id)s.%(ext)s" \
  "https://youtube.com/@trademachineoff/shorts"
```

Transcrire fallback :

```bash
whisper outputs/youtube/audio/*.mp3 \
  --model small \
  --output_dir outputs/youtube/transcripts
```

## Méthode OCR

Extraire frames :

```bash
ffmpeg -i input.mp4 -vf fps=1 outputs/youtube/frames/<video_id>/frame_%04d.jpg
```

OCR :

```text
Option simple: Tesseract
Option robuste: PaddleOCR
```

## Déduplication OCR

Les textes écran se répètent souvent sur plusieurs frames. Consolidation recommandée :

```text
frame_text
→ nettoyage espaces / symboles
→ similarité texte
→ suppression doublons
→ conservation timestamps
→ screen_text consolidé
```

## Audit attendu

```json
{
  "video_id": "string",
  "transcript_source": "manual_subs|auto_subs|whisper|missing",
  "ocr_engine": "tesseract|paddleocr|none",
  "frames_sampled": 0,
  "frames_with_text": 0,
  "audio_quality": "ok|poor|missing",
  "screen_text_quality": "ok|poor|missing",
  "warnings": []
}
```

## Règles

- Ne pas fusionner transcript et OCR avant le parser input.
- Garder les timestamps si disponibles.
- Marquer explicitement l'absence de sous-titres ou d'OCR.
- Ne pas inférer un prix ou une direction si le texte est illisible.

## Critère de réussite

Pour chaque vidéo pilote :

```text
spoken_transcript exploitable OU missing_reason
screen_text exploitable OU missing_reason
audit JSON généré
```