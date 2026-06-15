from __future__ import annotations

COLORS: dict[str, str] = {
    "bg":           "#f5f5f7",
    "text":         "#1d1d1f",
    "muted":        "#666",
    "sidebar_bg":   "#1d1d1f",
    "sidebar_text": "#f5f5f7",
    "sidebar_hover": "#333",
    "sidebar_muted": "#888",
    "card_bg":      "#fff",
    "card_border":  "#e6e6e6",
    "card_radius":  "12px",
    "accent_blue":  "#007aff",
    "accent_green": "#30d158",
    "accent_orange":"#ff9f0a",
    "accent_red":   "#ff453a",
    "link_color":   "#007aff",
    "table_header_bg": "#fafafa",
    "table_border": "#eee",
    "pill_radius":  "999px",
}

CSS_RESET = (
    "* { box-sizing: border-box; margin: 0; padding: 0; }"
)

LIGHT_CSS = (
    f"{CSS_RESET}\n"
    f"body {{ font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; "
    f"background: {COLORS['bg']}; color: {COLORS['text']}; }}\n"

    f".layout {{ display: grid; grid-template-columns: 240px 1fr; min-height: 100vh; }}\n"
    f".sidebar {{ background: {COLORS['sidebar_bg']}; color: {COLORS['sidebar_text']}; "
    f"padding: 20px 12px; overflow-y: auto; position: sticky; top: 0; height: 100vh; }}\n"
    f".sidebar h1 {{ font-size: 16px; font-weight: 600; margin-bottom: 20px; "
    f"padding-bottom: 12px; border-bottom: 1px solid {COLORS['sidebar_hover']}; }}\n"
    f".sidebar h1 small {{ display: block; font-size: 11px; font-weight: 400; "
    f"color: {COLORS['sidebar_muted']}; margin-top: 2px; }}\n"

    f".nav-item {{ display: flex; align-items: center; gap: 8px; padding: 6px 10px; "
    f"border-radius: 8px; color: #ccc; text-decoration: none; font-size: 13px; "
    f"margin-bottom: 2px; transition: background .15s; }}\n"
    f".nav-item:hover {{ background: {COLORS['sidebar_hover']}; color: #fff; }}\n"
    f".nav-active {{ background: {COLORS['sidebar_hover']}; color: #fff; }}\n"
    f".nav-icon {{ font-size: 16px; width: 20px; text-align: center; }}\n"
    f".nav-label {{ flex: 1; }}\n"

    f".main {{ padding: 24px 32px; max-width: 1200px; }}\n"
    f".main h2 {{ font-size: 22px; margin-bottom: 8px; }}\n"
    f".main .subtitle {{ color: {COLORS['muted']}; font-size: 14px; margin-bottom: 24px; }}\n"
    f".section-title {{ font-size: 16px; font-weight: 600; margin: 24px 0 12px; }}\n"
)

CARD_CSS = (
    f".card {{ background: {COLORS['card_bg']}; border: 1px solid {COLORS['card_border']}; "
    f"border-radius: {COLORS['card_radius']}; padding: 14px 16px; }}\n"

    f".summary-bar {{ display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }}\n"
    f".summary-card {{ flex: 1; min-width: 120px; padding: 16px; border-radius: {COLORS['card_radius']}; "
    f"border: 1px solid {COLORS['card_border']}; background: {COLORS['card_bg']}; }}\n"
    f".summary-card .num {{ font-size: 28px; font-weight: 700; }}\n"
    f".summary-card .label {{ font-size: 12px; color: {COLORS['muted']}; margin-top: 4px; }}\n"
    f".summary-card .bar {{ font-family: monospace; font-size: 13px; color: {COLORS['accent_green']}; "
    f"letter-spacing: 2px; margin-top: 4px; }}\n"

    f".summary-ok      {{ border-left: 4px solid {COLORS['accent_green']}; }}\n"
    f".summary-warn    {{ border-left: 4px solid {COLORS['accent_orange']}; }}\n"
    f".summary-critical{{ border-left: 4px solid {COLORS['accent_red']}; }}\n"
    f".summary-blue    {{ border-left: 4px solid {COLORS['accent_blue']}; }}\n"

    f".domain-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); "
    f"gap: 12px; margin-bottom: 24px; }}\n"
    f".domain-card {{ background: {COLORS['card_bg']}; border: 1px solid {COLORS['card_border']}; "
    f"border-radius: {COLORS['card_radius']}; padding: 14px 16px; }}\n"
    f".domain-title {{ font-size: 14px; font-weight: 600; margin-bottom: 8px; color: {COLORS['text']}; }}\n"

    f".kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); "
    f"gap: 12px; margin-bottom: 20px; }}\n"
    f".kpi {{ padding: 14px; border-radius: {COLORS['card_radius']}; "
    f"border: 1px solid {COLORS['card_border']}; background: {COLORS['card_bg']}; }}\n"
    f".kpi .num {{ font-size: 26px; font-weight: 700; }}\n"
    f".kpi .label {{ font-size: 11px; color: {COLORS['muted']}; margin-top: 4px; }}\n"
)

