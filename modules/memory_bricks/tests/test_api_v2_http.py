from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.memory_bricks.app.api_v2_server import app


@pytest.fixture
def state_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    root = tmp_path / "memory_bricks_state"
    bricks_dir = root / "bricks"
    index_dir = root / "index"
    meta_dir = root / "meta"

    bricks_dir.mkdir(parents=True)
    index_dir.mkdir(parents=True)
    meta_dir.mkdir(parents=True)

    brick_one = """---
id: "MB-00001"
title: "Seed persisted source"
date: "2026-03-27T19:04:27-04:00"
timezone: "America/Montreal"
type: "resume_point"
status: "resumed"
ia: "chatgpt"
machine: "fantome"
surface: "terminal_linux"
project: "opt-trading"
module: "memory_bricks"
summary_short: "Persistent source seed for LocalCMS viewer validation."
resume_point: "Read the persisted source from the isolated fixture state."
links: []
tags:
  - "memory"
  - "viewer"
  - "seed"
repo: ""
branch: ""
path: ""
source_ref: []
canonical_ref: []
real_state_ref: []
validated_by: ""
decisions:
  - "Keep memory_bricks as source of truth"
todo:
  - "Validate the isolated HTTP fixture"
---

# MB-00001 - Seed persisted source

Fixture content for the read-only API tests.
"""
    brick_two = """---
id: "MB-00002"
title: "Viewer read-only contract"
date: "2026-03-27T19:04:27-04:00"
timezone: "America/Montreal"
type: "decision"
status: "open"
ia: "claude"
machine: "fantome"
surface: "terminal_linux"
project: "opt-trading"
module: "memory_bricks"
summary_short: "LocalCMS must read memory_bricks without writing back."
resume_point: "Consume index_full.json and brick markdown in read-only mode."
links:
  - "MB-00001"
tags:
  - "memory"
  - "viewer"
  - "contract"
repo: ""
branch: ""
path: ""
source_ref: []
canonical_ref: []
real_state_ref: []
validated_by: ""
decisions:
  - "LocalCMS reads index_full.json"
  - "LocalCMS detail reads MB markdown"
todo: []
---

# MB-00002 - Viewer read-only contract

LocalCMS must read memory_bricks without writing back.
"""

    (bricks_dir / "MB-00001__seed-persisted-source.md").write_text(brick_one, encoding="utf-8")
    (bricks_dir / "MB-00002__viewer-read-only-contract.md").write_text(brick_two, encoding="utf-8")

    index_full = [
        {
            "id": "MB-00001",
            "title": "Seed persisted source",
            "date": "2026-03-27T19:04:27-04:00",
            "timezone": "America/Montreal",
            "type": "resume_point",
            "status": "resumed",
            "ia": "chatgpt",
            "machine": "fantome",
            "surface": "terminal_linux",
            "project": "opt-trading",
            "module": "memory_bricks",
            "summary_short": "Persistent source seed for LocalCMS viewer validation.",
            "resume_point": "Read the persisted source from the isolated fixture state.",
            "links": [],
            "tags": ["memory", "viewer", "seed"],
            "repo": "",
            "branch": "",
            "path": "",
            "source_ref": [],
            "canonical_ref": [],
            "real_state_ref": [],
            "validated_by": "",
            "decisions": ["Keep memory_bricks as source of truth"],
            "todo": ["Validate the isolated HTTP fixture"],
        },
        {
            "id": "MB-00002",
            "title": "Viewer read-only contract",
            "date": "2026-03-27T19:04:27-04:00",
            "timezone": "America/Montreal",
            "type": "decision",
            "status": "open",
            "ia": "claude",
            "machine": "fantome",
            "surface": "terminal_linux",
            "project": "opt-trading",
            "module": "memory_bricks",
            "summary_short": "LocalCMS must read memory_bricks without writing back.",
            "resume_point": "Consume index_full.json and brick markdown in read-only mode.",
            "links": ["MB-00001"],
            "tags": ["memory", "viewer", "contract"],
            "repo": "",
            "branch": "",
            "path": "",
            "source_ref": [],
            "canonical_ref": [],
            "real_state_ref": [],
            "validated_by": "",
            "decisions": [
                "LocalCMS reads index_full.json",
                "LocalCMS detail reads MB markdown",
            ],
            "todo": [],
        },
    ]
    (index_dir / "index_full.json").write_text(json.dumps(index_full, indent=2), encoding="utf-8")
    (index_dir / "index_short.md").write_text(
        "# INDEX BRIQUES\n\n"
        "MB-00001 - 2026-03-27 - chatgpt - fantome - resumed - memory_bricks\n"
        "MB-00002 - 2026-03-27 - claude - fantome - open - memory_bricks\n",
        encoding="utf-8",
    )
    (meta_dir / "sequence.json").write_text(json.dumps({"last": 2}, indent=2), encoding="utf-8")

    monkeypatch.setenv("MEMORY_BRICKS_STATE_ROOT", str(root))
    return root


