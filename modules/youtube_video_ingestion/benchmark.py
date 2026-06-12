from __future__ import annotations

import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .vision import analyze_vision_layer_v1


BENCHMARK_RESULTS_FILENAME = "benchmark_results.json"
BENCHMARK_REPORT_FILENAME = "benchmark_report.md"
ANNOTATION_SCHEMA_VERSION = "vision_benchmark_annotations_v1"
RESULTS_SCHEMA_VERSION = "vision_benchmark_results_v1"


def write_vision_annotation_template(
    *,
    parser_input_dir: Path,
    output_path: Path,
    limit: int | None = None,
) -> dict[str, Any]:
    records = _load_parser_inputs(parser_input_dir, limit=limit)
    annotations = []
    for record in records:
        vision = _vision_for(record)
        annotations.append(
            {
                "video_id": record["video_id"],
                "expected": {
                    "symbols": [item["symbol"] for item in _list_of_dicts(vision.get("symbols_detected"))],
                    "prices": [
                        {"role": item["role"], "value": item["value"]}
                        for item in _list_of_dicts(vision.get("prices_detected"))
                    ],
                    "timeframes": [item["timeframe"] for item in _list_of_dicts(vision.get("timeframes_detected"))],
                    "indicators": [item["indicator"] for item in _list_of_dicts(vision.get("indicators_detected"))],
                    "chart_detected": bool(vision.get("chart_detected")),
                },
                "notes": "Review manually before using this annotation for benchmark scoring.",
            }
        )

    payload = {
        "schema_version": ANNOTATION_SCHEMA_VERSION,
        "generated_at": _now_z(),
        "parser_input_dir": str(parser_input_dir),
        "annotations": annotations,
    }
    _atomic_write_json(output_path, payload)
    return {
        "annotations_written": len(annotations),
        "annotation_template": str(output_path),
    }


def run_vision_benchmark(
    *,
    parser_input_dir: Path,
    annotations_path: Path,
    output_root: Path,
    limit: int | None = None,
    fixtures_output_dir: Path | None = None,
) -> dict[str, Any]:
    records = _load_parser_inputs(parser_input_dir, limit=limit)
    annotations = _load_annotations(annotations_path)
    annotated_by_id = {annotation["video_id"]: annotation for annotation in annotations}
    evaluated = [record for record in records if record["video_id"] in annotated_by_id]
    if not evaluated:
        raise ValueError("No parser_input records match the annotation video_id values")

    per_video = []
    aggregate = _empty_aggregate()
    chart_correct = 0
    for record in evaluated:
        annotation = annotated_by_id[record["video_id"]]
        expected = _expected(annotation)
        prediction = _prediction(_vision_for(record))
        metrics = {
            "symbols": _set_metrics(prediction["symbols"], expected["symbols"]),
            "prices": _set_metrics(prediction["prices"], expected["prices"]),
            "timeframes": _set_metrics(prediction["timeframes"], expected["timeframes"]),
            "indicators": _set_metrics(prediction["indicators"], expected["indicators"]),
        }
        for field, field_metrics in metrics.items():
            _add_metrics(aggregate[field], field_metrics)

        expected_chart = expected["chart_detected"]
        predicted_chart = prediction["chart_detected"]
        if predicted_chart == expected_chart:
            chart_correct += 1

        per_video.append(
            {
                "video_id": record["video_id"],
                "prediction": _json_prediction(prediction),
                "expected": _json_expected(expected),
                "metrics": metrics,
                "chart_detected_correct": predicted_chart == expected_chart,
                "vision_confidence": prediction["vision_confidence"],
            }
        )

    metrics_summary = {field: _finalize_metrics(values) for field, values in aggregate.items()}
    metrics_summary["chart_detected"] = {
        "correct": chart_correct,
        "total": len(evaluated),
        "accuracy": _safe_ratio(chart_correct, len(evaluated)),
    }

    output_root.mkdir(parents=True, exist_ok=True)
    result_path = output_root / BENCHMARK_RESULTS_FILENAME
    report_path = output_root / BENCHMARK_REPORT_FILENAME
    result = {
        "schema_version": RESULTS_SCHEMA_VERSION,
        "generated_at": _now_z(),
        "parser_input_dir": str(parser_input_dir),
        "annotations_path": str(annotations_path),
        "videos_evaluated": len(evaluated),
        "metrics": metrics_summary,
        "per_video": per_video,
        "artifacts": {
            "benchmark_results": str(result_path),
            "benchmark_report": str(report_path),
            "fixtures_real_world": str(fixtures_output_dir) if fixtures_output_dir else None,
        },
    }
    _atomic_write_json(result_path, result)
    _write_report(report_path, result)
    if fixtures_output_dir:
        _write_fixture_subset(fixtures_output_dir, evaluated, annotated_by_id)
    return result