BADGE_CSS = (
    f".badge {{ display: inline-block; padding: 2px 8px; border-radius: {COLORS['pill_radius']}; "
    f"font-size: 11px; font-weight: 600; }}\n"

    f".badge-up       {{ background: #d1fae5; color: #065f46; }}\n"
    f".badge-down     {{ background: #ffe4e6; color: #9f1239; }}\n"
    f".badge-neutral  {{ background: #f3f4f6; color: #6b7280; }}\n"
    f".badge-minimal  {{ background: #fef3c7; color: #92400e; }}\n"
    f".badge-critical {{ background: #fef3c7; color: #92400e; font-size: 10px; }}\n"
    f".badge-noncrit  {{ background: #e0e7ff; color: #3730a3; font-size: 10px; }}\n"
    f".badge-info     {{ background: #dbeafe; color: #1e40af; }}\n"

    f".badge-operational {{ background: #d1fae5; color: #065f46; }}\n"
    f".badge-impl      {{ background: #dbeafe; color: #1e40af; }}\n"
    f".badge-partial   {{ background: #fef3c7; color: #92400e; }}\n"
    f".badge-to_build  {{ background: #f3e8ff; color: #6b21a8; }}\n"
    f".badge-closed    {{ background: #e5e7eb; color: #374151; }}\n"
    f".badge-deprecated{{ background: #fce7f3; color: #9d174d; }}\n"

    f".cred-set     {{ display:inline-block;padding:2px 8px;border-radius:{COLORS['pill_radius']};"
    f"font-size:11px;font-weight:600;background:#d1fae5;color:#065f46; }}\n"
    f".cred-absent  {{ display:inline-block;padding:2px 8px;border-radius:{COLORS['pill_radius']};"
    f"font-size:11px;font-weight:600;background:#ffe4e6;color:#9f1239; }}\n"
    f".cred-unknown {{ display:inline-block;padding:2px 8px;border-radius:{COLORS['pill_radius']};"
    f"font-size:11px;font-weight:600;background:#f3f4f6;color:#6b7280; }}\n"
    f".cred-future  {{ display:inline-block;padding:2px 8px;border-radius:{COLORS['pill_radius']};"
    f"font-size:11px;font-weight:600;background:#e0e7ff;color:#3730a3; }}\n"

    f".pill        {{ display: inline-block; padding: 3px 10px; border-radius: {COLORS['pill_radius']}; "
    f"font-size: 12px; margin: 2px 4px 2px 0; }}\n"
    f".pill-danger {{ background: #ffe4e6; color: #9f1239; border: 1px solid #fecdd3; }}\n"
    f".pill-warn   {{ background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}\n"
    f".pill-ok     {{ background: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; }}\n"
)

TABLE_CSS = (
    f"table {{ width: 100%; border-collapse: collapse; background: {COLORS['card_bg']}; "
    f"border-radius: {COLORS['card_radius']}; overflow: hidden; "
    f"border: 1px solid {COLORS['card_border']}; }}\n"
    f"th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid {COLORS['table_border']}; "
    f"font-size: 13px; }}\n"
    f"th {{ background: {COLORS['table_header_bg']}; font-weight: 600; color: {COLORS['muted']}; "
    f"text-transform: uppercase; font-size: 11px; letter-spacing: .5px; }}\n"
    f"tr:hover {{ background: #f9f9fb; }}\n"
    f"a {{ color: {COLORS['link_color']}; text-decoration: none; }}\n"
    f"a:hover {{ text-decoration: underline; }}\n"
)

