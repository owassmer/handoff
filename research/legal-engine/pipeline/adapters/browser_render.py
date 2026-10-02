"""Render one page in headless Chrome (Playwright, system Chrome) and print JSON {url, html, responses}.

Run by pipeline/adapters/base.py with research/legal-engine/.venv/bin/python:
  browser_render.py URL [--wait-for CSS] [--capture REGEX] [--timeout SECONDS]
--capture keeps the bodies of the page's own network responses whose URL matches REGEX (for sites whose text
arrives through a JSON API).
"""
import json
import re
import sys

from playwright.sync_api import sync_playwright

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def main():
    a = sys.argv[1:]
    url = a[0]
    wait_for = a[a.index("--wait-for") + 1] if "--wait-for" in a else None
    capture = re.compile(a[a.index("--capture") + 1]) if "--capture" in a else None
    timeout = int(a[a.index("--timeout") + 1]) if "--timeout" in a else 60
    responses = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True, args=["--disable-blink-features=AutomationControlled"])
        ctx = b.new_context(user_agent=UA)
        pg = ctx.new_page()

        def on_response(r):
            if capture and capture.search(r.url):
                try:
                    responses.append({"url": r.url, "status": r.status, "body": r.text()})
                except Exception:  # noqa: BLE001
                    pass
        pg.on("response", on_response)
        pg.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
        if wait_for:
            try:
                pg.wait_for_selector(wait_for, timeout=timeout * 1000)
            except Exception:  # noqa: BLE001
                pass
        pg.wait_for_timeout(3000)
        for _ in range(5):  # a Cloudflare check page replaces itself; give it time
            if "Just a moment" not in pg.content()[:5000]:
                break
            pg.wait_for_timeout(3000)
        out = {"url": pg.url, "html": pg.content(), "responses": responses}
        b.close()
    sys.stdout.write(json.dumps(out))


if __name__ == "__main__":
    main()
