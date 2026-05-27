#!/usr/bin/env python3
"""Continuous local LLM file audit scanner.

Reads files from one or more root directories, sends each to the local model,
logs results, and auto-aggregates at the end. Designed to run without manual
supervision on a bounded scope.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import logging
import re
import subprocess
import sys
import time
from pathlib import Path
from statistics import mean
from typing import Any


DEFAULT_INCLUDE_EXTENSIONS = {".md", ".txt", ".py", ".json", ".yaml", ".yml"}
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "tools/local_llm_worker/outputs",
    "tools/local_llm_worker/logs",
}

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    return loaded or {}


def should_skip(path: Path, include_extensions: set[str], exclude_dirs: set[str], exclude_files: set[str] | None = None) -> bool:
    if exclude_files and path.name in exclude_files:
        return True
    parts = set(path.parts)
    for excluded in exclude_dirs:
        if excluded in str(path):
            return True
        excluded_parts = set(Path(excluded).parts)
        if excluded_parts.issubset(parts):
            return True
    return path.suffix not in include_extensions


def iter_files(root: Path, include_extensions: set[str], exclude_dirs: set[str], exclude_files: set[str] | None = None) -> list[Path]:
    if root.is_file():
        return [] if should_skip(root, include_extensions, exclude_dirs, exclude_files) else [root]
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and not should_skip(path, include_extensions, exclude_dirs, exclude_files):
            files.append(path)
    return files


def stable_output_name(path: Path) -> str:
    digest = hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:16]
    safe_name = str(path).replace("/", "__").replace("\\", "__").replace(":", "")
    return f"{digest}__{safe_name}.json"


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

def chunk_by_sections(text: str, max_chars: int) -> list[str]:
    lines = text.splitlines(keepends=True)
    chunks: list[str] = []
    current: list[str] = []
    current_size = 0
    for line in lines:
        is_section_header = re.match(r"^#{1,3}\s", line) and not re.match(r"^#\s", line)
        line_len = len(line)
        if is_section_header and current_size + line_len > max_chars and current:
            chunks.append("".join(current))
            current = [line]
            current_size = line_len
        else:
            current.append(line)
            current_size += line_len
    if current:
        chunks.append("".join(current))
    return chunks or [text]


def read_text_chunked(path: Path, max_chars: int, chunking_config: dict[str, Any]) -> tuple[str, list[str]]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return f"[READ_ERROR] {exc}", [f"[READ_ERROR] {exc}"]
    chunking_enabled = chunking_config.get("enabled", False)
    chunk_max_chars = int(chunking_config.get("max_chars_per_chunk", max_chars))
    if not chunking_enabled or len(text) <= chunk_max_chars:
        return text, [text[:max_chars] + "\n\n[TRUNCATED]" if len(text) > max_chars else text]
    raw_chunks = chunk_by_sections(text, chunk_max_chars)
    limited_chunks: list[str] = []
    for c in raw_chunks:
        if len(c) > max_chars:
            limited_chunks.append(c[:max_chars] + "\n\n[TRUNCATED]")
        else:
            limited_chunks.append(c)
    return text, limited_chunks


def build_prompt(prompt_template: str, file_path: Path, content: str, chunk_index: int | None = None, total_chunks: int | None = None) -> str:
    section_info = ""
    if chunk_index is not None and total_chunks and total_chunks > 1:
        section_info = f"\n(SECTION {chunk_index + 1} OF {total_chunks} — analyse uniquement cette section)\n"
    return (
        prompt_template
        + "\n\n---\n"
        + f"FILE_PATH:\n{file_path}\n\n"
        + section_info
        + "FILE_CONTENT:\n"
        + content
        + "\n\nReturn strict JSON only."
    )


def run_ollama(model: str, prompt: str, timeout_seconds: int) -> str:
    proc = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout_seconds,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"ollama exited with {proc.returncode}")
    return proc.stdout.strip()


def extract_json(raw: str) -> dict[str, Any]:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:].strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start >= 0 and end > start:
            return json.loads(raw[start : end + 1])
        raise


def normalize_report(report: dict[str, Any], file_path: Path) -> dict[str, Any]:
    defaults: dict[str, Any] = {
        "file": str(file_path),
        "file_type": "",
        "purpose": "",
        "established": [],
        "hypothesis": [],
        "remaining_gap": [],
        "todo": [],
        "risk": [],
        "duplicate_candidate": [],
        "patch_proposal": "",
        "confidence": 0,
    }
    normalized = defaults | report
    normalized["file"] = str(file_path)
    for key in [
        "established", "hypothesis", "remaining_gap",
        "todo", "risk", "duplicate_candidate",
    ]:
        value = normalized.get(key)
        if not isinstance(value, list):
            normalized[key] = [str(value)] if value else []
        else:
            normalized[key] = [str(item) for item in value[:7]]
    try:
        normalized["confidence"] = max(0, min(100, int(normalized.get("confidence", 0))))
    except (TypeError, ValueError):
        normalized["confidence"] = 0
    return normalized


def merge_chunk_reports(reports: list[dict[str, Any]], file_path: Path) -> dict[str, Any]:
    if not reports:
        return normalize_report({}, file_path)
    if len(reports) == 1:
        return reports[0]
    merged: dict[str, Any] = {
        "file": str(file_path),
        "file_type": reports[0].get("file_type", ""),
        "purpose": reports[0].get("purpose", ""),
        "established": [],
        "hypothesis": [],
        "remaining_gap": [],
        "todo": [],
        "risk": [],
        "duplicate_candidate": [],
        "patch_proposal": "",
        "confidence": 0,
    }
    list_keys = ["established", "hypothesis", "remaining_gap", "todo", "risk", "duplicate_candidate"]
    total_confidence = 0
    for r in reports:
        for key in list_keys:
            merged[key].extend(r.get(key, []))
        if r.get("patch_proposal"):
            merged["patch_proposal"] += (merged["patch_proposal"] and " | ") + r["patch_proposal"]
        total_confidence += int(r.get("confidence", 0))
    merged["confidence"] = round(total_confidence / len(reports))
    for key in list_keys:
        seen: set[str] = set()
        deduped: list[str] = []
        for item in merged[key]:
            if item not in seen:
                seen.add(item)
                deduped.append(item)
        merged[key] = deduped[:7]
    return normalize_report(merged, file_path)


def merge_two_pass(report1: dict[str, Any], report2: dict[str, Any], file_path: Path) -> dict[str, Any]:
    """Merge two passes: keep the BETTER result (higher confidence).
    If both have similar confidence (within 15pts), merge via union + bonus."""
    list_keys = ["established", "hypothesis", "remaining_gap", "todo", "risk", "duplicate_candidate"]

    conf1 = int(report1.get("confidence", 0))
    conf2 = int(report2.get("confidence", 0))

    if abs(conf1 - conf2) > 15:
        best = report1 if conf1 > conf2 else report2
        best["file"] = str(file_path)
        return normalize_report(best, file_path)

    merged: dict[str, Any] = {
        "file": str(file_path),
        "file_type": report1.get("file_type") or report2.get("file_type", ""),
        "purpose": report1.get("purpose") or report2.get("purpose", ""),
        "patch_proposal": report1.get("patch_proposal") or report2.get("patch_proposal", ""),
    }

    for key in list_keys:
        seen: set[str] = set()
        merged[key] = []
        for item in list(report1.get(key, [])) + list(report2.get(key, [])):
            if item not in seen:
                seen.add(item)
                merged[key].append(item)
        merged[key] = merged[key][:5]

    merged["confidence"] = min(100, max(conf1, conf2) + 10)
    return normalize_report(merged, file_path)


def write_error_report(file_path: Path) -> dict[str, Any]:
    return {
        "file": str(file_path),
        "file_type": "unknown",
        "purpose": "Audit failed.",
        "established": [],
        "hypothesis": [],
        "remaining_gap": ["Audit failed: LLM output unavailable or invalid."],
        "todo": ["Review this file manually or rerun with a smaller input."],
        "risk": ["LLM output unavailable or invalid."],
        "duplicate_candidate": [],
        "patch_proposal": "",
        "confidence": 0,
    }


# ---------------------------------------------------------------------------
# Agregation
# ---------------------------------------------------------------------------

def collect_items(reports: list[dict[str, Any]], key: str) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    for report in reports:
        source = str(report.get("file", "UNKNOWN"))
        for item in report.get(key, []) or []:
            if isinstance(item, str) and item.strip():
                items.append((source, item.strip()))
    return items


def render_section(title: str, items: list[tuple[str, str]], limit: int | None = None) -> str:
    if not items:
        return f"## {title}\n\n- Aucun élément.\n"
    selected = items if limit is None else items[:limit]
    lines = [f"## {title}", ""]
    for source, item in selected:
        lines.append(f"- `{source}` — {item}")
    return "\n".join(lines) + "\n"


def render_report(reports: list[dict[str, Any]]) -> str:
    confidences = [
        int(report.get("confidence", 0))
        for report in reports
        if isinstance(report.get("confidence", 0), int)
    ]
    avg_confidence = round(mean(confidences), 2) if confidences else 0
    lines = [
        "# Student Local LLM Audit Report",
        "",
        "## SUMMARY",
        "",
        f"- Files audited: {len(reports)}",
        f"- Average confidence: {avg_confidence}",
        "",
    ]
    lines.append(render_section("13_ESTABLISHED", collect_items(reports, "established")))
    lines.append(render_section("14_HYPOTHESIS", collect_items(reports, "hypothesis")))
    lines.append(render_section("15_REMAINING_GAP", collect_items(reports, "remaining_gap")))
    lines.append(render_section("16_TODO", collect_items(reports, "todo")))
    lines.append(render_section("RISKS", collect_items(reports, "risk")))
    lines.append(render_section("DUPLICATE_CANDIDATES", collect_items(reports, "duplicate_candidate")))
    patch_items = [
        (str(report.get("file", "UNKNOWN")), str(report.get("patch_proposal", "")).strip())
        for report in reports
        if str(report.get("patch_proposal", "")).strip()
    ]
    lines.append(render_section("PATCH_PROPOSALS", patch_items))
    lines.extend([
        "## 17_RESUME_POINT",
        "",
        "```text",
        "review report → validate hallucination rate → decide extension or stop",
        "```",
        "",
    ])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Continuous local LLM audit scanner — silent, logged, auto-aggregated."
    )
    parser.add_argument("--config", default="tools/local_llm_worker/config.yaml")
    parser.add_argument("--model", default=None)
    parser.add_argument("--roots", nargs="+", default=["docs"],
                        help="One or more root directories to scan")
    parser.add_argument("--max-files", type=int, default=None,
                        help="Limit total files scanned across all roots")
    parser.add_argument("--incremental", action="store_true",
                        help="Skip files that already have an output JSON")
    parser.add_argument("--silent", action="store_true",
                        help="Suppress all stdout output (log only)")
    parser.add_argument("--passes", type=int, default=None, choices=[1, 2],
                        help="Number of independent passes per file (2 = consensus merge)")
    args = parser.parse_args()

    # Load config
    config = load_config(Path(args.config))
    audit_config = config.get("audit", {})
    llm_config = config.get("llm", {})

    model = args.model or config.get("model")
    if not model:
        print("Missing model. Use --model <model> or set model in config.yaml.", file=sys.stderr)
        return 2

    max_chars = int(audit_config.get("max_chars_per_file", 12000))
    chunking_config = audit_config.get("chunking", {"enabled": False})
    timeout_seconds = int(llm_config.get("timeout_seconds", 120))
    include_extensions = set(audit_config.get("include_extensions", DEFAULT_INCLUDE_EXTENSIONS))
    exclude_dirs = set(audit_config.get("exclude_dirs", DEFAULT_EXCLUDE_DIRS))
    exclude_files = set(audit_config.get("exclude_files", []))
    passes = args.passes if args.passes is not None else int(llm_config.get("passes", 1))

    # Setup dirs
    output_dir = Path(config.get("output_dir", "tools/local_llm_worker/outputs"))
    file_analysis_dir = output_dir / "file_analysis"
    logs_dir = output_dir / "logs"
    reports_dir = output_dir / "reports"
    file_analysis_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Run ID
    run_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = logs_dir / f"scan_{run_id}.log"

    # Setup logging
    logger = logging.getLogger("continuous_scan")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(str(log_path), encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(fh)

    if not args.silent:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(ch)

    # Load prompt
    prompt_path = Path("tools/local_llm_worker/prompts/file_audit_prompt.md")
    prompt_template = prompt_path.read_text(encoding="utf-8")

    # Collect files
    all_files: list[Path] = []
    for root_str in args.roots:
        root = Path(root_str)
        if not root.exists():
            logger.warning("Root does not exist, skipping: %s", root)
            continue
        found = iter_files(root, include_extensions, exclude_dirs, exclude_files)
        logger.info("Root %s: %d files found", root, len(found))
        all_files.extend(found)

    all_files = sorted(set(all_files))

    # De-duplicate / sort by size (small first for progressive confidence building)
    all_files.sort(key=lambda p: p.stat().st_size)

    if args.max_files and len(all_files) > args.max_files:
        logger.info("Limiting to %d files (of %d)", args.max_files, len(all_files))
        all_files = all_files[:args.max_files]

    if not all_files:
        logger.warning("No files to scan.")
        return 0

    # Scan
    logger.info("=" * 60)
    logger.info("CONTINUOUS SCAN  run_id=%s  model=%s  roots=%s  passes=%d",
                run_id, model, " ".join(args.roots), passes)
    logger.info("Files to scan: %d  chunking=%s  timeout=%ds",
                len(all_files), chunking_config.get("enabled", False), timeout_seconds)
    logger.info("=" * 60)

    SECOND_PASS_SUFFIX = (
        "\n\n## SECOND PASS\n\nSeconde analyse indépendante du même fichier. "
        "Applique les mêmes règles que la première analyse."
    )

    def audit_content(fp: Path, pass_label: str, content: str, chunk_index: int | None = None, total_chunks: int | None = None) -> dict[str, Any]:
        pt = prompt_template
        if pass_label == "pass2":
            pt += SECOND_PASS_SUFFIX
        prompt = build_prompt(pt, fp, content, chunk_index, total_chunks)
        raw = run_ollama(model, prompt, timeout_seconds)
        return normalize_report(extract_json(raw), fp)

    start_time = time.time()
    ok_count = 0
    error_count = 0
    total_chunks_processed = 0

    for idx, file_path in enumerate(all_files, 1):
        output_path = file_analysis_dir / stable_output_name(file_path)

        if args.incremental and output_path.exists():
            logger.info("[%3d/%d] SKIP (exists) %s", idx, len(all_files), file_path)
            continue

        _, chunks = read_text_chunked(file_path, max_chars, chunking_config)

        try:
            t0 = time.time()

            if len(chunks) == 1:
                report1 = audit_content(file_path, "pass1", chunks[0])
                elapsed1 = time.time() - t0
                total_chunks_processed += 1

                report = report1
                log_flags = f"{elapsed1:.1f}s  conf={report1.get('confidence', 0)}"

                if passes == 2 and report1.get("confidence", 0) < 50:
                    report2 = audit_content(file_path, "pass2", chunks[0])
                    elapsed2 = time.time() - t0
                    total_chunks_processed += 1
                    report = merge_two_pass(report1, report2, file_path)
                    log_flags = f"{elapsed1:.1f}s+{elapsed2 - elapsed1:.1f}s  2pass  conf={report.get('confidence', 0)}"
            else:
                chunk_reports1: list[dict[str, Any]] = []
                for ci, chunk in enumerate(chunks):
                    cr = audit_content(file_path, "pass1", chunk, chunk_index=ci, total_chunks=len(chunks))
                    chunk_reports1.append(cr)
                    total_chunks_processed += 1
                report1 = merge_chunk_reports(chunk_reports1, file_path)

                report = report1
                elapsed_total = time.time() - t0
                log_flags = f"{elapsed_total:.1f}s  {len(chunks)} chunks  conf={report.get('confidence', 0)}"

                if passes == 2 and report1.get("confidence", 0) < 50:
                    chunk_reports2: list[dict[str, Any]] = []
                    for ci, chunk in enumerate(chunks):
                        cr = audit_content(file_path, "pass2", chunk, chunk_index=ci, total_chunks=len(chunks))
                        chunk_reports2.append(cr)
                        total_chunks_processed += 1
                    report2 = merge_chunk_reports(chunk_reports2, file_path)
                    report = merge_two_pass(report1, report2, file_path)
                    elapsed_total = time.time() - t0
                    log_flags = f"{elapsed_total:.1f}s  {len(chunks)} chunks  2pass  conf={report.get('confidence', 0)}"

            output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            ok_count += 1
            logger.info("[%3d/%d] OK %s  (%s)", idx, len(all_files), file_path, log_flags)

        except Exception as exc:
            error_count += 1
            report = write_error_report(file_path)
            output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            logger.error("[%3d/%d] ERROR %s  (%s)", idx, len(all_files), file_path, exc)

    elapsed_total = time.time() - start_time
    logger.info("=" * 60)
    logger.info("SCAN COMPLETE  run_id=%s", run_id)
    logger.info("  Files: %d OK, %d errors, %d total", ok_count, error_count, len(all_files))
    logger.info("  Chunks processed: %d", total_chunks_processed)
    logger.info("  Elapsed: %.1f seconds (%.1f min)", elapsed_total, elapsed_total / 60)
    logger.info("=" * 60)

    # Auto-aggregate
    reports: list[dict[str, Any]] = []
    for f in sorted(file_analysis_dir.glob("*.json")):
        try:
            reports.append(json.loads(f.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            pass

    if reports:
        report_md = render_report(reports)
        report_path = reports_dir / f"scan_{run_id}_report.md"
        report_path.write_text(report_md, encoding="utf-8")
        logger.info("Aggregated report: %s", report_path)
        logger.info("  Files in report: %d", len(reports))
        confidences = [r.get("confidence", 0) for r in reports if isinstance(r.get("confidence", 0), int)]
        avg_conf = round(mean(confidences), 1) if confidences else 0
        logger.info("  Average confidence: %s", avg_conf)
    else:
        logger.warning("No valid reports to aggregate.")

    logger.info("Log: %s", log_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
