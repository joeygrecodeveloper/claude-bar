# CLAUDE.md

## Project
macOS menu bar app that displays Claude API usage (daily and weekly) as a tray item. Clicking it shows current usage and reset times. No Dock icon — menu bar only.

## Stack
- Python 3
- `rumps` for macOS menu bar integration
- `rookiepy` for reading claude.ai session cookie from browser
- Claude.ai internal API (`/api/organizations`, `/api/organizations/{id}/usage`)

## How It Works
1. Reads `claude.ai` session cookie from browser cookie store via `rookiepy`
2. Calls `GET https://claude.ai/api/organizations` to get org ID
3. Calls `GET https://claude.ai/api/organizations/{id}/usage` for usage data
4. Updates menu bar every 5 minutes
5. Usage reflects all clients (web, macOS app, VS Code)

## Project Structure
- `CLAUDE.md` — this file, read first
- `requirements.md` — functional and non-functional requirements
- `architecture.md` — technical design and data flow
- `design.md` — UI/UX decisions
- `tasks/current.md` — active work
- `tasks/backlog.md` — future work

## Rules for Claude
- Fix bugs one at a time
- Keep code changes small and focused
- Never modify files outside the project directory
- Ask before adding new dependencies
- After each change, state what to test

## Key Constraints
- macOS only
- No Dock icon — LSUIElement = true in Info.plist
- No background server — app polls on a timer
- No credentials stored — reads existing browser session via rookiepy