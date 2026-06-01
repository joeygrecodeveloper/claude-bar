# design.md

## Menu Bar Title
- Format: `{daily}% | {weekly}%`
- Error state: `--% | --%`
- No icon — text only

## Dropdown Menu
- `Daily: {x}% (resets in {Xh Ym})`
- `Weekly: {x}% (resets in {Xd Xh})`
- `Last updated: {HH:MM}`
- `---` (separator)
- `Quit`

## Behavior
- Dropdown items are non-clickable labels except Quit
- No alert dialogs — errors are silent, reflected in `--% | --%`
- No preferences window — no configuration UI needed

## Constraints
- macOS native look — no custom fonts, colors, or windows
- Menu bar text should be concise — no labels like "Claude:" prefix