MISC_CSS = (
    f".notice {{ background: #fef3c7; border: 1px solid #fde68a; border-radius: 8px; "
    f"padding: 10px 14px; font-size: 13px; margin-bottom: 16px; color: #92400e; }}\n"
    f".notice-info {{ background: #dbeafe; border: 1px solid #bfdbfe; color: #1e40af; }}\n"
    f".notice-danger {{ background: #ffe4e6; border: 1px solid #fecdd3; color: #9f1239; }}\n"

    f".links-bar {{ display: flex; gap: 6px; flex-wrap: wrap; margin: 12px 0; }}\n"
    f".links-bar a {{ color: {COLORS['text']}; padding: 4px 10px; border: 1px solid #ddd; "
    f"border-radius: 8px; text-decoration: none; font-size: 12px; }}\n"
    f".links-bar a:hover {{ background: #eee; }}\n"

    f".code-block {{ background: {COLORS['sidebar_bg']}; color: #e8e8e8; "
    f"padding: 12px; border-radius: 10px; font-size: 12px; overflow-x: auto; }}\n"
    f".auto-refresh {{ color: {COLORS['muted']}; font-size: 12px; }}\n"
    f".subgroup {{ margin: 8px 0 4px 12px; }}\n"
    f".subgroup-title {{ font-size: 12px; font-weight: 600; color: {COLORS['muted']}; "
    f"text-transform: uppercase; letter-spacing: .5px; margin-bottom: 4px; }}\n"
    f".module-row {{ display: flex; align-items: center; gap: 8px; padding: 3px 0; font-size: 13px; }}\n"
    f".module-label {{ flex: 1; }}\n"
    f".module-machine {{ font-size: 11px; color: #999; font-family: monospace; }}\n"

    f".card-row {{ display: flex; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; }}\n"
    f".card-pass    {{ border-left: 4px solid {COLORS['accent_green']}; }}\n"
    f".card-fail    {{ border-left: 4px solid {COLORS['accent_red']}; }}\n"
    f".card-blue    {{ border-left: 4px solid {COLORS['accent_blue']}; }}\n"
    f".card-win     {{ border-left: 4px solid {COLORS['accent_green']}; }}\n"
    f".card-loss    {{ border-left: 4px solid {COLORS['accent_red']}; }}\n"
    f".card-neutral {{ border-left: 4px solid #8e8e93; }}\n"

    f".info-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); "
    f"gap: 12px; margin-bottom: 24px; }}\n"
    f".info-card {{ background: {COLORS['card_bg']}; border: 1px solid {COLORS['card_border']}; "
    f"border-radius: {COLORS['card_radius']}; padding: 14px 16px; }}\n"
    f".info-card h4 {{ font-size: 12px; color: {COLORS['muted']}; text-transform: uppercase; "
    f"letter-spacing: .5px; margin-bottom: 6px; }}\n"
    f".info-card .value {{ font-size: 14px; font-weight: 600; }}\n"
    f".info-card .value-mono {{ font-family: monospace; font-size: 13px; }}\n"
)

