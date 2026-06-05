"""
Safe Telegram entity resolver — resolves typed inputs to entity records.

Handles:
- public_username → get_entity + optional JoinChannelRequest
- private_invite → CheckChatInviteRequest + optional ImportChatInviteRequest
- display_name, internal_c_link → skipped with reason
- All RPC errors caught and logged, never crash
"""

import time
from typing import Optional

from .normalize import TelegramInput, normalize_telegram_input


def _entity_kind(entity) -> str:
    from telethon.tl.types import User, Channel, Chat
    if isinstance(entity, User):
        return "bot" if getattr(entity, "bot", False) else "user"
    if isinstance(entity, Channel):
        if getattr(entity, "broadcast", False):
            return "channel"
        if getattr(entity, "megagroup", False):
            return "supergroup"
        return "channel"
    if isinstance(entity, Chat):
        return "group"
    return type(entity).__name__


def _entity_record(entity, source_raw: str, method: str) -> dict:
    return {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_raw": source_raw,
        "method": method,
        "status": "ok",
        "entity_kind": _entity_kind(entity),
        "id": getattr(entity, "id", None),
        "username": getattr(entity, "username", None),
        "title": getattr(entity, "title", None) or " ".join(filter(None, [
            getattr(entity, "first_name", None),
            getattr(entity, "last_name", None),
        ])) or None,
        "verified": bool(getattr(entity, "verified", False)),
        "scam": bool(getattr(entity, "scam", False)),
        "fake": bool(getattr(entity, "fake", False)),
        "bot": bool(getattr(entity, "bot", False)),
        "access_hash_present": getattr(entity, "access_hash", None) is not None,
    }


async def resolve_telegram_input(client, raw: str, join: bool = False) -> dict:
    """Resolve a raw Telegram input string to an entity record. Never raises."""
    parsed = normalize_telegram_input(raw)

    try:
        if parsed.kind in ("public_username", "message_link"):
            entity = await client.get_entity(parsed.username)

            if join and _entity_kind(entity) in ("channel", "supergroup"):
                from telethon.tl.functions.channels import JoinChannelRequest
                await client(JoinChannelRequest(entity))

            record = _entity_record(entity, raw, "get_entity")
            record["normalized_username"] = parsed.username
            if parsed.message_id:
                record["message_id"] = parsed.message_id
            record["join_attempted"] = join
            return record

        if parsed.kind == "private_invite":
            from telethon.tl.functions.messages import CheckChatInviteRequest, ImportChatInviteRequest
            await client(CheckChatInviteRequest(parsed.invite_hash))

            if join:
                try:
                    await client(ImportChatInviteRequest(parsed.invite_hash))
                    return {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                            "source_raw": raw, "status": "joined", "method": "import_invite",
                            "invite_hash_present": True, "join_attempted": True}
                except Exception as e:
                    if "USER_ALREADY_PARTICIPANT" in str(e).upper():
                        return {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                "source_raw": raw, "status": "already_participant",
                                "method": "import_invite", "invite_hash_present": True}

            return {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "source_raw": raw, "status": "invite_valid", "method": "check_invite",
                    "invite_hash_present": True, "join_attempted": False}

        return {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "source_raw": raw, "status": "skipped", "kind": parsed.kind,
                "reason": parsed.reason or "unsupported_input_type"}

    except Exception as e:
        etype = type(e).__name__
        emsg = str(e)[:200]

        if "FLOOD_WAIT" in emsg.upper():
            seconds = int(''.join(c for c in emsg if c.isdigit())) if any(c.isdigit() for c in emsg) else 60
            return {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "source_raw": raw, "status": "flood_wait", "seconds": seconds, "kind": parsed.kind}

        if "USERNAME" in emsg.upper() and ("INVALID" in emsg.upper() or "NOT_OCCUPIED" in emsg.upper()):
            return {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "source_raw": raw, "status": "resolve_failed", "kind": parsed.kind,
                    "normalized_username": parsed.username, "error_type": etype,
                    "reason": "username_invalid_or_not_occupied"}

        if "INVITE" in emsg.upper() and ("INVALID" in emsg.upper() or "EXPIRED" in emsg.upper()):
            return {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "source_raw": raw, "status": "invite_failed", "kind": parsed.kind,
                    "error_type": etype, "reason": "invite_invalid_or_expired"}

        return {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "source_raw": raw, "status": "error", "kind": parsed.kind,
                "error_type": etype, "error_message": emsg}
