from __future__ import annotations


def badge(label: str, variant: str = "neutral") -> str:
    cred_variants: frozenset[str] = frozenset({
        "cred_set", "cred_absent", "cred_future", "cred_unknown",
    })
    variants: dict[str, str] = {
        "up":            "badge-up",
        "down":          "badge-down",
        "neutral":       "badge-neutral",
        "unknown":       "badge-unknown",
        "minimal":       "badge-minimal",
        "critical":      "badge-critical",
        "noncrit":       "badge-noncrit",
        "info":          "badge-info",
        "impl":          "badge-impl",
        "partial":       "badge-partial",
        "to_build":      "badge-to_build",
        "closed":        "badge-closed",
        "deprecated":    "badge-deprecated",
        "cred_set":      "cred-set",
        "cred_absent":   "cred-absent",
        "cred_future":   "cred-future",
        "cred_unknown":  "cred-unknown",
        "operational":   "badge-operational",
    }
    cls = variants.get(variant, variants["neutral"])
    if variant in cred_variants:
        return f'<span class="{cls}">{label}</span>'
    return f'<span class="badge {cls}">{label}</span>'


def status_badge_operational() -> str:
    return badge("operational", "operational")

STATUS_BADGES: dict[str, str] = {
    "operational": badge("\u25cf operational", "operational"),
    "impl":        badge("\u25cb impl", "impl"),
    "partial":     badge("\u25cc partial", "partial"),
    "to_build":    badge("\u2295 to_build", "to_build"),
    "closed":      badge("\u2715 closed", "closed"),
    "deprecated":  badge("\u2193 deprecated", "deprecated"),
    "minimal":     badge("\u25cb minimal", "minimal"),
}


def pnl_badge(outcome: str) -> str:
    if outcome == "win":
        return badge("WIN", "up")
    if outcome == "loss":
        return badge("LOSS", "down")
    if outcome == "breakeven":
        return badge("BREAKEVEN", "minimal")
    return badge(outcome, "unknown")


def verdict_badge(verdict: str) -> str:
    if verdict == "APPROVED":
        return badge("APPROVED", "up")
    if verdict == "REJECTED":
        return badge("REJECTED", "down")
    return badge(verdict, "unknown")


def closeout_badge(ack: bool) -> str:
    if ack:
        return badge("\u2713 CLOSED", "up")
    return badge("\u26a0 PENDING", "down")


def cred_status_badge(status: str) -> str:
    mapping = {
        "SET":     ("SET",     "cred_set"),
        "ABSENT":  ("ABSENT",  "cred_absent"),
        "FUTURE":  ("FUTURE",  "cred_future"),
        "UNKNOWN": ("UNKNOWN", "cred_unknown"),
    }
    label, variant = mapping.get(status, ("UNKNOWN", "cred_unknown"))
    return badge(label, variant)


def card(content: str, *, accent: str | None = None) -> str:
    accent_attr = f' class="{accent}"' if accent else ""
    return f'<div class="card"{accent_attr}>{content}</div>'


def summary_card(label: str, value: str, *, accent: str | None = None) -> str:
    accent_cls = f' {accent}' if accent else ""
    return (
        f'<div class="summary-card{accent_cls}">'
        f'<div class="num">{value}</div>'
        f'<div class="label">{label}</div>'
        f'</div>'
    )


def kpi_grid(cards: list[str]) -> str:
    inner = "\n".join(cards)
    return f'<div class="kpi-grid">{inner}</div>'


def table(headers: list[str], rows: list[list[str]], *, bordered: bool = True) -> str:
    thead = "<thead><tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr></thead>"
    tbody = "<tbody>"
    for row in rows:
        tbody += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    tbody += "</tbody>"
    cls = ' class="table-bordered"' if bordered else ""
    return f'<table{cls}>{thead}{tbody}</table>'


def section_title(title: str) -> str:
    return f'<div class="section-title">{title}</div>'


def links_bar(links: list[tuple[str, str]]) -> str:
    items = "".join(f'<a href="{href}">{label}</a>' for label, href in links)
    return f'<div class="links-bar">{items}</div>'


def auto_refresh_script(seconds: int) -> str:
    if seconds <= 0:
        return ""
    return f"<script>setTimeout(() => location.reload(), {seconds * 1000});</script>"


def auto_refresh_xhr(interval_s: int, fetch_url: str, render_function: str) -> str:
    return (
        f"<script>setInterval(async () => {{"
        f"try {{"
        f"const r = await fetch('{fetch_url}');"
        f"const d = await r.json();"
        f"{render_function}(d);"
        f"}} catch(e) {{}}"
        f"}}, {interval_s * 1000});"
        f"</script>"
    )


def notice(message: str) -> str:
    return f'<div class="notice">{message}</div>'


def page_shell(
    title: str,
    content: str,
    *,
    sidebar: str = "",
    refresh_s: int = 0,
    css: str = "",
    body_class: str = "",
) -> str:
    sidebar_html = ""
    if sidebar:
        sidebar_html = f'<nav class="sidebar">{sidebar}</nav>'
    layout = (
        f'<div class="layout">'
        f'{sidebar_html}'
        f'<main class="main">{content}</main>'
        f'</div>'
    ) if sidebar else f'<main class="page">{content}</main>'

    body_cls = f' class="{body_class}"' if body_class else ""
    return (
        f'<!DOCTYPE html>\n'
        f'<html lang="en">\n'
        f'<head>\n'
        f'  <meta charset="utf-8"/>\n'
        f'  <meta name="viewport" content="width=device-width,initial-scale=1"/>\n'
        f'  <title>{title}</title>\n'
        f'  <style>{css}</style>\n'
        f'</head>\n'
        f'<body{body_cls}>\n'
        f'{layout}\n'
        f'{auto_refresh_script(refresh_s)}\n'
        f'</body>\n'
        f'</html>'
    )


def sidebar_nav(title: str, *, links: list[tuple[str, str, bool]] = ()) -> str:
    sections: dict[str, list[tuple[str, str, bool]]] = {}
    for label, href, active in links:
        section_key = label.split(" ")[0]
        sections.setdefault(section_key, []).append((label, href, active))

    nav_html = ""
    for section, items in sections.items():
        items_html = ""
        for label, href, active in items:
            active_cls = " nav-active" if active else ""
            items_html += (
                f'<a class="nav-item{active_cls}" href="{href}">'
                f'<span class="nav-label">{label}</span>'
                f'</a>'
            )
        nav_html += (
            f'<div class="nav-section" style="margin-bottom:16px">'
            f'<div class="nav-item" style="color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;padding:4px 10px">{section}</div>'
            f'{items_html}'
            f'</div>'
        )

    return (
        f'<h1>{title}<small>Central UI — opt-trading</small></h1>\n'
        f'{nav_html}'
    )
