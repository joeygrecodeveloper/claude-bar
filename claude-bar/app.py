import logging
import os
import subprocess
import threading
import datetime

import rumps

from cookie import get_session_cookie
from api import get_org_id, get_usage

LAUNCH_AGENT_LABEL = "com.claudebar"
LAUNCH_AGENT_PLIST = os.path.expanduser("~/Library/LaunchAgents/com.claudebar.plist")

logging.basicConfig(
    filename=f"{rumps.application_support('claude-bar')}/claude-bar.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


class ClaudeUsageApp(rumps.App):
    def __init__(self):
        super().__init__("Claude", title="--% | --%", quit_button=None)

        noop = lambda _: None
        self._daily = rumps.MenuItem("Daily: --", callback=noop)
        self._daily_reset = rumps.MenuItem("Resets in --")
        self._weekly = rumps.MenuItem("Weekly: --", callback=noop)
        self._weekly_reset_abs = rumps.MenuItem("Resets --")
        self._updated = rumps.MenuItem("Last updated: --", callback=noop)

        self.menu = [
            self._daily,
            self._daily_reset,
            self._weekly,
            self._weekly_reset_abs,
            self._updated,
            None,
            rumps.MenuItem("Disable Auto-launch", callback=self._disable_autolaunch),
            rumps.MenuItem("Quit", callback=rumps.quit_application),
        ]

        threading.Thread(target=self._poll, daemon=True).start()
        rumps.Timer(self._tick, 300).start()

    def _tick(self, _):
        threading.Thread(target=self._poll, daemon=True).start()

    def _poll(self):
        try:
            cookie = get_session_cookie()
            org_id = get_org_id(cookie)
            usage = get_usage(cookie, org_id)
        except Exception:
            logger.exception("Poll failed")
            self.title = "--% | --%"
            return
        self._refresh(usage)

    def _disable_autolaunch(self, _):
        try:
            subprocess.run(
                ["launchctl", "unload", LAUNCH_AGENT_PLIST],
                check=True, capture_output=True,
            )
            os.remove(LAUNCH_AGENT_PLIST)
            self.menu["Disable Auto-launch"].set_callback(None)
            self.menu["Disable Auto-launch"].title = "Auto-launch disabled"
        except Exception:
            logger.exception("Failed to disable auto-launch")

    def _refresh(self, usage):
        d = usage["daily_pct"]
        w = usage["weekly_pct"]
        self.title = f"{d}% | {w}%"
        self._daily.title = f"Daily: {d}%"
        self._daily_reset.title = f"Resets in {usage['daily_resets_in']}"
        self._weekly.title = f"Weekly: {w}%"
        self._weekly_reset_abs.title = usage["weekly_reset_label"]
        self._updated.title = f"Last updated: {datetime.datetime.now().strftime('%-I:%M %p')}"


if __name__ == "__main__":
    from AppKit import NSApplication, NSApplicationActivationPolicyAccessory
    NSApplication.sharedApplication().setActivationPolicy_(NSApplicationActivationPolicyAccessory)
    ClaudeUsageApp().run()
