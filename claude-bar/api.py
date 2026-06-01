import json
import logging
import datetime
import urllib.request

logger = logging.getLogger(__name__)

BASE_URL = "https://claude.ai"


def _get(url, cookie):
    req = urllib.request.Request(
        url,
        headers={
            "Cookie": f"sessionKey={cookie}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read()
        logger.debug("GET %s → %s", url, body[:500])
        return json.loads(body)


def get_org_id(cookie):
    data = _get(f"{BASE_URL}/api/organizations", cookie)
    if isinstance(data, list) and data:
        # Prefer the first org with a uuid field, fall back to id
        org = data[0]
        return org.get("uuid") or org.get("id")
    raise ValueError(f"Unexpected organizations response: {data!r}")


def get_usage(cookie, org_id):
    raw = _get(f"{BASE_URL}/api/organizations/{org_id}/usage", cookie)
    logger.debug("Usage raw: %s", raw)
    return _parse_usage(raw)


def _time_until(reset_str):
    if not reset_str:
        return "--"
    reset = datetime.datetime.fromisoformat(reset_str.replace("Z", "+00:00"))
    now = datetime.datetime.now(datetime.timezone.utc)
    secs = int((reset - now).total_seconds())
    if secs <= 0:
        return "now"
    days, secs = divmod(secs, 86400)
    hours, secs = divmod(secs, 3600)
    minutes = secs // 60
    if days > 0:
        return f"{days}d {hours}h"
    return f"{hours}h {minutes}m"


def _reset_label(reset_str):
    if not reset_str:
        return ""
    reset = datetime.datetime.fromisoformat(reset_str.replace("Z", "+00:00"))
    local = reset.astimezone()
    return f"Resets {local.strftime('%a')} {local.strftime('%-I:%M %p')}"


def _parse_usage(raw):
    five_hour = raw["five_hour"]
    seven_day = raw["seven_day"]
    return {
        "daily_pct": round(five_hour["utilization"]),
        "weekly_pct": round(seven_day["utilization"]),
        "daily_resets_in": _time_until(five_hour["resets_at"]),
        "weekly_resets_in": _time_until(seven_day["resets_at"]),
        "weekly_reset_label": _reset_label(seven_day["resets_at"]),
    }