def _load_parser_inputs(parser_input_dir: Path, *, limit: int | None) -> list[dict[str, Any]]:
    if not parser_input_dir.exists():
        raise FileNotFoundError(f"Parser input directory does not exist: {parser_input_dir}")
    records = []
    for path in sorted(parser_input_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"Parser input must be a JSON object: {path}")
        video_id = str(payload.get("video_id") or "").strip()
        if not video_id:
            raise ValueError(f"Parser input is missing video_id: {path}")
        records.append(payload)
        if limit is not None and len(records) >= limit:
            break
    if not records:
        raise ValueError(f"No parser_input JSON files found in {parser_input_dir}")
    return records


def _load_annotations(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        raw_annotations = payload.get("annotations")
    else:
        raw_annotations = payload
    if not isinstance(raw_annotations, list) or not raw_annotations:
        raise ValueError("Annotations must be a non-empty JSON array or an object with annotations[]")
    annotations = []
    for annotation in raw_annotations:
        if not isinstance(annotation, dict):
            raise ValueError("Each annotation must be a JSON object")
        video_id = str(annotation.get("video_id") or "").strip()
        if not video_id:
            raise ValueError("Each annotation must include video_id")
        annotations.append({"video_id": video_id, "expected": annotation.get("expected") or {}})
    return annotations


def _vision_for(record: dict[str, Any]) -> dict[str, Any]:
    vision = record.get("vision")
    if isinstance(vision, dict):
        return vision
    return analyze_vision_layer_v1(
        video_id=str(record.get("video_id") or ""),
        screen_text=str(record.get("screen_text") or ""),
        ocr_segments=record.get("ocr_segments") if isinstance(record.get("ocr_segments"), list) else [],
    )


def _prediction(vision: dict[str, Any]) -> dict[str, Any]:
    return {
        "symbols": {str(item["symbol"]) for item in _list_of_dicts(vision.get("symbols_detected")) if item.get("symbol")},
        "prices": {_price_key(item) for item in _list_of_dicts(vision.get("prices_detected")) if _price_key(item)},
        "timeframes": {
            str(item["timeframe"]) for item in _list_of_dicts(vision.get("timeframes_detected")) if item.get("timeframe")
        },
        "indicators": {
            str(item["indicator"]) for item in _list_of_dicts(vision.get("indicators_detected")) if item.get("indicator")
        },
        "chart_detected": bool(vision.get("chart_detected")),
        "vision_confidence": float(vision.get("confidence") or 0.0),
    }


def _expected(annotation: dict[str, Any]) -> dict[str, Any]:
    expected = annotation.get("expected") if isinstance(annotation.get("expected"), dict) else {}
    return {
        "symbols": {str(item) for item in _list_values(expected.get("symbols"))},
        "prices": {_price_key(item) for item in _list_of_dicts(expected.get("prices")) if _price_key(item)},
        "timeframes": {str(item) for item in _list_values(expected.get("timeframes"))},
        "indicators": {str(item) for item in _list_values(expected.get("indicators"))},
        "chart_detected": bool(expected.get("chart_detected")),
    }


def _set_metrics(predicted: set[Any], expected: set[Any]) -> dict[str, Any]:
    true_positive = len(predicted & expected)
    false_positive = len(predicted - expected)
    false_negative = len(expected - predicted)
    precision = _safe_ratio(true_positive, true_positive + false_positive)
    recall = _safe_ratio(true_positive, true_positive + false_negative)
    return {
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "predicted": len(predicted),
        "expected": len(expected),
        "precision": precision,
        "recall": recall,
        "f1": _f1(precision, recall),
        "exact_match": predicted == expected,
    }


def _empty_aggregate() -> dict[str, dict[str, int]]:
    return {
        field: {
            "true_positive": 0,
            "false_positive": 0,
            "false_negative": 0,
            "predicted": 0,
            "expected": 0,
            "exact_match": 0,
            "total": 0,
        }
        for field in ("symbols", "prices", "timeframes", "indicators")
    }


def _add_metrics(aggregate: dict[str, int], metrics: dict[str, Any]) -> None:
    for key in ("true_positive", "false_positive", "false_negative", "predicted", "expected"):
        aggregate[key] += int(metrics[key])
    aggregate["exact_match"] += int(bool(metrics["exact_match"]))
    aggregate["total"] += 1


def _finalize_metrics(values: dict[str, int]) -> dict[str, Any]:
    precision = _safe_ratio(values["true_positive"], values["true_positive"] + values["false_positive"])
    recall = _safe_ratio(values["true_positive"], values["true_positive"] + values["false_negative"])
    return {
        **values,
        "precision": precision,
        "recall": recall,
        "f1": _f1(precision, recall),
        "exact_match_rate": _safe_ratio(values["exact_match"], values["total"]),
    }


def _json_prediction(prediction: dict[str, Any]) -> dict[str, Any]:
    return {
        "symbols": sorted(prediction["symbols"]),
        "prices": _json_prices(prediction["prices"]),
        "timeframes": sorted(prediction["timeframes"]),
        "indicators": sorted(prediction["indicators"]),
        "chart_detected": prediction["chart_detected"],
    }


def _json_expected(expected: dict[str, Any]) -> dict[str, Any]:
    return {
        "symbols": sorted(expected["symbols"]),
        "prices": _json_prices(expected["prices"]),
        "timeframes": sorted(expected["timeframes"]),
        "indicators": sorted(expected["indicators"]),
        "chart_detected": expected["chart_detected"],
    }


def _json_prices(values: set[tuple[str, float]]) -> list[dict[str, Any]]:
    return [{"role": role, "value": value} for role, value in sorted(values)]


def _price_key(item: dict[str, Any]) -> tuple[str, float] | None:
    role = str(item.get("role") or "").strip()
    value = item.get("value")
    if not role or not isinstance(value, (int, float)):
        return None
    return role, round(float(value), 5)


def _list_values(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _list_of_dicts(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _safe_ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 1.0
    return round(numerator / denominator, 4)


def _f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return round(2 * precision * recall / (precision + recall), 4)


def _write_report(path: Path, result: dict[str, Any]) -> None:
    metrics = result["metrics"]
    lines = [
        "# Vision Benchmark Report",
        "",
        f"Generated: {result['generated_at']}",
        f"Parser input: `{result['parser_input_dir']}`",
        f"Annotations: `{result['annotations_path']}`",
        f"Videos evaluated: {result['videos_evaluated']}",
        "",
        "## Metrics",
        "",
        "| Field | Precision | Recall | F1 | Exact match |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for field in ("symbols", "prices", "timeframes", "indicators"):
        field_metrics = metrics[field]
        lines.append(
            f"| {field} | {field_metrics['precision']:.4f} | {field_metrics['recall']:.4f} | "
            f"{field_metrics['f1']:.4f} | {field_metrics['exact_match_rate']:.4f} |"
        )
    chart = metrics["chart_detected"]
    lines.extend(
        [
            "",
            f"Chart detected accuracy: {chart['accuracy']:.4f} ({chart['correct']}/{chart['total']})",
            "",
            "## Per Video",
            "",
            "| Video | Symbols | Prices | Timeframes | Indicators | Chart | Confidence |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in result["per_video"]:
        row_metrics = row["metrics"]
        lines.append(
            f"| `{row['video_id']}` | {_status(row_metrics['symbols'])} | {_status(row_metrics['prices'])} | "
            f"{_status(row_metrics['timeframes'])} | {_status(row_metrics['indicators'])} | "
            f"{'ok' if row['chart_detected_correct'] else 'miss'} | {row['vision_confidence']:.2f} |"
        )
    _write_text(path, "\n".join(lines) + "\n")


def _status(metrics: dict[str, Any]) -> str:
    return "ok" if metrics["exact_match"] else f"tp{metrics['true_positive']}/fp{metrics['false_positive']}/fn{metrics['false_negative']}"


def _write_fixture_subset(
    fixtures_output_dir: Path,
    records: list[dict[str, Any]],
    annotated_by_id: dict[str, dict[str, Any]],
) -> None:
    fixtures_output_dir.mkdir(parents=True, exist_ok=True)
    for record in records:
        payload = {
            "video_id": record["video_id"],
            "url": record.get("url"),
            "title": record.get("title"),
            "screen_text": record.get("screen_text"),
            "ocr_segments": record.get("ocr_segments") or [],
            "vision": _vision_for(record),
            "annotation": annotated_by_id[record["video_id"]],
        }
        _atomic_write_json(fixtures_output_dir / f"{record['video_id']}.json", payload)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as handle:
        handle.write(text)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def _atomic_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def _now_z() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
