# architecture.md

## Overview
A lightweight macOS menu bar app built with Python + rumps. It reads the
claude.ai session cookie from Chrome via rookiepy, calls the claude.ai
internal API for usage data, and displays it in the menu bar. Polls every
5 minutes on a background timer.

## Component Breakdown

### 1. Cookie Reader (`cookie.py`)
- Uses `rookiepy.chrome()` to read the `sessionKey` cookie for `claude.ai`
- Returns the cookie string or raises on failure

### 2. API Client (`api.py`)
- `get_org_id(cookie)` — GET `https://claude.ai/api/organizations`
- `get_usage(cookie, org_id)` — GET `https://claude.ai/api/organizations/{id}/usage`
- Returns parsed usage dict or raises on failure

### 3. Menu Bar App (`app.py`)
- `rumps.App` subclass, `LSUIElement = true` (no Dock icon)
- Holds last known state, updates menu bar title and dropdown on each poll
- On error: displays `--% | --%`, retains last known values

### 4. Poller
- `rumps.Timer` fires every 300 seconds (5 min)
- Runs cookie read + API calls in a background thread to avoid blocking UI

## Data Flow
Chrome cookie store
  → rookiepy
  → cookie string
  → api.py (org ID + usage)
  → app.py (menu bar title + dropdown)

## Error Handling
- Cookie failure: show `--% | --%`, retry on next poll
- API failure: same
- No crash, no alert dialogs

## File Structure
claude-bar/
├── app.py
├── cookie.py
├── api.py
├── requirements.txt
└── docs/
    ├── CLAUDE.md
    ├── requirements.md
    ├── architecture.md
    ├── design.md
    └── tasks/
        ├── current.md
        └── backlog.md