"""
Telegram input normalizer — classifies raw strings into typed Telegram inputs.

Distinguishes:
- public_username (@channel, t.me/channel)
- private_invite (t.me/+HASH, t.me/joinchat/HASH)  
- message_link (t.me/channel/123)
- internal_c_link (t.me/c/...) — not resolvable without prior access
- display_name — needs search, not resolve
- invalid — unclassifiable input
"""

import re
from dataclasses import dataclass
from typing import Optional

USERNAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]{3,31}$")


@dataclass
class TelegramInput:
    raw: str
    kind: str  # public_username, private_invite, message_link, internal_c_link, display_name, invalid
    username: Optional[str] = None
    invite_hash: Optional[str] = None
    message_id: Optional[int] = None
    reason: Optional[str] = None


def normalize_telegram_input(raw: str) -> TelegramInput:
    s = (raw or "").strip()
    if not s:
        return TelegramInput(raw=raw, kind="invalid", reason="empty_input")

    s = s.replace("https://", "").replace("http://", "")
    s = s.replace("telegram.me/", "t.me/")
    s = s.removeprefix("@")

    # t.me/+HASH
    if s.startswith("t.me/+"):
        invite_hash = s.split("t.me/+", 1)[1].split("?", 1)[0].strip("/")
        return TelegramInput(raw=raw, kind="private_invite", invite_hash=invite_hash)

    # t.me/joinchat/HASH
    if s.startswith("t.me/joinchat/"):
        invite_hash = s.split("t.me/joinchat/", 1)[1].split("?", 1)[0].strip("/")
        return TelegramInput(raw=raw, kind="private_invite", invite_hash=invite_hash)

    # t.me/c/... internal private link
    if s.startswith("t.me/c/"):
        return TelegramInput(raw=raw, kind="internal_c_link", reason="requires_prior_access")

    # t.me/username or t.me/username/123
    if s.startswith("t.me/"):
        tail = s.split("t.me/", 1)[1].split("?", 1)[0].strip("/")
        parts = tail.split("/")
        username = parts[0]
        message_id = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None

        if USERNAME_RE.match(username):
            return TelegramInput(
                raw=raw, kind="message_link" if message_id else "public_username",
                username=username, message_id=message_id,
            )
        return TelegramInput(raw=raw, kind="invalid", reason="invalid_username_in_url")

    # direct username
    if USERNAME_RE.match(s):
        return TelegramInput(raw=raw, kind="public_username", username=s)

    # Display name — needs search, not resolve
    if " " in s or len(s) > 0:
        return TelegramInput(raw=raw, kind="display_name", reason="needs_search_not_resolve")

    return TelegramInput(raw=raw, kind="invalid", reason="unclassified")