@pytest.fixture
def client(state_root: Path) -> TestClient:
    del state_root
    return TestClient(app)


def test_health_returns_200(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "module": "memory_bricks",
        "version": "0.1.0-readonly",
    }


def test_status_returns_coherent_indicators(client: TestClient, state_root: Path) -> None:
    response = client.get("/status")

    assert response.status_code == 200
    assert response.json() == {
        "root": str(state_root),
        "root_exists": True,
        "bricks_dir": True,
        "bricks": 2,
        "index_full": True,
        "index_short": True,
        "sequence": True,
    }


def test_bricks_returns_list_envelope(client: TestClient) -> None:
    response = client.get("/bricks")
    payload = response.json()

    assert response.status_code == 200
    assert payload["total"] == 2
    assert payload["limit"] == 50
    assert payload["offset"] == 0
    assert [item["id"] for item in payload["items"]] == ["MB-00001", "MB-00002"]


def test_brick_detail_returns_200_for_existing_brick(client: TestClient) -> None:
    response = client.get("/bricks/MB-00002")
    payload = response.json()

    assert response.status_code == 200
    assert payload["id"] == "MB-00002"
    assert payload["title"] == "Viewer read-only contract"
    assert payload["links"] == ["MB-00001"]
    assert "LocalCMS must read memory_bricks" in payload["content_markdown"]


def test_brick_detail_returns_stable_404_for_missing_brick(client: TestClient) -> None:
    response = client.get("/bricks/MB-99999")

    assert response.status_code == 404
    assert response.json() == {"error": "Brick not found"}


def test_find_returns_200_for_text_query(client: TestClient) -> None:
    response = client.get("/find", params={"text": "viewer"})
    payload = response.json()

    assert response.status_code == 200
    assert payload["total"] == 2
    assert payload["query"] == "viewer"
    assert [item["id"] for item in payload["items"]] == ["MB-00001", "MB-00002"]
    assert all("excerpt" in item for item in payload["items"])


def test_find_returns_stable_400_when_text_is_empty(client: TestClient) -> None:
    response = client.get("/find", params={"text": ""})

    assert response.status_code == 400
    assert response.json() == {"error": "Query text cannot be empty"}


def test_indexes_status_returns_200(client: TestClient, state_root: Path) -> None:
    response = client.get("/indexes/status")

    assert response.status_code == 200
    assert response.json() == {
        "index_dir": str(state_root / "index"),
        "index_dir_exists": True,
        "index_full_exists": True,
        "index_short_exists": True,
        "sequence_exists": True,
    }


def test_indexes_full_returns_json_from_index_full(client: TestClient) -> None:
    response = client.get("/indexes/full")
    payload = response.json()

    assert response.status_code == 200
    assert len(payload) == 2
    assert payload[0]["id"] == "MB-00001"
    assert payload[1]["id"] == "MB-00002"


def test_indexes_full_returns_stable_404_when_missing(client: TestClient, state_root: Path) -> None:
    (state_root / "index" / "index_full.json").unlink()

    response = client.get("/indexes/full")

    assert response.status_code == 404
    assert response.json() == {"error": "index_full.json not found"}


def test_indexes_short_returns_markdown_content(client: TestClient) -> None:
    response = client.get("/indexes/short")

    assert response.status_code == 200
    assert response.json() == {
        "content": "# INDEX BRIQUES\n\n"
        "MB-00001 - 2026-03-27 - chatgpt - fantome - resumed - memory_bricks\n"
        "MB-00002 - 2026-03-27 - claude - fantome - open - memory_bricks\n"
    }


def test_indexes_short_returns_stable_404_when_missing(client: TestClient, state_root: Path) -> None:
    (state_root / "index" / "index_short.md").unlink()

    response = client.get("/indexes/short")

    assert response.status_code == 404
    assert response.json() == {"error": "index_short.md not found"}


def test_indexes_sequence_returns_json_from_sequence_file(client: TestClient) -> None:
    response = client.get("/indexes/sequence")

    assert response.status_code == 200
    assert response.json() == {"last": 2}


def test_indexes_sequence_returns_stable_404_when_missing(client: TestClient, state_root: Path) -> None:
    (state_root / "meta" / "sequence.json").unlink()

    response = client.get("/indexes/sequence")

    assert response.status_code == 404
    assert response.json() == {"error": "sequence.json not found"}
