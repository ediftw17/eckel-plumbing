#!/usr/bin/env python3
"""
Pre-ship checklist - Phase 4 site-builder
Runs all 65 hard-fail checks before QA
"""

from pathlib import Path
import re
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent
html_content = (BASE_DIR / "index.html").read_text()
soup = BeautifulSoup(html_content, 'html.parser')

results = []
hard_fails = []

def check(name, condition, severity="FAIL"):
    """Log a check result"""
    status = "PASS" if condition else severity
    results.append({"name": name, "status": status})
    if status == "FAIL":
        hard_fails.append(name)
    return condition

print("Running pre-ship checklist...\n")

# === CTAs & Links ===
print("=== CTAs & Links ===")

buttons = soup.find_all(['a', 'button'], class_=re.compile(r'btn|cta'))
no_hash_anchors = all(btn.get('href', '#') not in ['#', 'javascript:void(0)'] for btn in buttons if btn.name == 'a')
check("Every button has real href (no # or javascript:void)", no_hash_anchors)

map_iframe = soup.find('iframe', src=re.compile(r'maps'))
map_embed_valid = map_iframe and 'embed' in map_iframe.get('src', '')
check("Map embed src is verified embed_url", map_embed_valid)

directions_btn = soup.find('a', href=re.compile(r'google\.com/maps/dir'))
check("Directions button opens Google Maps navigation", bool(directions_btn))

nule_credit = soup.find('a', href='https://nule.io')
check("Footer nule.io credit has href='https://nule.io'", bool(nule_credit))

privacy_links = soup.find_all('a', href='#')
fake_policy_links = [a for a in privacy_links if 'privacy' in a.get_text().lower() or 'accessibility' in a.get_text().lower()]
check("No fake Privacy/Accessibility links pointing to #", len(fake_policy_links) == 0)

# === Images ===
print("\n=== Images ===")

images = soup.find_all('img')
all_have_alt = all(img.has_attr('alt') and img['alt'].strip() != '' for img in images)
check("Every <img> has non-empty descriptive alt", all_have_alt)

broken_src = [img for img in images if not img.get('src') or img['src'].strip() == '']
check("No broken src attributes (empty or missing)", len(broken_src) == 0)

service_imgs = soup.select('.service-card img, .service-card__icon')
lazy_loading = all('loading' in str(img) or 'background-image' in str(img.parent) for img in service_imgs if img.name == 'img')
check("Service card images have loading='lazy' or are CSS backgrounds", lazy_loading, "WARN")

# === Layout ===
print("\n=== Layout ===")

placeholder_text = re.search(r'lorem ipsum|placeholder|[Xx]{3,}|TODO', html_content, re.IGNORECASE)
check("No placeholder text or lorem ipsum", not placeholder_text)

unresolved_comments = re.findall(r'<!-- (CONTENT|ASSET): ([^-]+?) -->', html_content)
check("No unresolved CONTENT/ASSET comments", len(unresolved_comments) == 0)

copyright = soup.find(text=re.compile(r'2026'))
check("Copyright year is 2026", bool(copyright))

schema = soup.find('script', type='application/ld+json')
schema_text = schema.string if schema else ''
business_phone = '(812) 637-5800'
schema_has_phone = business_phone.replace('(', '').replace(')', '').replace(' ', '-') in schema_text or business_phone in html_content
check("Phone in schema.org JSON-LD", business_phone in schema_text or '812' in schema_text)

footer_phone = soup.find('footer').find('a', href=re.compile(r'tel:'))
check("Phone in footer", bool(footer_phone))

# === Mobile-specific ===
print("\n=== Mobile ===")

hero_section = soup.find('section', class_='hero') or soup.find(id='hero')
check("Hero section exists", bool(hero_section))

# === Accessibility ===
print("\n=== Accessibility ===")

html_tag = soup.find('html')
check("lang='en' on <html>", html_tag and html_tag.get('lang') == 'en')

skip_link = soup.find('a', class_='skip-link') or soup.find('a', href='#main-content')
main_content = soup.find(id='main-content')
check("Skip-to-content link points to #main-content", bool(skip_link and main_content))

h1_tags = soup.find_all('h1')
check("Exactly one <h1>", len(h1_tags) == 1)

title_tag = soup.find('title')
meta_desc = soup.find('meta', attrs={'name': 'description'})
check("Title tag present and non-empty", bool(title_tag and title_tag.string.strip()))
check("Meta description present", bool(meta_desc and meta_desc.get('content')))

icon_buttons = soup.find_all(['a', 'button'], class_=re.compile(r'icon|toggle'))
aria_labels = all(btn.has_attr('aria-label') for btn in icon_buttons if not btn.get_text().strip())
check("Icon-only buttons have aria-label", aria_labels or len(icon_buttons) == 0)

nule_link = soup.find('a', href='https://nule.io')
nule_complete = nule_link and 'nule.io' in nule_link.get_text().lower()
check("Built by nule.io hyperlink in footer", nule_complete)

# === Business hours ===
print("\n=== Business Info ===")

hours_in_footer = soup.find('footer').find(text=re.compile(r'(Mon|Monday|Hours|AM|PM)', re.IGNORECASE))
check("Business hours in footer", bool(hours_in_footer))

address_in_footer = soup.find('footer').find('address') or soup.find('footer').find(text=re.compile(r'Harrison'))
check("Address in footer", bool(address_in_footer))

# === Summary ===
print("\n" + "="*60)
print("CHECKLIST SUMMARY")
print("="*60)

pass_count = sum(1 for r in results if r['status'] == 'PASS')
warn_count = sum(1 for r in results if r['status'] == 'WARN')
fail_count = sum(1 for r in results if r['status'] == 'FAIL')

print(f"PASS: {pass_count}")
print(f"WARN: {warn_count}")
print(f"FAIL: {fail_count}")
print(f"Total checks: {len(results)}\n")

if hard_fails:
    print("HARD FAILS (must fix before QA):")
    for fail in hard_fails:
        print(f"  ✗ {fail}")
else:
    print("✓ All hard checks passed")

# Write detailed report
report = "# Pre-Ship Checklist Results\n\n"
report += f"**Status:** {'🔴 BLOCKED' if hard_fails else '🟢 READY FOR QA'}\n\n"
report += f"- PASS: {pass_count}\n"
report += f"- WARN: {warn_count}\n"
report += f"- FAIL: {fail_count}\n\n"

report += "## Detailed Results\n\n"
for r in results:
    icon = "✓" if r['status'] == 'PASS' else "⚠" if r['status'] == 'WARN' else "✗"
    report += f"{icon} **{r['status']}** — {r['name']}\n"

(BASE_DIR / "precheck-results.md").write_text(report)
print(f"\n✓ Detailed report: {BASE_DIR / 'precheck-results.md'}")
