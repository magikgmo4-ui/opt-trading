"""
telegram_signal_cli.py — CLI entry point for telegram signal queries.
Called from: cmd.sh telegram <subcommand> [args...]
"""
import sys

sys.path.insert(0, ".")

from modules.analysis_bundles.app.telegram_signal_query import (
    query_signals, list_channels, signal_summary, format_table, CHANNEL_TYPE_LABELS
)


def cmd_signals():
    """List signals with optional filters."""
    channel = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "." else None
    pair = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "." else None
    direction = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != "." else None

    signals = query_signals(channel=channel, pair=pair, direction=direction)
    if not signals:
        print("(aucun signal)")
        return

    print(f"Signals: {len(signals)}")
    rows = []
    for s in signals[:80]:
        details = f"{s.get('entry_price','?')} / SL={s.get('sl','?')} / TP={s.get('tp','?')}"
        rows.append({
            "channel": (s.get("channel", "?") or "")[:28],
            "pair": s.get("pair", "?"),
            "dir": s.get("direction", "?"),
            "details": details,
        })
    print(format_table(rows, ["channel", "pair", "dir", "details"]))
    if len(signals) > 80:
        print(f"  ... and {len(signals) - 80} more")


def cmd_complete():
    """List only complete signals (entry + sl + tp)."""
    channel = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "." else None
    pair = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "." else None
    direction = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != "." else None

    signals = query_signals(channel=channel, pair=pair, direction=direction, complete_only=True)
    if not signals:
        print("(aucun signal complet)")
        return

    print(f"Complete signals: {len(signals)}")
    rows = []
    for s in signals[:60]:
        details = f"entry={s.get('entry_price','?')} SL={s.get('sl','?')} TP={s.get('tp','?')}"
        rows.append({
            "channel": (s.get("channel", "?") or "")[:28],
            "pair": s.get("pair", "?"),
            "dir": s.get("direction", "?"),
            "details": details,
        })
    print(format_table(rows, ["channel", "pair", "dir", "details"]))
    if len(signals) > 60:
        print(f"  ... and {len(signals) - 60} more")


def cmd_channels():
    """List all channels by mode."""
    channels = list_channels()
    active = [c for c in channels if c["mode"] == "ACTIVE"]
    watch = [c for c in channels if c["mode"] == "WATCH"]
    discovery = [c for c in channels if c["mode"] == "DISCOVERY"]
    rejected = [c for c in channels if c["mode"] == "REJECTED"]

    print(f"=== ACTIVE ({len(active)}) ===")
    for c in active:
        pairs_str = ",".join(c["pairs"][:4])
        print(f"  {c['alias']:<42s} {c['type_label']:<22s} sig={c['signals_total']:>3d} ok={c['signals_complete']:>3d}  {pairs_str}")

    if watch:
        print(f"\n=== WATCH ({len(watch)}) ===")
        for c in watch:
            print(f"  {c['alias']:<42s} {c['type_label']:<22s} sig={c['signals_total']:>3d} ok={c['signals_complete']:>3d}")

    if discovery:
        print(f"\n=== DISCOVERY ({len(discovery)}) ===")
        for c in discovery:
            print(f"  {c['alias']:<42s} {c['type_label']:<22s}")

    if rejected:
        print(f"\n=== REJECTED ({len(rejected)}) ===")
        for c in rejected:
            print(f"  {c['alias']:<42s} {c['type_label']:<22s}")


def cmd_stats():
    """Dashboard summary."""
    s = signal_summary()
    t = s["totals"]
    print(f"Signals: {t['signals']} total, {t['complete']} complete, {t['incomplete']} incomplete")
    print(f"Direction: {t['longs']} LONG, {t['shorts']} SHORT")
    print(f"Channels actifs: {t['active_channels']}")
    print()
    print("=== Par type ===")
    for ct, info in sorted(s["by_type"].items(), key=lambda x: -x[1]["total"]):
        print(f"  {info['label']:<25s} total={info['total']:>3d} complete={info['complete']:>3d}")
    print()
    print("=== Top paires ===")
    for pair_name, cnt in list(s["by_pair"].items())[:12]:
        print(f"  {pair_name:<14s} {cnt:>3d}")
    print()
    print("=== Top canaux (complete) ===")
    top = sorted(s["by_channel"].items(), key=lambda x: -x[1]["complete"])[:15]
    for ch, info in top:
        print(f"  {ch:<44s} total={info['total']:>3d} complete={info['complete']:>3d}  {info['priority']}")


def cmd_types():
    """Signal type taxonomy."""
    print("Taxonomie des types de signaux:")
    for ct, info in sorted(CHANNEL_TYPE_LABELS.items()):
        print(f"  {info['icon']} {ct:<20s} {info['fr']}")


def cmd_help():
    print("Usage: cmd.sh telegram <subcommand> [filter] [filter] [filter]")
    print()
    print("Subcommands:")
    print("  signals [channel] [pair] [dir]   — all signals (max 80)")
    print("  complete [channel] [pair] [dir]  — complete only (entry+sl+tp)")
    print("  channels                          — channels by mode/type")
    print("  stats                             — dashboard summary")
    print("  types                             — signal type taxonomy")
    print()
    print("Filters (use '.' to skip):")
    print("  signals xauusd                    — only from channel xauusd")
    print("  signals . XAU/USD                 — only XAU/USD signals")
    print("  signals . . LONG                  — only LONG signals")
    print("  complete xauusd . LONG            — complete LONG from xauusd")


COMMANDS = {
    "signals": cmd_signals,
    "complete": cmd_complete,
    "channels": cmd_channels,
    "stats": cmd_stats,
    "summary": cmd_stats,
    "types": cmd_types,
    "help": cmd_help,
    "-h": cmd_help,
    "--help": cmd_help,
    "": cmd_help,
}


if __name__ == "__main__":
    sub = sys.argv[1] if len(sys.argv) > 1 else ""
    handler = COMMANDS.get(sub, cmd_help)
    handler()
