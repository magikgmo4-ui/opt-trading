"""Voice Operator command menu helpers.

Builds grouped command metadata for UI/menu exposure.
Read-only. No business logic.
"""

from __future__ import annotations

from modules.voice_operator.engine.intent_router import list_intents


COMMAND_GROUPS: list[tuple[str, set[str]]] = [
    (
        "Executive",
        {
            "executive_briefing",
            "executive_regime",
            "executive_risks",
            "executive_opportunities",
            "executive_leaders",
            "executive_laggards",
            "executive_changes",
            "executive_watch",
            "morning_briefing",
        },
    ),
    (
        "Setups",
        {
            "setup_cards",
            "top_setups",
            "setups_all",
            "setup_detail",
            "score_detail",
        },
    ),
    (
        "Assets",
        {
            "asset_state",
            "market_thesis_symbol",
            "btc_full",
            "gold_full",
            "spcx_full",
        },
    ),
    (
        "Reliability",
        {
            "market_thesis_reliability",
        },
    ),
    (
        "System",
        {
            "system_status",
            "telegram_alerts",
            "daily_report",
            "exec_summary",
            "market_view",
            "whats_new",
            "priorities",
            "attention",
            "top_movers",
        },
    ),
]


def grouped_intents() -> list[dict]:
    intents = list_intents()
    grouped: list[dict] = []
    used: set[str] = set()

    for label, ids in COMMAND_GROUPS:
        items = [i for i in intents if i["intent"] in ids]
        if items:
            grouped.append({"group": label, "items": items})
            used.update(i["intent"] for i in items)

    remaining = [i for i in intents if i["intent"] not in used]
    if remaining:
        grouped.append({"group": "Other", "items": remaining})

    return grouped


def quick_commands() -> list[str]:
    return [
        "briefing quotidien",
        "briefing automatique",
        "fiche setup",
        "carte setup",
        "briefing marché",
        "régime de marché",
        "top risques",
        "top opportunités",
        "état BTC",
        "état Gold",
        "état SPCX",
        "état système",
    ]


def asset_shortcuts() -> list[dict]:
    return [
        {
            "asset": "BTC",
            "commands": ["état BTC", "analyse BTC", "thèse BTC"],
        },
        {
            "asset": "Gold",
            "commands": ["état Gold", "analyse Gold"],
        },
        {
            "asset": "SPCX",
            "commands": ["état SPCX", "analyse SPCX"],
        },
        {
            "asset": "ETH",
            "commands": ["état ETH", "analyse ETH"],
        },
        {
            "asset": "SOL",
            "commands": ["état SOL", "analyse SOL"],
        },
        {
            "asset": "XRP",
            "commands": ["état XRP", "analyse XRP"],
        },
        {
            "asset": "NVDA",
            "commands": ["état NVDA"],
        },
        {
            "asset": "MU",
            "commands": ["état MU"],
        },
        {
            "asset": "AVGO",
            "commands": ["état AVGO"],
        },
    ]


def menu_sections() -> list[dict]:
    return [
        {
            "section": "Executive",
            "commands": [
                "briefing quotidien",
                "briefing automatique",
                "briefing marché",
                "régime de marché",
                "top risques",
                "top opportunités",
                "leaders marché",
                "ce qui a changé",
                "à surveiller",
            ],
        },
        {
            "section": "Setups",
            "commands": [
                "fiche setup",
                "carte setup",
                "setups détaillés",
            ],
        },
        {
            "section": "Assets",
            "commands": [
                "état BTC",
                "état Gold",
                "état SPCX",
                "état ETH",
                "état SOL",
                "état XRP",
            ],
        },
        {
            "section": "System",
            "commands": [
                "état système",
                "alertes Telegram",
                "fiabilité BTC",
                "fiabilité globale",
            ],
        },
    ]
