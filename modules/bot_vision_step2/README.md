# bot_vision_step2 v5 (admin-trading cerveau)

Goal (your spec):
- Every 10 minutes: send ONE resized screenshot to Telegram (cheap).
- On Telegram `/analyze`: analyze the 4 charts in that screenshot (OpenAI Vision),
  produce Desk Pro artifacts + analysis .txt/.md, and optionally "Send all" (4 cropped quadrants).

Notes:
- We do NOT assume "last 4 screenshots". We assume ONE dashboard screenshot that contains 4 charts.
- Mosaic is optional. We can crop quadrants (01..04) for Desk Pro / Send all.

## Family status
- `bot_vision_step2` is not treated as the single final survivor of the family
- current transitory operational chain is:
  - `vision_bot` for capture / inbox-outbox
  - `bot_vision_step2` for Telegram + Vision analysis + Desk Pro artifacts
- `bot_vision` remains the legacy `step1` skeleton
