# -*- coding: utf-8 -*-
"""Where Chrome lives. Windows keeps the original path; the Linux container
built by Claude Code on the web ships Playwright's Chromium, and CHROME_BIN
overrides both."""
import os
import shutil

CANDIDATES = [
    os.environ.get("CHROME_BIN"),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/opt/pw-browsers/chromium/chrome",
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
]

# Headless Chromium in a container has no sandbox namespaces to use.
FLAGS = ["--no-sandbox", "--disable-dev-shm-usage"] if os.name != "nt" else []


def find():
    for c in CANDIDATES:
        if c and os.path.exists(c):
            return c
    for n in ("google-chrome", "chromium", "chromium-browser"):
        p = shutil.which(n)
        if p:
            return p
    raise SystemExit("no Chrome/Chromium found; set CHROME_BIN")


CHROME = find()
