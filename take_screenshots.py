#!/usr/bin/env python3
"""
Screenshot capture for Phase 4 QA
Takes desktop (1440x900) and mobile (390x844) screenshots
"""

from playwright.sync_api import sync_playwright
from pathlib import Path

BASE_DIR = Path(__file__).parent
HTML_FILE = f"file://{BASE_DIR / 'index.html'}"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

SCREENSHOTS_DIR.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()

    # Desktop screenshot
    print("Taking desktop screenshot (1440x900)...")
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(HTML_FILE)
    page.wait_for_load_state('networkidle')
    page.screenshot(path=str(SCREENSHOTS_DIR / 'desktop-1440.png'), full_page=True)
    page.close()
    print(f"✓ Saved: {SCREENSHOTS_DIR / 'desktop-1440.png'}")

    # Mobile screenshot
    print("\nTaking mobile screenshot (390x844)...")
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto(HTML_FILE)
    page.wait_for_load_state('networkidle')
    page.screenshot(path=str(SCREENSHOTS_DIR / 'mobile-390.png'), full_page=True)
    page.close()
    print(f"✓ Saved: {SCREENSHOTS_DIR / 'mobile-390.png'}")

    browser.close()

print("\n✓ Screenshots complete")
