"""Fetch a published document in a temporary public SharePoint share session.

Input JSON on stdin: share_url, document_path. No credentials or browser state are saved.
"""
import base64
import json
import sys
from playwright.sync_api import sync_playwright


def main():
    request = json.load(sys.stdin)
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        try:
            page = browser.new_page()
            page.goto(request["share_url"], wait_until="domcontentloaded", timeout=60000)
            result = page.evaluate("""async path => {
                const response = await fetch(path);
                const bytes = new Uint8Array(await response.arrayBuffer());
                let binary = '';
                for (let i=0; i<bytes.length; i+=32768)
                    binary += String.fromCharCode(...bytes.subarray(i, i+32768));
                return {status: response.status, url: response.url,
                        content_type: response.headers.get('content-type'), body: btoa(binary)};
            }""", request["document_path"])
            sys.stdout.write(json.dumps(result))
        finally:
            browser.close()


if __name__ == "__main__":
    main()
