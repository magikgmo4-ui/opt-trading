---
doc_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01_TRANSCRIPT_OCR_METHOD
go_id: GO_OPT_TRADING_YOUTUBE_VIDEO_INGESTION_PARENT_01
doc_type: transcript_ocr_method
status: draft_reference
created_at: 2026-06-06
---

# 03_TRANSCRIPT_OCR_METHOD

## Objectif

Définir la méthode d'extraction multimodale : audio + texte affiché.

Les Shorts trading contiennent souvent des signaux visuels absents de l'audio. La transcription seule est insuffisante.

## Transcription audio

Ordre de priorité :

1. sous-titres manuels YouTube ;
2. sous-titres automatiques YouTube ;
3. Whisper/faster-whisper local ;
4. fallback manuel sur échantillon.

Commande indicative :

```bash
yt-dlp --write-subs --write-auto-subs --sub-lang "en,fr" --skip-download "$VIDEO_URL"
```

Fallback audio :

```bash
yt-dlp --extract-audio --audio-format mp3 -o "outputs/youtube/audio/%(id)s.%(ext)s" "$VIDEO_URL"
whisper outputs/youtube/audio/<video_id>.mp3 --model small --output_dir outputs/youtube/transcripts
```

## OCR écran

Extraction de frames :

```bash
ffmpeg -i input.mp4 -vf fps=1 outputs/youtube/frames/<video_id>/frame_%06d.jpg
```

OCR simple :

```bash
tesseract frame_000001.jpg stdout
```

OCR robuste candidat : PaddleOCR.

## Déduplication OCR

Les textes écran se répètent souvent sur plusieurs frames.

Règles :

- normaliser whitespace ;
- supprimer lignes identiques consécutives ;
- grouper les textes similaires ;
- conserver une preuve frame/timestamp.

## Sortie OCR JSONL

```json
{"video_id":"...","frame":"frame_000001.jpg","timestamp_sec":1,"text":"BUY XAUUSD...","confidence":0.83}
```

## Limites

- OCR faible sur texte minuscule, compression, overlays rapides.
- Les valeurs numériques peuvent être mal reconnues.
- Les signaux doivent être validés par fixtures avant usage backtest.