STANDARD_CSS = (
    f"{LIGHT_CSS}\n"
    f"{BADGE_CSS}\n"
    f"{CARD_CSS}\n"
    f"{TABLE_CSS}\n"
    f"{MISC_CSS}\n"
    # ── Responsive mobile ──
    f"@media (max-width: 768px) {{\n"
    f"  .layout {{ display: flex; flex-direction: column; }}\n"
    f"  .sidebar {{ width: 100%; min-height: auto; padding: 12px; }}\n"
    f"  .sidebar h1 {{ font-size: 16px; }}\n"
    f"  .sidebar h1 small {{ display: none; }}\n"
    f"  .nav-item {{ padding: 6px 8px; font-size: 12px; }}\n"
    f"  .main {{ padding: 12px; }}\n"
    f"  .summary-bar {{ flex-wrap: wrap; gap: 6px; }}\n"
    f"  .summary-card {{ min-width: 100px; flex: 1 1 calc(50% - 6px); }}\n"
    f"  .summary-card .num {{ font-size: 18px; }}\n"
    f"  table {{ font-size: 11px; }}\n"
    f"  th, td {{ padding: 4px 6px; }}\n"
    f"  .voice-btn {{ padding: 6px 10px; font-size: 11px; }}\n"
    f"  .console-input {{ font-size: 14px; }}\n"
    f"  .profile-bar {{ gap: 4px; }}\n"
    f"  .profile-tab {{ padding: 4px 8px; font-size: 10px; }}\n"
    f"  .preset-btn {{ padding: 5px 10px; font-size: 10px; }}\n"
    f"  h2 {{ font-size: 18px; }}\n"
    f"  .subtitle {{ font-size: 12px; }}\n"
    f"}}\n"
    f"@media (max-width: 480px) {{\n"
    f"  .summary-card {{ flex: 1 1 100%; }}\n"
    f"  .voice-buttons {{ gap: 4px; }}\n"
    f"  .voice-btn {{ padding: 8px 12px; font-size: 12px; }}\n"
    f"}}\n"
)

DARK_BASE = (
    f"{CSS_RESET}\n"
    f"body {{ font-family: system-ui, -apple-system, sans-serif; "
    f"background: #0a0e14; color: #c8d6e5; }}\n"
    f".card {{ background: #121820; border: 1px solid #1e2733; "
    f"border-radius: 14px; padding: 20px; }}\n"
)

SIGNALS_DARK_CSS = (
    f"{CSS_RESET}\n"
    f"body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace; "
    f"background: #0d1117; color: #c9d1d9; }}\n"
    f"header {{ background: #161b22; border-bottom: 1px solid #30363d; "
    f"padding: 12px 24px; display: flex; align-items: center; gap: 12px; }}\n"
    f"header a {{ color: #58a6ff; text-decoration: none; font-size: 14px; }}\n"
    f"header h1 {{ font-size: 18px; color: #f0f6fc; }}\n"
    f"main {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}\n"
    f".kpi {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; "
    f"padding: 16px; text-align: center; }}\n"
    f".kpi .num {{ font-size: 28px; font-weight: 700; color: #58a6ff; }}\n"
    f".kpi .num.pnl-positive {{ color: #3fb950; }}\n"
    f".kpi .num.pnl-negative {{ color: #f85149; }}\n"
    f".kpi .label {{ font-size: 11px; color: #8b949e; margin-top: 4px; text-transform: uppercase; }}\n"
    f".kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); "
    f"gap: 12px; margin-bottom: 24px; }}\n"
    f".section {{ margin-bottom: 24px; }}\n"
    f".section h2 {{ font-size: 16px; color: #f0f6fc; margin-bottom: 8px; "
    f"border-bottom: 1px solid #30363d; padding-bottom: 6px; }}\n"
    f"table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}\n"
    f"th {{ text-align: left; padding: 6px 8px; border-bottom: 1px solid #30363d; "
    f"color: #8b949e; font-weight: 600; }}\n"
    f"td {{ padding: 4px 8px; border-bottom: 1px solid #21262d; }}\n"
    f"tr:hover {{ background: #161b22; }}\n"
    f".json-toggle {{ margin-top: 16px; font-size: 12px; }}\n"
    f".json-toggle summary {{ color: #58a6ff; cursor: pointer; }}\n"
    f".json-toggle pre {{ background: #0d1117; border: 1px solid #30363d; "
    f"border-radius: 4px; padding: 12px; overflow-x: auto; font-size: 11px; max-height: 400px; }}\n"
    f".auto-refresh {{ font-size: 11px; color: #484f58; text-align: center; margin-top: 24px; }}\n"
    f".nav-back {{ display: inline-block; padding: 4px 12px; background: #21262d; "
    f"border-radius: 4px; color: #c9d1d9; }}\n"
)
