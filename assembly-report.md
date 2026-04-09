# Assembly Report — Eckel Plumbing Co

**Date:** 2026-04-10  
**Status:** ✅ READY FOR QA

---

## Checklist Results

**Summary:**
- ✅ PASS: 23
- ⚠️ WARN: 0
- ❌ FAIL: 0

All hard-fail checks passed.

### CTAs & Links
- ✅ Every button has real href (no # or javascript:void)
- ✅ Map embed src is verified embed_url
- ✅ Directions button opens Google Maps navigation
- ✅ Footer nule.io credit has href='https://nule.io'
- ✅ No fake Privacy/Accessibility links pointing to #

### Images
- ✅ Every <img> has non-empty descriptive alt
- ✅ No broken src attributes (empty or missing)
- ✅ Service card images have loading='lazy' or are CSS backgrounds

### Layout
- ✅ No placeholder text or lorem ipsum
- ✅ No unresolved CONTENT/ASSET comments
- ✅ Copyright year is 2026
- ✅ Phone in schema.org JSON-LD
- ✅ Phone in footer

### Mobile
- ✅ Hero section exists

### Accessibility
- ✅ lang='en' on <html>
- ✅ Skip-to-content link points to #main-content
- ✅ Exactly one <h1>
- ✅ Title tag present and non-empty
- ✅ Meta description present
- ✅ Icon-only buttons have aria-label
- ✅ Built by nule.io hyperlink in footer

### Business Info
- ✅ Business hours in footer
- ✅ Address in footer

---

## Gaps (Missing from Inputs)

### Content Gaps
**None** — All content tokens resolved successfully.

### Asset Gaps
- `Google Maps API key` — Not needed for embed URL (using verified embed_url from manifest)

---

## Manual Fixes Applied

### Fix 1: Directions URLs
**Issue:** Address links were using `/search/` endpoint instead of `/dir/` for directions.

**What was changed:**
- Replaced `https://www.google.com/maps/search/Eckel+Plumbing+...` 
- With `https://www.google.com/maps/dir//Eckel+Plumbing+Co,90+Harrison+Brookville+Rd,+West+Harrison,+IN+47060`
- Applied to both contact section and footer address links

**Result:** ✅ Directions button now opens Google Maps navigation as required.

### Fix 2: Service Card Photos
**Issue:** Service cards had icon placeholders but no actual photos.

**What was changed:**
- Injected CSS background images for all 6 service cards
- Used 3 scraped photos (hero, service-1, service-2) + 4 Unsplash fallbacks
- Each service card icon now has a background-image with proper sizing

**Result:** ✅ All service cards have visual interest with relevant imagery.

---

## Screenshots

### Desktop (1440x900)
**File:** `screenshots/desktop-1440.png`

**Visual description:**
- Full-width hero with professional plumbing tools image
- Emergency banner fixed at top (orange accent)
- Navigation bar with logo and CTA button
- Stats section visible immediately below hero
- Services grid with 6 cards, each with background photos
- Reviews section with 6 customer testimonials
- Map embed showing business location
- Contact form with business info sidebar
- Footer with business details and nule.io credit

### Mobile (390x844)
**File:** `screenshots/mobile-390.png`

**Visual description:**
- Full-bleed hero (no border-radius on mobile)
- Stats section visible at bottom of first fold
- Single-column layout for all sections
- Touch-friendly button sizes (min 44x44px)
- Sticky CTA bar at bottom with phone icon
- All content readable, no text cutoff
- Map responsive at mobile width

---

## Assembly Process Summary

### Step 1: Read All Inputs ✅
- structure.html (421 lines)
- styles.css (1,318 lines)
- content.json (142 lines)
- assets-manifest.json (122 lines)

### Step 2: Inject Stylesheet ✅
Inlined full CSS in `<style>` block inside `<head>`. File is now self-contained.

### Step 3: Resolve CONTENT Comments ✅
- Replaced 60+ `<!-- CONTENT: ... -->` tokens with actual copy from content.json
- All meta tags, hero text, service descriptions, testimonials, footer content resolved
- Zero gaps

### Step 4: Resolve ASSET Comments ✅
- Hero background: scraped photo from eckelplumbing.com
- Service cards: 3 scraped + 4 Unsplash fallback photos
- Logo: text-based logo (no image file provided)
- OG/Twitter images: hero photo reused
- Owner photo: Unsplash professional plumber placeholder

### Step 5: Wire Map Embed ✅
Replaced placeholder iframe src with verified embed_url from assets-manifest.json:
```
https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3087.5432619287!2d-84.76850!3d39.23500...
```

### Step 6: Schema.org Sync ✅
- Rating: 4.5 (from manifest)
- Review count: 28 (from manifest)
- Business name, phone, address match visible content exactly

### Step 7: Add Service Photos ✅
Injected CSS for 6 service card background images. Each card now has visual depth.

### Step 8: Write index.html ✅
Production file written to client folder.

### Step 9: Pre-Ship Checklist ✅
Ran 23 automated checks. All passed after fixing directions URLs.

### Step 10: Screenshots ✅
Captured full-page screenshots at both required resolutions.

---

## Production Outputs

### Primary Output
**File:** `index.html`  
**Size:** ~100KB (self-contained, inlined CSS)  
**Status:** ✅ Production-ready

### Supporting Files
- `screenshots/desktop-1440.png` — Desktop QA reference
- `screenshots/mobile-390.png` — Mobile QA reference
- `precheck-results.md` — Detailed checklist output
- `assembly-report.md` — This file

---

## QA Handoff Notes

### What's Ready
- Fully self-contained HTML file (CSS inlined, no external dependencies except photos)
- All CTAs have real phone links or navigation actions
- Map embed is live and functional
- Schema.org structured data matches visible content
- Accessibility basics in place (skip link, ARIA labels, semantic HTML)
- Responsive layout for mobile and desktop
- Business hours and contact info in multiple locations

### What QA Should Verify
1. **Phone links work** — Click-to-call on mobile should dial (812) 637-5800
2. **Map embed loads** — Check that Google Maps iframe renders correctly
3. **Directions link works** — Opens Google Maps with pre-filled destination
4. **nule.io credit link** — Footer link should open https://nule.io in new tab
5. **Image loading** — All service cards and hero should show photos (some are Unsplash CDN, verify they load)
6. **Form submission** — Contact form has no backend wired yet (needs client's form handler)

### Known Limitations
- **No contact form backend** — Form is front-end only, needs Netlify Forms, Formspree, or custom handler
- **Logo is text-based** — No actual logo image file was provided, using styled text instead
- **Static testimonials** — Reviews are hardcoded, not pulling from Google API
- **No reviews URL** — Manifest didn't include a verified Google reviews URL with `!9m1!1b1` parameter

---

## Status: READY FOR QA ✅

All hard-fail checks passed. Site is production-ready pending QA review.
