# What you get after /analyze

Artifacts per run:
  /opt/trading/data/desk_pro/vision/runs/<run_id>/
    charts/dashboard.jpg        (resized screenshot)
    charts/01..04.jpg           (optional quadrants if CROP_MODE=quad)
    analysis.txt / analysis.md  (OpenAI output)
    summary.json                (Desk Pro ingestion)
    vision.log.jsonl

Plus mirrored in vision_outbox:
  /srv/sftp/shared_files/shared/vision_outbox/analyze_<run_id>.txt
  /srv/sftp/shared_files/shared/vision_outbox/analyze_<run_id>.md
