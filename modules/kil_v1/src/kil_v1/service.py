from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any
from uuid import uuid4

from .contracts import REQUIRED_POLICIES, require_fields
from .errors import PolicyError, ValidationError
from .memory_bricks_sync import sync_to_memory_bricks
from .provider_ollama import call_ollama_provider
from .storage import KilStorage, now_z


def run_campaign(spec: dict[str, Any], workspace_root: Path) -> dict[str, Any]:
    storage = KilStorage(workspace_root)
    storage.initialize()

    campaign_id = _build_id("KIL")
    created_at = now_z()
    topic_payload = _require_topic(spec)
    policies = _require_policies(spec, campaign_id)

    campaign = {
        "id": campaign_id,
        "status": "DRAFT",
        "title": topic_payload["title"],
        "created_at": created_at,
        "updated_at": created_at,
        "requested_goal": topic_payload["requested_goal"],
    }
    _persist(storage, "campaigns", campaign)

    topic = dict(topic_payload)
    topic["campaign_id"] = campaign_id
    topic["topic_id"] = _build_id("TOPIC")
    topic["created_at"] = created_at
    _persist(storage, "topics", topic)
    _journal(storage, campaign_id, "topic_created", "topic", topic["topic_id"], None, "DRAFT", "Topic Framing Auditor", {"title": topic["title"]})

    for policy_type, policy_payload in policies.items():
        _persist(storage, "policies", policy_payload)

    framing = _build_framing(spec, campaign_id)
    _persist(storage, "framings", framing)
    _advance_campaign(storage, campaign, "FRAMED", "frame_completed", "framing_audit", framing["framing_id"], "Topic Framing Auditor")

    question = _build_question(spec, campaign_id)
    _persist(storage, "question_sets", question)
    _advance_campaign(storage, campaign, "QUESTIONED", "question_generated", "question_set", question["question_set_id"], "Question Generator")

    responses_input = spec.get("responses")
    if not isinstance(responses_input, list) or not responses_input:
        raise ValidationError("At least one response is required")

    response_records: list[dict[str, Any]] = []
    evaluation_records: list[dict[str, Any]] = []
    for response_input in responses_input:
        resolved_response_input = _materialize_response_input(question, response_input)
        run = _build_run(campaign_id, question, resolved_response_input)
        _persist(storage, "runs", run)

        response = _build_response(campaign_id, run, question, resolved_response_input)
        _persist(storage, "responses", response)
        _journal(storage, campaign_id, "response_captured", "response_record", response["response_id"], None, response["response_status"], "Responder Adapter", {"target_label": run["target_label"]})

        if response["response_status"] != "READY_FOR_EVAL":
            _advance_campaign(storage, campaign, "BLOCKED", "response_unusable", "response_record", response["response_id"], "Responder Adapter")
            raise ValidationError(response["responder_meta"].get("provider_error") or "No exploitable response captured")

        evaluation = _build_evaluation(spec, campaign_id, question, resolved_response_input, response)
        _persist(storage, "evaluations", evaluation)
        _journal(storage, campaign_id, "response_evaluated", "evaluation_record", evaluation["evaluation_id"], None, evaluation["evaluation_status"], "Evaluator", {"verdict": evaluation["evaluator_verdict"]})

        response_records.append(response)
        evaluation_records.append(evaluation)

    _advance_campaign(storage, campaign, "ANSWERED", "responses_completed", "campaign", campaign_id, "Interview Orchestrator")
    _advance_campaign(storage, campaign, "EVALUATED", "evaluations_completed", "campaign", campaign_id, "Evaluator")

    comparison_record = None
    comparison_input = spec.get("comparison") or {}
    comparison_enabled = bool(comparison_input.get("enabled")) and len(response_records) > 1
    if comparison_enabled:
        comparison_record = _build_comparison(campaign_id, question, response_records, evaluation_records, comparison_input)
        _persist(storage, "comparisons", comparison_record)
        _advance_campaign(storage, campaign, "COMPARED", "comparison_completed", "comparison_record", comparison_record["comparison_id"], "Evaluator")

    _advance_campaign(storage, campaign, "CAPITALIZATION_PENDING", "capitalization_started", "campaign", campaign_id, "Memory Promotion Gate")
    capitalization = _build_capitalization(spec, campaign_id, topic, question, response_records, evaluation_records, comparison_record, storage)
    _persist(storage, "capitalizations", capitalization)
    if capitalization["promotion_status"].startswith("PROMOTED_"):
        sync_result = sync_to_memory_bricks(
            workspace_root=workspace_root,
            campaign_id=campaign_id,
            capitalization_id=capitalization["capitalization_id"],
            brick_payload=capitalization["candidate_memory_payload"],
            links=capitalization["memory_brick_links"],
        )
        capitalization["promoted_memory_brick_id"] = sync_result.promoted_memory_brick_id
        capitalization["memory_sync_status"] = sync_result.memory_sync_status
        capitalization["memory_sync_at"] = sync_result.memory_sync_at
        capitalization["memory_sync_error"] = sync_result.memory_sync_error
        _persist(storage, "capitalizations", capitalization)
        _journal(
            storage,
            campaign_id,
            "memory_bricks_sync_completed" if sync_result.memory_sync_status == "SYNCED" else "memory_bricks_sync_failed",
            "capitalization_record",
            capitalization["capitalization_id"],
            None,
            sync_result.memory_sync_status,
            "Journal / Storage",
            {
                "promoted_memory_brick_id": capitalization["promoted_memory_brick_id"],
                "memory_sync_error": capitalization["memory_sync_error"],
            },
        )
    _journal(storage, campaign_id, "capitalization_completed", "capitalization_record", capitalization["capitalization_id"], None, capitalization["promotion_status"], "Memory Promotion Gate", {"granted_level": capitalization["granted_level"]})
    _advance_campaign(storage, campaign, "CAPITALIZED", "capitalization_recorded", "capitalization_record", capitalization["capitalization_id"], "Memory Promotion Gate")

    exports = _write_exports(storage, campaign, topic, framing, question, response_records, evaluation_records, comparison_record, capitalization)
    _advance_campaign(storage, campaign, "EXPORTED", "exports_published", "export_record", exports[0]["export_id"], "Journal / Storage")

    integrity = audit_campaign_integrity(workspace_root, campaign_id)
    if not integrity["ok"]:
        _advance_campaign(storage, campaign, "BLOCKED", "integrity_failed", "campaign", campaign_id, "Journal / Storage")
        raise ValidationError(f"Campaign integrity failed: {'; '.join(integrity['issues'])}")

    _advance_campaign(storage, campaign, "CLOSED", "campaign_closed", "campaign", campaign_id, "Interview Orchestrator")
    return {
        "campaign_id": campaign_id,
        "final_status": campaign["status"],
        "granted_promotion_level": capitalization["granted_level"],
        "promotion_status": capitalization["promotion_status"],
        "memory_sync_status": capitalization["memory_sync_status"],
        "promoted_memory_brick_id": capitalization["promoted_memory_brick_id"],
        "comparison_winner": None if comparison_record is None else comparison_record["winner_or_none"],
        "workspace": str(workspace_root),
        "exports": [record["file_path"] for record in exports],
    }


