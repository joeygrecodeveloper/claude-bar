# requirements.md

## Functional Requirements

### Menu Bar
- Display `[daily]% | [weekly]%` in the menu bar at all times
- Show `--% | --%` on error or while loading

### Dropdown (on click)
- Daily: `{x}%` (resets in `{Xh Ym}`)
- Weekly: `{x}%` (resets in `{Xd Xh}`)
- Last updated timestamp
- "Quit" item at the bottom

### Data
- Poll claude.ai usage API every 5 minutes
- Read session cookie from browser via rookiepy — no stored credentials
- Usage reflects all Claude clients (web, macOS app, VS Code)

## Non-Functional Requirements
- macOS only
- No Dock icon
- No crash on cookie/API failure — degrade to `--% | --%`
- Polling must not block the UI