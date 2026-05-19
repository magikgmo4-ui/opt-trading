# FILE SPEC — MIMO OPEN OBSERVER V0

## app/config.py
Charger le YAML, valider le périmètre V0, exposer une config pure.

## app/models.py
Définir Bar, RawEvent, EnrichedEvent, helpers to_dict/from_dict.

## app/data_provider.py
Servir les bougies OHLC et les prix ponctuels via une interface unique.

## app/utils_time.py
Gérer timezone, jours actifs, fenêtres, offsets +30m / +60m.

## app/window_detector.py
Lire M1x5, détecter le premier FVG, calculer sweep, produire RawEvent.

## app/event_journal.py
Append-only raw + enriched, anti-doublons, lecture tail.

## app/outcome_sampler.py
Compléter +30m / +60m, delta, outcome.

## app/stats_builder.py
Lire enriched et sortir summary / by_direction / by_sweep / by_weekday.

## app/runner_detect.py
CLI detect_once / detect_range.

## app/runner_sample.py
CLI sample_pending.

## app/runner_stats.py
CLI build_stats / show_stats.
