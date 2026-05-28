# 10_REAL_TEST_PROTOCOL

## Scope
Manual hardware validation for `TABLET_INPUT_PANEL_V1`.

Devices:
- Android tablet
- PC 1
- PC 2

Surfaces:
- Unified Remote
- Stream Deck Mobile
- Android virtual keyboard
- physical keyboard attached to tablet
- tablet trackpad / stylus pointer
- LocalCMS mobile / Web cockpit shortcut
- RustDesk/RDP shortcut only

## Constraints
- No SSH / tmux / Tasker in this GO.
- No runtime trading.
- No scripts.
- No destructive buttons.
- Manual tests only.

## Test A — Unified Remote setup
1. Install Unified Remote server on PC 1.
2. Install Unified Remote server on PC 2.
3. Install Android app on tablet.
4. Pair tablet with PC 1.
5. Pair tablet with PC 2.
6. Switch from PC 1 to PC 2 and back.

PASS:
- both PCs are reachable;
- switch is possible without network reconfiguration;
- no screen duplication is required.

FAIL:
- pairing unstable;
- target PC cannot be selected reliably;
- app requires repeated manual repair.

## Test B — Trackpad / mouse
1. Move cursor slowly.
2. Move cursor quickly.
3. Test left click.
4. Test right click.
5. Test scroll.
6. Test drag/drop.
7. Test multi-monitor movement if available.

PASS:
- usable navigation for 10 minutes;
- no repeated lost click;
- no severe pointer drift.

FAIL:
- latency blocks work;
- drag/drop unreliable;
- scroll unusable.

## Test C — Keyboard
1. Type short text with Android virtual keyboard.
2. Type long text with Android virtual keyboard.
3. Connect physical keyboard to tablet.
4. Type short and long text through physical keyboard.
5. Test `Ctrl+C`, `Ctrl+V`, `Ctrl+Z`, `Ctrl+S`, `Alt+Tab`.

PASS:
- no major key order issue;
- no repeated ghost keys;
- shortcuts reach active PC.

FAIL:
- layout mismatch too severe;
- latency breaks typing;
- physical keyboard does not pass through.

## Test D — Stylus pointer
1. Use stylus to move pointer.
2. Click small buttons.
3. Draw a simple line.
4. Try pressure-sensitive drawing app if available.

PASS:
- useful as pointer / menu selector.

FAIL:
- unsuitable for precision drawing;
- pressure/inclination absent or not transmitted.

## Test E — Custom remote shortcuts
Create minimal profile:

```txt
[Ctrl+Z] [Ctrl+S]
[B]      [E]
[Space]  [Alt+Tab]
[PC1]    [PC2]
```

PASS:
- each button triggers expected action on active PC.

FAIL:
- button target ambiguous;
- PC switch unreliable;
- accidental destructive action possible.

## Test F — Stream Deck Mobile comparison
1. Create 8-button profile.
2. Include LocalCMS, Desk Pro, RustDesk/RDP, Telegram, TradingView links only.
3. Compare visual clarity with Unified Remote custom remote.

PASS:
- better for static cockpit shortcuts.

FAIL:
- less useful than Unified Remote for input/pointer control.

## Test G — Mobile/Figma cockpit compatibility
Cross-check with `GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01`.

1. Open LocalCMS/Web cockpit shortcut.
2. Verify read-only usage.
3. Verify Desk Pro remains separate.
4. Verify RustDesk/RDP shortcut opens support surface only.
5. Verify no button performs trade, git push, merge, reset, kill, or secret mutation.

PASS:
- tablet supports `voir / commander / intervenir` separation.

FAIL:
- cockpit/control/support roles are mixed;
- any destructive shortcut is exposed.
