import browser_cookie3


def get_session_cookie():
    jar = browser_cookie3.chrome(domain_name=".claude.ai")
    for c in jar:
        if c.name == "sessionKey":
            return c.value
    raise ValueError("sessionKey cookie not found in Chrome for .claude.ai")
