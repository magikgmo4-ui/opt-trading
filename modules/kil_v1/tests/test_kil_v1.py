from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
import importlib
from pathlib import Path
from typing import Any, cast
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "modules" / "kil_v1" / "src"))

PolicyError = importlib.import_module("kil_v1.errors").PolicyError
ValidationError = importlib.import_module("kil_v1.errors").ValidationError
audit_campaign_integrity = importlib.import_module("kil_v1.service").audit_campaign_integrity
run_campaign = importlib.import_module("kil_v1.service").run_campaign
service_module = importlib.import_module("kil_v1.service")


class KilV1Tests(unittest.TestCase):
    def test_sample_flow_runs_end_to_end_and_closes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_sample_spec()
            cli_path = self._build_fake_memory_bricks_cli(Path(temp_dir))
            with patch.dict(os.environ, {"KIL_V1_MEMORY_BRICKS_CMD": str(cli_path)}, clear=False):
                result = run_campaign(spec, Path(temp_dir))

            self.assertEqual(result["final_status"], "CLOSED")
            self.assertEqual(result["granted_promotion_level"], "STRICT")
            self.assertEqual(result["memory_sync_status"], "SYNCED")
            self.assertTrue(str(result["promoted_memory_brick_id"]).startswith("MB-"))
            self.assertTrue((Path(temp_dir) / "sqlite" / "kil_v1.db").exists())
            self.assertTrue((Path(temp_dir) / "exports" / result["campaign_id"] / "campaign_summary.md").exists())

    def test_truth_claims_do_not_get_strict_promotion(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_sample_spec()
            spec["responses"] = [
                {
                    "target_label": "candidate_truthy",
                    "surface": "fixture",
                    "machine": "student",
                    "operator": "tester",
                    "response_text": "This definitely is proven and guaranteed to be correct forever.",
                    "source_citations": [],
                    "external_validation": False,
                }
            ]
            result = run_campaign(spec, Path(temp_dir))
            report = (Path(temp_dir) / "exports" / result["campaign_id"] / "evaluation_report.md").read_text(encoding="utf-8")

            self.assertEqual(result["granted_promotion_level"], "LAB")
            self.assertIn("definitely", report)

    def test_duplicate_accumulation_blocks_standard_promotion(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_sample_spec()
            cli_path = self._build_fake_memory_bricks_cli(Path(temp_dir))
            with patch.dict(os.environ, {"KIL_V1_MEMORY_BRICKS_CMD": str(cli_path)}, clear=False):
                first = run_campaign(spec, Path(temp_dir))
                second = run_campaign(spec, Path(temp_dir))
            cap_report = (Path(temp_dir) / "exports" / second["campaign_id"] / "capitalization_candidate.md").read_text(encoding="utf-8")

            self.assertEqual(first["granted_promotion_level"], "STRICT")
            self.assertEqual(second["granted_promotion_level"], "LAB")
            self.assertIn("duplicate_response_detected", cap_report)

    def test_non_standardized_prompt_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_sample_spec()
            question = cast(dict[str, Any], spec["question"])
            del question["prompt_template_id"]
            with self.assertRaises(ValidationError):
                run_campaign(spec, Path(temp_dir))

    def test_missing_policy_blocks_campaign(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_sample_spec()
            policies = cast(dict[str, Any], spec["policies"])
            del policies["evaluation"]
            with self.assertRaises(PolicyError):
                run_campaign(spec, Path(temp_dir))

    def test_bias_evaluator_prefers_evidence_over_rhetoric(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_sample_spec()
            cli_path = self._build_fake_memory_bricks_cli(Path(temp_dir))
            with patch.dict(os.environ, {"KIL_V1_MEMORY_BRICKS_CMD": str(cli_path)}, clear=False):
                result = run_campaign(spec, Path(temp_dir))
            report = (Path(temp_dir) / "exports" / result["campaign_id"] / "evaluation_report.md").read_text(encoding="utf-8")

            self.assertIsNotNone(result["comparison_winner"])
            self.assertIn("rhetoric_outweighs_evidence", report)

    def test_lab_only_content_does_not_pollute_standard(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_sample_spec()
            capitalization = cast(dict[str, Any], spec["capitalization"])
            capitalization["target_level"] = "STANDARD"
            spec["responses"] = [
                {
                    "target_label": "candidate_lab",
                    "surface": "fixture",
                    "machine": "student",
                    "operator": "tester",
                    "response_text": "A possible idea is to maybe do something useful later.",
                    "source_citations": [],
                    "external_validation": False,
                }
            ]
            result = run_campaign(spec, Path(temp_dir))

            self.assertEqual(result["granted_promotion_level"], "LAB")

    def test_integrity_audit_detects_missing_journal(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_sample_spec()
            cli_path = self._build_fake_memory_bricks_cli(Path(temp_dir))
            with patch.dict(os.environ, {"KIL_V1_MEMORY_BRICKS_CMD": str(cli_path)}, clear=False):
                result = run_campaign(spec, Path(temp_dir))
            journal_path = Path(temp_dir) / "jsonl" / "journal.jsonl"
            journal_path.unlink()

            audit = audit_campaign_integrity(Path(temp_dir), result["campaign_id"])
            self.assertFalse(audit["ok"])
            self.assertTrue(any("journal.jsonl" in issue for issue in audit["issues"]))

    def test_invalid_comparison_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_sample_spec()
            responses = cast(list[dict[str, Any]], spec["responses"])
            responses[1]["question_text_override"] = "A different question entirely"
            with self.assertRaises(ValidationError):
                run_campaign(spec, Path(temp_dir))

    def test_sync_failure_keeps_promotion_decision(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_sample_spec()
            with patch.dict(os.environ, {"KIL_V1_MEMORY_BRICKS_CMD": "/bin/false"}, clear=False):
                result = run_campaign(spec, Path(temp_dir))
            cap_report = (Path(temp_dir) / "exports" / result["campaign_id"] / "capitalization_candidate.md").read_text(encoding="utf-8")

            self.assertEqual(result["granted_promotion_level"], "STRICT")
            self.assertEqual(result["memory_sync_status"], "SYNC_FAILED")
            self.assertIn("Memory sync status: SYNC_FAILED", cap_report)

    def test_ollama_provider_success_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_provider_spec()
            cli_path = self._build_fake_memory_bricks_cli(Path(temp_dir))
            with patch.object(
                service_module,
                "call_ollama_provider",
                return_value={
                    "response_text": "A grounded answer with enough detail to be evaluated safely.",
                    "source_citations": [],
                    "external_validation": False,
                    "provider_label": "ollama",
                    "provider_model": "deepseek-r1:1.5b",
                    "provider_request_id": "req-1",
                    "provider_finish_reason": "stop",
                    "provider_timeout_seconds": 30,
                    "provider_error": None,
                    "captured_at": "2026-04-02T00:00:00Z",
                },
            ), patch.dict(os.environ, {"KIL_V1_MEMORY_BRICKS_CMD": str(cli_path)}, clear=False):
                result = run_campaign(spec, Path(temp_dir))

            responses_stream = (Path(temp_dir) / "jsonl" / "responses.jsonl").read_text(encoding="utf-8")
            self.assertEqual(result["final_status"], "CLOSED")
            self.assertIn('"provider_label": "ollama"', responses_stream)
            self.assertIn('"provider_model": "deepseek-r1:1.5b"', responses_stream)

    def test_ollama_provider_timeout_blocks_before_evaluation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_provider_spec()
            with patch.object(service_module, "call_ollama_provider", side_effect=ValidationError("ollama_timeout")):
                with self.assertRaises(ValidationError):
                    run_campaign(spec, Path(temp_dir))
            journal = (Path(temp_dir) / "jsonl" / "journal.jsonl").read_text(encoding="utf-8")
            self.assertIn("response_unusable", journal)
            self.assertNotIn("response_evaluated", journal)

    def test_ollama_provider_model_absent_blocks_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_provider_spec()
            with patch.object(service_module, "call_ollama_provider", side_effect=ValidationError("ollama_http_error: 404 model not found")):
                with self.assertRaises(ValidationError):
                    run_campaign(spec, Path(temp_dir))
            responses_stream = (Path(temp_dir) / "jsonl" / "responses.jsonl").read_text(encoding="utf-8")
            self.assertIn('"provider_error": "ollama_http_error: 404 model not found"', responses_stream)

    def test_ollama_provider_empty_response_blocks_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_provider_spec()
            with patch.object(service_module, "call_ollama_provider", side_effect=ValidationError("ollama_empty_response")):
                with self.assertRaises(ValidationError):
                    run_campaign(spec, Path(temp_dir))
            responses_stream = (Path(temp_dir) / "jsonl" / "responses.jsonl").read_text(encoding="utf-8")
            self.assertIn('"response_status": "INVALID_FORMAT"', responses_stream)

    def test_provider_response_is_not_treated_as_established_truth(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_provider_spec()
            cli_path = self._build_fake_memory_bricks_cli(Path(temp_dir))
            with patch.object(
                service_module,
                "call_ollama_provider",
                return_value={
                    "response_text": "This answer is structured and plausible but not externally validated yet.",
                    "source_citations": [],
                    "external_validation": False,
                    "provider_label": "ollama",
                    "provider_model": "deepseek-r1:1.5b",
                    "provider_request_id": None,
                    "provider_finish_reason": "stop",
                    "provider_timeout_seconds": 30,
                    "provider_error": None,
                    "captured_at": "2026-04-02T00:00:00Z",
                },
            ), patch.dict(os.environ, {"KIL_V1_MEMORY_BRICKS_CMD": str(cli_path)}, clear=False):
                result = run_campaign(spec, Path(temp_dir))

            self.assertEqual(result["granted_promotion_level"], "LAB")
            evaluations_stream = (Path(temp_dir) / "jsonl" / "evaluations.jsonl").read_text(encoding="utf-8")
            self.assertIn('"certainty_level": "HYPOTHESE"', evaluations_stream)

    def test_no_local_memory_brick_is_written_by_kil(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            spec = self._load_sample_spec()
            cli_path = self._build_fake_memory_bricks_cli(Path(temp_dir))
            with patch.dict(os.environ, {"KIL_V1_MEMORY_BRICKS_CMD": str(cli_path)}, clear=False):
                run_campaign(spec, Path(temp_dir))

            self.assertFalse((Path(temp_dir) / "memory_bricks").exists())

    def _load_sample_spec(self) -> dict[str, Any]:
        path = REPO_ROOT / "modules" / "kil_v1" / "examples" / "sample_campaign.json"
        return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))

    def _load_provider_spec(self) -> dict[str, Any]:
        spec = self._load_sample_spec()
        spec["responses"] = [
            {
                "target_label": "ollama_candidate",
                "surface": "ollama_local",
                "machine": "student",
                "operator": "system",
                "provider": {
                    "type": "ollama",
                    "model": "deepseek-r1:1.5b",
                    "timeout_seconds": 30,
                },
            }
        ]
        comparison = cast(dict[str, Any], spec["comparison"])
        comparison["enabled"] = False
        capitalization = cast(dict[str, Any], spec["capitalization"])
        capitalization["target_level"] = "STRICT"
        return spec

    def _build_fake_memory_bricks_cli(self, root: Path) -> Path:
        script_path = root / "fake_memory_bricks_cli.py"
        state_dir = root / "fake_memory_bricks_state"
        script_path.write_text(
            "#!/usr/bin/env python3\n"
            "import json\n"
            "import sys\n"
            "from pathlib import Path\n"
            "\n"
            f"STATE_DIR = Path({str(state_dir)!r})\n"
            "STATE_DIR.mkdir(parents=True, exist_ok=True)\n"
            "SEQ_PATH = STATE_DIR / 'seq.txt'\n"
            "LINKS_PATH = STATE_DIR / 'links.jsonl'\n"
            "INDEX_PATH = STATE_DIR / 'index_rebuild.log'\n"
            "args = sys.argv[1:]\n"
            "if args[:2] == ['new', '--payload-file']:\n"
            "    payload = json.loads(Path(args[2]).read_text(encoding='utf-8'))\n"
            "    seq = int(SEQ_PATH.read_text(encoding='utf-8')) if SEQ_PATH.exists() else 0\n"
            "    seq += 1\n"
            "    SEQ_PATH.write_text(str(seq), encoding='utf-8')\n"
            "    brick_id = f'MB-{seq:05d}'\n"
            "    Path(STATE_DIR / f'{brick_id}.json').write_text(json.dumps(payload), encoding='utf-8')\n"
            "    print(json.dumps({'id': brick_id, 'status': 'created'}))\n"
            "elif args[:2] == ['link', '--id']:\n"
            "    payload = {'id': args[2], 'target': args[4]}\n"
            "    with LINKS_PATH.open('a', encoding='utf-8') as handle:\n"
            "        handle.write(json.dumps(payload) + '\\n')\n"
            "    print(json.dumps({'status': 'linked'}))\n"
            "elif args[:2] == ['index', 'rebuild']:\n"
            "    INDEX_PATH.write_text('rebuilt', encoding='utf-8')\n"
            "    print(json.dumps({'status': 'rebuilt'}))\n"
            "else:\n"
            "    print(json.dumps({'error': 'unsupported command', 'args': args}))\n"
            "    sys.exit(2)\n",
            encoding="utf-8",
        )
        script_path.chmod(0o755)
        return script_path


if __name__ == "__main__":
    unittest.main()