def audit_campaign_integrity(workspace_root: Path, campaign_id: str) -> dict[str, Any]:
    storage = KilStorage(workspace_root)
    issues: list[str] = []

    required_paths = [
        storage.db_path,
        storage.jsonl_dir / "campaigns.jsonl",
        storage.jsonl_dir / "topics.jsonl",
        storage.jsonl_dir / "framings.jsonl",
        storage.jsonl_dir / "question_sets.jsonl",
        storage.jsonl_dir / "runs.jsonl",
        storage.jsonl_dir / "responses.jsonl",
        storage.jsonl_dir / "evaluations.jsonl",
        storage.jsonl_dir / "capitalizations.jsonl",
        storage.jsonl_dir / "journal.jsonl",
        storage.exports_dir / campaign_id / "campaign_summary.md",
        storage.exports_dir / campaign_id / "evaluation_report.md",
        storage.exports_dir / campaign_id / "capitalization_candidate.md",
        storage.exports_dir / campaign_id / "resume_point.txt",
    ]
    for path in required_paths:
        if not path.exists():
            issues.append(f"missing artifact: {path}")

    if storage.count_journal_events(campaign_id) < 6:
        issues.append("journal event count too low")

    return {"campaign_id": campaign_id, "ok": not issues, "issues": issues}


def _require_topic(spec: dict[str, Any]) -> dict[str, Any]:
    topic = spec.get("topic")
    if not isinstance(topic, dict):
        raise ValidationError("topic must be an object")
    require_fields(topic, ("title", "topic_text", "domain", "requested_goal"), "topic")
    topic.setdefault("source_refs", [])
    return dict(topic)


