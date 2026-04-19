from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


def now_z() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, payload: Any) -> None:
    ensure_directory(path.parent)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    ensure_directory(path.parent)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")


class KilStorage:
    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root
        self.jsonl_dir = workspace_root / "jsonl"
        self.sqlite_dir = workspace_root / "sqlite"
        self.exports_dir = workspace_root / "exports"
        self.db_path = self.sqlite_dir / "kil_v1.db"
        ensure_directory(self.workspace_root)
        ensure_directory(self.jsonl_dir)
        ensure_directory(self.sqlite_dir)
        ensure_directory(self.exports_dir)

    def initialize(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS campaigns (
                    id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS topics (
                    id TEXT PRIMARY KEY,
                    campaign_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS framings (
                    id TEXT PRIMARY KEY,
                    campaign_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS question_sets (
                    id TEXT PRIMARY KEY,
                    campaign_id TEXT NOT NULL,
                    version TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,
                    campaign_id TEXT NOT NULL,
                    question_set_id TEXT NOT NULL,
                    target_label TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS responses (
                    id TEXT PRIMARY KEY,
                    campaign_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    response_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS evaluations (
                    id TEXT PRIMARY KEY,
                    campaign_id TEXT NOT NULL,
                    response_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    total_score INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS comparisons (
                    id TEXT PRIMARY KEY,
                    campaign_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS capitalizations (
                    id TEXT PRIMARY KEY,
                    campaign_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    granted_level TEXT NOT NULL,
                    promoted_memory_brick_id TEXT,
                    memory_sync_status TEXT,
                    memory_sync_at TEXT,
                    memory_sync_error TEXT,
                    created_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS journal_events (
                    id TEXT PRIMARY KEY,
                    campaign_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    object_type TEXT NOT NULL,
                    object_id TEXT NOT NULL,
                    from_status TEXT,
                    to_status TEXT,
                    actor_role TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS exports (
                    id TEXT PRIMARY KEY,
                    campaign_id TEXT NOT NULL,
                    export_type TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    generated_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS policies (
                    id TEXT PRIMARY KEY,
                    campaign_id TEXT NOT NULL,
                    policy_type TEXT NOT NULL,
                    version TEXT NOT NULL,
                    active_flag INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
                CREATE INDEX IF NOT EXISTS idx_responses_hash ON responses(response_hash);
                CREATE INDEX IF NOT EXISTS idx_journal_campaign ON journal_events(campaign_id);
                """
            )

    def insert_record(self, table: str, record: dict[str, Any]) -> None:
        payload = dict(record)
        payload_json = json.dumps(payload, ensure_ascii=True)
        if table == "campaigns":
            values = (record["id"], record["status"], record["title"], record["created_at"], record["updated_at"], payload_json)
            sql = "INSERT OR REPLACE INTO campaigns (id, status, title, created_at, updated_at, payload_json) VALUES (?, ?, ?, ?, ?, ?)"
        elif table == "topics":
            values = (record["topic_id"], record["campaign_id"], record["title"], record["created_at"], payload_json)
            sql = "INSERT OR REPLACE INTO topics (id, campaign_id, title, created_at, payload_json) VALUES (?, ?, ?, ?, ?)"
        elif table == "framings":
            values = (record["framing_id"], record["campaign_id"], record["framing_status"], record["created_at"], payload_json)
            sql = "INSERT OR REPLACE INTO framings (id, campaign_id, status, created_at, payload_json) VALUES (?, ?, ?, ?, ?)"
        elif table == "question_sets":
            values = (record["question_set_id"], record["campaign_id"], record["question_version"], record["created_at"], payload_json)
            sql = "INSERT OR REPLACE INTO question_sets (id, campaign_id, version, created_at, payload_json) VALUES (?, ?, ?, ?, ?)"
        elif table == "runs":
            values = (record["run_id"], record["campaign_id"], record["question_set_id"], record["target_label"], record["run_status"], record["started_at"], payload_json)
            sql = "INSERT OR REPLACE INTO runs (id, campaign_id, question_set_id, target_label, status, created_at, payload_json) VALUES (?, ?, ?, ?, ?, ?, ?)"
        elif table == "responses":
            values = (record["response_id"], record["campaign_id"], record["run_id"], record["response_status"], record["response_hash"], record["captured_at"], payload_json)
            sql = "INSERT OR REPLACE INTO responses (id, campaign_id, run_id, status, response_hash, created_at, payload_json) VALUES (?, ?, ?, ?, ?, ?, ?)"
        elif table == "evaluations":
            values = (record["evaluation_id"], record["campaign_id"], record["response_id"], record["evaluation_status"], record["evaluator_verdict"], record["total_score"], record["evaluated_at"], payload_json)
            sql = "INSERT OR REPLACE INTO evaluations (id, campaign_id, response_id, status, verdict, total_score, created_at, payload_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        elif table == "comparisons":
            values = (record["comparison_id"], record["campaign_id"], record["comparison_status"], record["compared_at"], payload_json)
            sql = "INSERT OR REPLACE INTO comparisons (id, campaign_id, status, created_at, payload_json) VALUES (?, ?, ?, ?, ?)"
        elif table == "capitalizations":
            values = (
                record["capitalization_id"],
                record["campaign_id"],
                record["promotion_status"],
                record["granted_level"],
                record.get("promoted_memory_brick_id"),
                record.get("memory_sync_status"),
                record.get("memory_sync_at"),
                record.get("memory_sync_error"),
                record["created_at"],
                payload_json,
            )
            sql = "INSERT OR REPLACE INTO capitalizations (id, campaign_id, status, granted_level, promoted_memory_brick_id, memory_sync_status, memory_sync_at, memory_sync_error, created_at, payload_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        elif table == "journal_events":
            values = (record["event_id"], record["campaign_id"], record["event_type"], record["object_type"], record["object_id"], record.get("from_status"), record.get("to_status"), record["actor_role"], record["timestamp"], payload_json)
            sql = "INSERT OR REPLACE INTO journal_events (id, campaign_id, event_type, object_type, object_id, from_status, to_status, actor_role, timestamp, payload_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        elif table == "exports":
            values = (record["export_id"], record["campaign_id"], record["export_type"], record["file_path"], record["generated_at"], payload_json)
            sql = "INSERT OR REPLACE INTO exports (id, campaign_id, export_type, file_path, generated_at, payload_json) VALUES (?, ?, ?, ?, ?, ?)"
        elif table == "policies":
            values = (record["policy_id"], record["campaign_id"], record["policy_type"], record["policy_version"], 1 if record.get("active_flag", True) else 0, record["created_at"], payload_json)
            sql = "INSERT OR REPLACE INTO policies (id, campaign_id, policy_type, version, active_flag, created_at, payload_json) VALUES (?, ?, ?, ?, ?, ?, ?)"
        else:
            raise ValueError(f"Unsupported table: {table}")

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(sql, values)
            conn.commit()

    def append_stream(self, stream_name: str, record: dict[str, Any]) -> None:
        append_jsonl(self.jsonl_dir / f"{stream_name}.jsonl", record)

    def response_hash_exists(self, response_hash: str, exclude_campaign_id: str | None = None) -> bool:
        query = "SELECT 1 FROM responses WHERE response_hash = ?"
        values: list[Any] = [response_hash]
        if exclude_campaign_id:
            query += " AND campaign_id != ?"
            values.append(exclude_campaign_id)
        query += " LIMIT 1"
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(query, tuple(values)).fetchone()
        return row is not None

    def count_journal_events(self, campaign_id: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT COUNT(*) FROM journal_events WHERE campaign_id = ?", (campaign_id,)).fetchone()
        return int(row[0]) if row else 0
