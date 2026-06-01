from modules.desk_pro.ui.page import render_ui_html


def test_followup_panel_present():
    html = render_ui_html()
    assert 'id="followupPanel"' in html
    assert 'Follow-up Surfaces' in html


def test_followup_cards_present():
    html = render_ui_html()
    assert 'id="btnNewsVision"' in html
    assert 'id="btnScreenerVision"' in html
    assert 'id="btnTelegramClaim"' in html
    assert 'News Sentiment' in html
    assert 'Screener Context' in html
    assert 'Telegram Claim' in html


def test_followup_routes_referenced_in_js():
    html = render_ui_html()
    assert '/desk/vision/news' in html
    assert '/desk/vision/screener' in html
    assert '/desk/vision/telegram-claim' in html