def _require_policies(spec: dict[str, Any], campaign_id: str) -> dict[str, dict[str, Any]]:
    raw = spec.get("policies")
    if not isinstance(raw, dict):
        raise PolicyError("Missing policies block")
    policies: dict[str, dict[str, Any]] = {}
    for policy_type in REQUIRED_POLICIES:
        payload = raw.get(policy_type)
        if not isinstance(payload, dict):
            raise PolicyError(f"Missing required policy: {policy_type}")
        require_fields(payload, ("policy_id", "policy_version", "policy_text"), f"policy {policy_type}")
        policies[policy_type] = {
            "policy_id": str(payload["policy_id"]),
            "campaign_id": campaign_id,
            "policy_type": policy_type,
            "policy_version": str(payload["policy_version"]),
            "policy_text": str(payload["policy_text"]),
            "active_flag": True,
            "created_at": now_z(),
        }
    return policies


def _build_framing(spec: dict[str, Any], campaign_id: str) -> dict[str, Any]:
    framing = spec.get("framing")
    if not isinstance(framing, dict):
        raise ValidationError("framing must be an object")
    require_fields(framing, ("objective_reframed",), "framing")
    if not framing.get("scope_allowed") or not framing.get("out_of_scope") or not framing.get("known_risks"):
        raise ValidationError("framing requires scope_allowed, out_of_scope and known_risks")
    return {
        "framing_id": _build_id("FRAME"),
        "campaign_id": campaign_id,
        "objective_reframed": str(framing["objective_reframed"]),
        "scope_allowed": list(framing["scope_allowed"]),
        "out_of_scope": list(framing["out_of_scope"]),
        "assumptions": list(framing.get("assumptions", [])),
        "known_risks": list(framing["known_risks"]),
        "validation_policy_id": "framing-v1",
        "framing_status": "FRAME_ACCEPTED",
        "auditor_notes": "Gate 0 passed",
        "created_at": now_z(),
    }


def _build_question(spec: dict[str, Any], campaign_id: str) -> dict[str, Any]:
    question = spec.get("question")
    if not isinstance(question, dict):
        raise ValidationError("question must be an object")
    require_fields(question, ("question_text", "question_type", "expected_answer_mode", "prompt_template_id"), "question")
    normalization_rules = question.get("normalization_rules")
    if not isinstance(normalization_rules, list) or not normalization_rules:
        raise ValidationError("question.normalization_rules must be a non-empty list")
    return {
        "question_set_id": _build_id("QUESTION"),
        "campaign_id": campaign_id,
        "question_version": "1.0",
        "question_text": str(question["question_text"]),
        "question_type": str(question["question_type"]),
        "expected_answer_mode": str(question["expected_answer_mode"]),
        "prompt_template_id": str(question["prompt_template_id"]),
        "normalization_rules": list(normalization_rules),
        "created_at": now_z(),
    }


def _build_run(campaign_id: str, question: dict[str, Any], response_input: dict[str, Any]) -> dict[str, Any]:
    require_fields(response_input, ("target_label", "surface", "machine", "operator"), "response")
    created_at = now_z()
    return {
        "run_id": _build_id("RUN"),
        "campaign_id": campaign_id,
        "question_set_id": question["question_set_id"],
        "mode": "comparative" if response_input.get("comparison_slot") else "single_answer",
        "target_label": str(response_input["target_label"]),
        "surface": str(response_input["surface"]),
        "machine": str(response_input["machine"]),
        "operator": str(response_input["operator"]),
        "run_status": "ANSWERED",
        "started_at": created_at,
        "ended_at": created_at,
    }


def _build_response(campaign_id: str, run: dict[str, Any], question: dict[str, Any], response_input: dict[str, Any]) -> dict[str, Any]:
    raw_response = str(response_input["response_text"])
    normalized = _normalize_text(raw_response, question["normalization_rules"])
    status = "READY_FOR_EVAL" if normalized else "INVALID_FORMAT"
    override = response_input.get("question_text_override")
    response_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return {
        "response_id": _build_id("RESP"),
        "campaign_id": campaign_id,
        "run_id": run["run_id"],
        "raw_response": raw_response,
        "normalized_response": normalized,
        "response_hash": response_hash,
        "responder_meta": {
            "target_label": run["target_label"],
            "surface": run["surface"],
            "machine": run["machine"],
            "operator": run["operator"],
            "source_citations": list(response_input.get("source_citations", [])),
            "external_validation": bool(response_input.get("external_validation", False)),
            "provider_label": response_input.get("provider_label"),
            "provider_model": response_input.get("provider_model"),
            "provider_request_id": response_input.get("provider_request_id"),
            "provider_finish_reason": response_input.get("provider_finish_reason"),
            "provider_timeout_seconds": response_input.get("provider_timeout_seconds"),
            "provider_error": response_input.get("provider_error"),
            "question_text_override": override,
        },
        "response_status": status,
        "captured_at": str(response_input.get("captured_at") or now_z()),
    }


