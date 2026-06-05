# Admin Trading Desk Pro Session Journal

This guide explains how to use the Session Journal features of the Desk Pro system on the `admin-trading` machine.

## Overview

The Session Journal is a simple, appended text file that tracks manual operator notes and automated system events (like successful runs). It serves as a lightweight "handover" log between sessions.

## Commands

### 1. Show Journal
Display the entire session journal:
```bash
desk-pro show-session-journal
# OR
desk-pro-session-journal show
```

### 2. Add Note
Append a manual note to the journal (automatically timestamped):
```bash
desk-pro add-session-note "Market looks volatile, reducing risk."
# OR
desk-pro-session-journal add-entry "Reviewing execution logs."
```

## Directory Structure

Journal file location:
`data/logs/desk_pro/session_journal.log`

Format:
`[YYYY-MM-DD HH:MM:SS UTC] [username] Message content`

## Integration

- **Automated Entries**: `desk-pro run-logged` automatically appends an entry upon run completion (Success/Fail).
- **Menu Integration**: The Ops Menu (`menu-desk-pro`) includes options to view and append to the journal.
- **Global Access**: Installing via `desk_pro_install_admin_trading.sh` creates the `desk-pro-session-journal` wrapper.

## RISKS

- À qualifier.
