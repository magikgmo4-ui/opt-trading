#!/usr/bin/env python3
"""Read-only local LLM file audit worker.

This script reads files, sends their content to a local Ollama model, extracts
strict JSON, and writes one output JSON per audited file.

It never modifies source files, never commits, and never pushes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_INCLUDE_EXTENSIONS = {".md", ".txt", ".py", ".json", ".yaml", ".yml"}
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "tools/local_llm_worker/outputs",
}


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    return loaded or {}


def should_skip(path: Path, include_extensions: set[str], exclude_dirs: set[str]) -> bool:
    parts = set(path.parts)
    for excluded in exclude_dirs:
        excluded_parts = set(Path(excluded).parts)
        if excluded in str(path) or excluded_parts.issubset(parts):
            return True
    return path.suffix not in include_extensions


def iter_files(root: Path, include_extensions: set[str], exclude_dirs: set[str]) -> list[Path]:
    if root.is_file():
        return [] if should_skip(root, include_extensions, exclude_dirs) else [root]
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and not should_skip(path, include_extensions, exclude_dirs):
            files.append(path)
    return files


def stable_output_name(path: Path) -> str:
    digest = hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:16]
    safe_name = str(path).replace("/", "__").replace("\\", "__").replace(":", "")
    return f"{digest}__{safe_name}.json"


def chunk_by_sections(text: str, max_chars: int) -> list[str]:
    """Split text into chunks at section headers (lines starting with `## `),
    each chunk at most `max_chars` characters."""
    lines = text.splitlines(keepends=True)
    chunks: list[str] = []
    current: list[str] = []
    current_size = 0

    for line in lines:
        is_section_header = re.match(r"^#{1,3}\s", line) and not re.match(r"^#\s", line)
        # Always include the very first lines (preamble before any ##)
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
    """Return (full_text, chunks) where chunks is a list of text segments.
    If chunking is disabled or text fits in one chunk, returns a single chunk."""
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
        "established",
        "hypothesis",
        "remaining_gap",
        "todo",
        "risk",
        "duplicate_candidate",
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
    """Merge multiple chunk reports into a single file-level report."""
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


def write_error_report(output_path: Path, file_path: Path, error: Exception) -> None:
    report = {
        "file": str(file_path),
        "file_type": "unknown",
        "purpose": "Audit failed.",
        "established": [],
        "hypothesis": [],
        "remaining_gap": [f"Audit failed: {error}"],
        "todo": ["Review this file manually or rerun with a smaller input."],
        "risk": ["LLM output unavailable or invalid."],
        "duplicate_candidate": [],
        "patch_proposal": "",
        "confidence": 0,
    }
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="tools/local_llm_worker/config.yaml")
    parser.add_argument("--model", default=None)
    parser.add_argument("--root", default="docs")
    parser.add_argument("--max-files", type=int, default=None)
    args = parser.parse_args()

    config = load_config(Path(args.config))
    audit_config = config.get("audit", {})
    llm_config = config.get("llm", {})

    model = args.model or config.get("model")
    if not model:
        print("Missing model. Use --model <model> or set model in config.yaml.", file=sys.stderr)
        return 2

    max_files = args.max_files or int(audit_config.get("max_files", 5))
    max_chars = int(audit_config.get("max_chars_per_file", 12000))
    chunking_config = audit_config.get("chunking", {"enabled": False})
    timeout_seconds = int(llm_config.get("timeout_seconds", 120))
    include_extensions = set(audit_config.get("include_extensions", DEFAULT_INCLUDE_EXTENSIONS))
    exclude_dirs = set(audit_config.get("exclude_dirs", DEFAULT_EXCLUDE_DIRS))

    root = Path(args.root)
    output_dir = Path(config.get("output_dir", "tools/local_llm_worker/outputs")) / "file_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    prompt_path = Path("tools/local_llm_worker/prompts/file_audit_prompt.md")
    prompt_template = prompt_path.read_text(encoding="utf-8")

    files = iter_files(root, include_extensions, exclude_dirs)[:max_files]
    print(f"Auditing {len(files)} file(s) with model={model}")

    for file_path in files:
        output_path = output_dir / stable_output_name(file_path)
        full_text, chunks = read_text_chunked(file_path, max_chars, chunking_config)

        if len(chunks) == 1:
            prompt = build_prompt(prompt_template, file_path, chunks[0])
            try:
                raw = run_ollama(model, prompt, timeout_seconds)
                report = normalize_report(extract_json(raw), file_path)
                output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
                print(f"OK {file_path} -> {output_path}")
            except Exception as exc:
                write_error_report(output_path, file_path, exc)
                print(f"ERROR {file_path}: {exc}", file=sys.stderr)
        else:
            print(f"CHUNKING {file_path} -> {len(chunks)} chunks")
            chunk_reports: list[dict[str, Any]] = []
            all_ok = True
            for i, chunk in enumerate(chunks):
                prompt = build_prompt(prompt_template, file_path, chunk, chunk_index=i, total_chunks=len(chunks))
                try:
                    raw = run_ollama(model, prompt, timeout_seconds)
                    report = normalize_report(extract_json(raw), file_path)
                    chunk_reports.append(report)
                    print(f"  chunk {i+1}/{len(chunks)} OK")
                except Exception as exc:
                    chunk_reports.append(normalize_report({
                        "file": str(file_path),
                        "file_type": "",
                        "purpose": f"Chunk {i+1}/{len(chunks)} failed.",
                        "remaining_gap": [f"Chunk {i+1}/{len(chunks)} audit failed: {exc}"],
                        "todo": [f"Review chunk {i+1}/{len(chunks)} manually."],
                        "risk": ["LLM output unavailable or invalid for this section."],
                        "confidence": 0,
                    }, file_path))
                    print(f"  chunk {i+1}/{len(chunks)} ERROR: {exc}", file=sys.stderr)
                    all_ok = False

            merged = merge_chunk_reports(chunk_reports, file_path)
            output_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"{'OK' if all_ok else 'PARTIAL'} {file_path} -> {output_path} ({len(chunks)} chunks merged)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