def _materialize_response_input(question: dict[str, Any], response_input: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(response_input, dict):
        raise ValidationError("response entries must be objects")

    resolved = dict(response_input)
    provider = resolved.get("provider")
    has_fixture = isinstance(resolved.get("response_text"), str) and bool(str(resolved.get("response_text", "")).strip())
    if provider is None:
        if not has_fixture:
            raise ValidationError("response_text is required when provider is not set")
        resolved.setdefault("provider_label", "fixture")
        resolved.setdefault("provider_model", None)
        resolved.setdefault("provider_request_id", None)
        resolved.setdefault("provider_finish_reason", None)
        resolved.setdefault("provider_timeout_seconds", None)
        resolved.setdefault("provider_error", None)
        resolved.setdefault("captured_at", now_z())
        return resolved

    if not isinstance(provider, dict):
        raise ValidationError("response.provider must be an object")
    provider_type = str(provider.get("type") or "").strip().lower()
    if provider_type != "ollama":
        raise ValidationError(f"Unsupported provider type: {provider_type or 'missing'}")

    resolved.setdefault("surface", "ollama_local")
    resolved.setdefault("machine", "student")
    resolved.setdefault("operator", "system")

    try:
        provider_result = call_ollama_provider(question, resolved)
    except ValidationError as exc:
        resolved["response_text"] = ""
        resolved["source_citations"] = []
        resolved["external_validation"] = False
        resolved["provider_label"] = "ollama"
        resolved["provider_model"] = str(provider.get("model") or "deepseek-r1:1.5b")
        resolved["provider_request_id"] = None
        resolved["provider_finish_reason"] = None
        resolved["provider_timeout_seconds"] = provider.get("timeout_seconds")
        resolved["provider_error"] = str(exc)
        resolved["captured_at"] = now_z()
        return resolved

    resolved.update(provider_result)
    return resolved


def _build_evaluation(
    spec: dict[str, Any],
    campaign_id: str,
    question: dict[str, Any],
    response_input: dict[str, Any],
    response: dict[str, Any],
) -> dict[str, Any]:
    normalized = response["normalized_response"]
    citations = list(response_input.get("source_citations", []))
    external_validation = bool(response_input.get("external_validation", False))
    truth_flags = _detect_truth_claims(normalized, citations, external_validation)
    rhetoric_bias = _detect_rhetoric_bias(normalized, citations, external_validation)
    coverage_score = 1 if len(normalized.split()) >= 12 else 0
    format_score = 1 if response["response_status"] == "READY_FOR_EVAL" else 0
    evidence_score = 2 if external_validation else (1 if citations else 0)
    caution_score = 0 if truth_flags else 1
    total_score = format_score + evidence_score + coverage_score + caution_score

    if response["response_status"] == "INVALID_FORMAT":
        verdict = "REJECT"
        evaluation_status = "EVAL_REJECTED"
    elif evidence_score >= 1 and not truth_flags and not rhetoric_bias:
        verdict = "ACCEPT"
        evaluation_status = "EVAL_COMPLETE"
    elif format_score == 1:
        verdict = "ACCEPT_WITH_NOTES"
        evaluation_status = "EVAL_BIASED_SUSPECTED" if rhetoric_bias else "EVAL_COMPLETE"
    else:
        verdict = "REJECT"
        evaluation_status = "EVAL_REJECTED"

    return {
        "evaluation_id": _build_id("EVAL"),
        "campaign_id": campaign_id,
        "response_id": response["response_id"],
        "evaluation_policy_id": str(spec["policies"]["evaluation"]["policy_id"]),
        "criteria_scores_json": {
            "format_score": format_score,
            "evidence_score": evidence_score,
            "coverage_score": coverage_score,
            "caution_score": caution_score,
        },
        "strengths": _list_strengths(citations, external_validation, coverage_score),
        "weaknesses": _list_weaknesses(response["response_status"], coverage_score),
        "red_flags": truth_flags,
        "truth_claims_detected": bool(truth_flags),
        "bias_notes": rhetoric_bias,
        "certainty_level": _certainty_level(external_validation, citations, truth_flags),
        "question_template_id": question["prompt_template_id"],
        "evaluator_verdict": verdict,
        "evaluation_status": evaluation_status,
        "total_score": total_score,
        "evaluated_at": now_z(),
    }


def _build_comparison(
    campaign_id: str,
    question: dict[str, Any],
    responses: list[dict[str, Any]],
    evaluations: list[dict[str, Any]],
    comparison_input: dict[str, Any],
) -> dict[str, Any]:
    for response in responses:
        override = response["responder_meta"].get("question_text_override")
        if override and str(override) != question["question_text"]:
            raise ValidationError("comparison requires equivalent question prompts")

    ordered = sorted(evaluations, key=lambda item: item["total_score"], reverse=True)
    winner = None
    if len(ordered) >= 2 and ordered[0]["total_score"] != ordered[1]["total_score"]:
        winner = ordered[0]["response_id"]
    return {
        "comparison_id": _build_id("CMP"),
        "campaign_id": campaign_id,
        "response_ids": [response["response_id"] for response in responses],
        "comparison_basis": str(comparison_input.get("basis", "highest_evaluation_score")),
        "winner_or_none": winner,
        "comparison_notes": "Comparison limited to equivalent question prompts.",
        "comparison_status": "COMPARED",
        "compared_at": now_z(),
    }


def _build_capitalization(
    spec: dict[str, Any],
    campaign_id: str,
    topic: dict[str, Any],
    question: dict[str, Any],
    responses: list[dict[str, Any]],
    evaluations: list[dict[str, Any]],
    comparison: dict[str, Any] | None,
    storage: KilStorage,
) -> dict[str, Any]:
    cap_input = spec.get("capitalization") or {}
    requested_level = str(cap_input.get("target_level", "LAB")).upper()
    if requested_level not in {"LAB", "STANDARD", "STRICT"}:
        raise ValidationError("capitalization.target_level must be LAB, STANDARD or STRICT")

    selected_evaluation = _select_best_evaluation(evaluations, comparison)
    selected_response = next(response for response in responses if response["response_id"] == selected_evaluation["response_id"])
    duplicate_exists = storage.response_hash_exists(selected_response["response_hash"], exclude_campaign_id=campaign_id)
    truth_flags = list(selected_evaluation["red_flags"])
    bias_notes = list(selected_evaluation["bias_notes"])
    citations = list(selected_response["responder_meta"].get("source_citations", []))
    external_validation = bool(selected_response["responder_meta"].get("external_validation", False))

    granted_level = "NONE"
    promotion_status = "PROMOTION_REJECTED"
    promotion_reasons: list[str] = []

    if selected_evaluation["evaluator_verdict"] == "REJECT":
        promotion_reasons.append("evaluation_rejected")
    else:
        granted_level = "LAB"
        promotion_status = "PROMOTED_LAB"
        if duplicate_exists:
            promotion_reasons.append("duplicate_response_detected")
        if truth_flags:
            promotion_reasons.append("truth_claims_require_confirmation")
        if bias_notes:
            promotion_reasons.append("evaluator_bias_risk")

        if (
            requested_level in {"STANDARD", "STRICT"}
            and selected_evaluation["evaluator_verdict"] == "ACCEPT"
            and selected_evaluation["certainty_level"] != "HYPOTHESE"
            and not duplicate_exists
            and not truth_flags
            and not bias_notes
        ):
            granted_level = "STANDARD"
            promotion_status = "PROMOTED_STANDARD"

        if requested_level == "STRICT":
            if external_validation and citations and promotion_status == "PROMOTED_STANDARD":
                granted_level = "STRICT"
                promotion_status = "PROMOTED_STRICT"
            elif promotion_status == "PROMOTED_STANDARD":
                promotion_reasons.append("strict_requires_external_validation")

    candidate_status = f"CANDIDATE_{requested_level}"
    record = {
        "capitalization_id": _build_id("CAP"),
        "campaign_id": campaign_id,
        "source_object_ids": [selected_response["response_id"], selected_evaluation["evaluation_id"]],
        "capitalization_type": str(cap_input.get("type", "decision")),
        "candidate_memory_payload": {
            "title": topic["title"],
            "summary_short": question["question_text"],
            "resume_point": "GO_KIL_V1_REGISTER_AND_EXPAND_01",
            "tags": list(cap_input.get("tags", ["kil", "campaign"])),
            "decisions": [topic["requested_goal"]],
            "todo": promotion_reasons,
        },
        "promotion_level_target": requested_level,
        "candidate_status": candidate_status,
        "promotion_status": promotion_status,
        "granted_level": granted_level,
        "promotion_reasons": promotion_reasons,
        "review_notes": "Promotion is conservative by design.",
        "promoted_memory_brick_id": None,
        "memory_sync_status": "NOT_SYNCED",
        "memory_sync_at": None,
        "memory_sync_error": None,
        "memory_brick_links": [campaign_id, f"cap:{_build_id('LINKTMP')}"],
        "created_at": now_z(),
    }

    record["memory_brick_links"] = [campaign_id, record["capitalization_id"]]
    record["candidate_memory_payload"] = {
        "title": topic["title"],
        "type": str(cap_input.get("type", "decision")),
        "summary_short": question["question_text"],
        "resume_point": "GO_KIL_V1_REGISTER_AND_EXPAND_01",
        "tags": list(cap_input.get("tags", ["kil", "campaign"])),
        "decisions": [topic["requested_goal"]],
        "todo": promotion_reasons,
        "project": "opt-trading",
        "module": "kil_v1",
        "surface": "kil_v1",
        "machine": "student",
        "links": record["memory_brick_links"],
    }

    return record


def _write_exports(
    storage: KilStorage,
    campaign: dict[str, Any],
    topic: dict[str, Any],
    framing: dict[str, Any],
    question: dict[str, Any],
    responses: list[dict[str, Any]],
    evaluations: list[dict[str, Any]],
    comparison: dict[str, Any] | None,
    capitalization: dict[str, Any],
) -> list[dict[str, Any]]:
    export_dir = storage.exports_dir / campaign["id"]
    export_dir.mkdir(parents=True, exist_ok=True)

    summary_path = export_dir / "campaign_summary.md"
    summary_text = "\n".join(
        [
            f"# Campaign {campaign['id']}",
            "",
            f"- Title: {topic['title']}",
            f"- Status: {campaign['status']}",
            f"- Framing: {framing['framing_status']}",
            f"- Question template: {question['prompt_template_id']}",
            f"- Responses: {len(responses)}",
            f"- Promotion: {capitalization['promotion_status']} ({capitalization['granted_level']})",
            f"- Memory sync: {capitalization['memory_sync_status']}",
        ]
    ) + "\n"
    summary_path.write_text(summary_text, encoding="utf-8")

    eval_path = export_dir / "evaluation_report.md"
    eval_lines = [f"# Evaluation Report {campaign['id']}", ""]
    for evaluation in evaluations:
        eval_lines.extend(
            [
                f"## {evaluation['response_id']}",
                f"- Verdict: {evaluation['evaluator_verdict']}",
                f"- Status: {evaluation['evaluation_status']}",
                f"- Total score: {evaluation['total_score']}",
                f"- Red flags: {', '.join(evaluation['red_flags']) if evaluation['red_flags'] else 'none'}",
                f"- Bias notes: {', '.join(evaluation['bias_notes']) if evaluation['bias_notes'] else 'none'}",
            ]
        )
    eval_path.write_text("\n".join(eval_lines) + "\n", encoding="utf-8")

    cap_path = export_dir / "capitalization_candidate.md"
    cap_lines = [
        f"# Capitalization Candidate {campaign['id']}",
        "",
        f"- Requested level: {capitalization['promotion_level_target']}",
        f"- Granted level: {capitalization['granted_level']}",
        f"- Promotion status: {capitalization['promotion_status']}",
        f"- Memory sync status: {capitalization['memory_sync_status']}",
        f"- Memory brick id: {capitalization['promoted_memory_brick_id'] or 'none'}",
        f"- Reasons: {', '.join(capitalization['promotion_reasons']) if capitalization['promotion_reasons'] else 'none'}",
    ]
    if capitalization["memory_sync_error"]:
        cap_lines.append(f"- Memory sync error: {capitalization['memory_sync_error']}")
    if comparison:
        cap_lines.append(f"- Comparison winner: {comparison['winner_or_none'] or 'none'}")
    cap_path.write_text("\n".join(cap_lines) + "\n", encoding="utf-8")

    resume_path = export_dir / "resume_point.txt"
    resume_path.write_text("GO_KIL_V1_REGISTER_AND_EXPAND_01\n", encoding="utf-8")

    exports = []
    for export_type, path in (("md", summary_path), ("md", eval_path), ("md", cap_path), ("txt", resume_path)):
        record = {
            "export_id": _build_id("EXPORT"),
            "campaign_id": campaign["id"],
            "export_type": export_type,
            "scope": "campaign",
            "file_path": str(path),
            "generated_at": now_z(),
        }
        _persist(storage, "exports", record)
        exports.append(record)
    return exports


def _advance_campaign(
    storage: KilStorage,
    campaign: dict[str, Any],
    new_status: str,
    event_type: str,
    object_type: str,
    object_id: str,
    actor_role: str,
) -> None:
    previous = campaign["status"]
    campaign["status"] = new_status
    campaign["updated_at"] = now_z()
    _persist(storage, "campaigns", campaign)
    _journal(storage, campaign["id"], event_type, object_type, object_id, previous, new_status, actor_role, {})


def _persist(storage: KilStorage, table: str, record: dict[str, Any]) -> None:
    storage.insert_record(table, record)
    storage.append_stream(table, record)


def _journal(
    storage: KilStorage,
    campaign_id: str,
    event_type: str,
    object_type: str,
    object_id: str,
    from_status: str | None,
    to_status: str | None,
    actor_role: str,
    payload: dict[str, Any],
) -> None:
    record = {
        "event_id": _build_id("EVENT"),
        "campaign_id": campaign_id,
        "event_type": event_type,
        "object_type": object_type,
        "object_id": object_id,
        "from_status": from_status,
        "to_status": to_status,
        "actor_role": actor_role,
        "event_payload_json": payload,
        "timestamp": now_z(),
    }
    storage.insert_record("journal_events", record)
    storage.append_stream("journal", record)


def _normalize_text(text: str, rules: list[str]) -> str:
    normalized = text
    if "strip" in rules:
        normalized = normalized.strip()
    if "collapse_whitespace" in rules:
        normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def _detect_truth_claims(text: str, citations: list[str], external_validation: bool) -> list[str]:
    if citations or external_validation:
        return []
    lowered = text.lower()
    markers = [
        "definitely",
        "guaranteed",
        "proven",
        "always",
        "never",
        "fact",
        "certainly",
        "best forever",
    ]
    return [marker for marker in markers if marker in lowered]


def _detect_rhetoric_bias(text: str, citations: list[str], external_validation: bool) -> list[str]:
    lowered = text.lower()
    flashy_terms = ["best", "amazing", "perfect", "forever", "everything"]
    matches = [term for term in flashy_terms if term in lowered]
    if (text.count("!") >= 2 or len(matches) >= 2) and not citations and not external_validation:
        return ["rhetoric_outweighs_evidence"]
    return []


def _list_strengths(citations: list[str], external_validation: bool, coverage_score: int) -> list[str]:
    strengths: list[str] = []
    if citations:
        strengths.append("includes_source_citations")
    if external_validation:
        strengths.append("externally_validated")
    if coverage_score:
        strengths.append("adequate_coverage")
    return strengths


def _list_weaknesses(response_status: str, coverage_score: int) -> list[str]:
    weaknesses: list[str] = []
    if response_status == "INVALID_FORMAT":
        weaknesses.append("invalid_format")
    if coverage_score == 0:
        weaknesses.append("thin_coverage")
    return weaknesses


def _certainty_level(external_validation: bool, citations: list[str], truth_flags: list[str]) -> str:
    if external_validation and citations and not truth_flags:
        return "ETABLI"
    if citations and not truth_flags:
        return "A_CONFIRMER"
    return "HYPOTHESE"


def _select_best_evaluation(evaluations: list[dict[str, Any]], comparison: dict[str, Any] | None) -> dict[str, Any]:
    if comparison and comparison["winner_or_none"]:
        winner_response_id = comparison["winner_or_none"]
        return next(item for item in evaluations if item["response_id"] == winner_response_id)
    return sorted(evaluations, key=lambda item: item["total_score"], reverse=True)[0]


def _build_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:12].upper()}"


def load_spec(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
