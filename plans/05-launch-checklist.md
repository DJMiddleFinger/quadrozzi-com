# 05 — Launch Checklist

## Content to collect
- [x] GBX page built at `/gbx/`
- [x] Helping Hooves page built at `/helping-hooves/` from published sources (6sqft, Brooklyn Eagle, Brooklyn Reporter, Patch, IRS/ProPublica)
- [ ] Contact emails (general, press, leasing) and a mailing address
- [ ] Verified heritage copy and figures for the stat tiles
- [x] Photos: hero, GBX, Brooklyn Equine, Helping Hooves, heritage (Commons + Brooklyn Equine; swap for family photography when available)
- [ ] Family approval of the positioning line and the pull quote

## GBX page
- [ ] Confirm the GBX phone number, email and street address (699 Columbia Street, Brooklyn, NY 11231)
- [ ] Decide how inquiries arrive: the email-app default, or a form service set in `GBX_INQUIRY.endpoint`
- [ ] Review the "Spaces & Settings" descriptions against what's actually offered (interiors, base camp, piers)
- [ ] Optional: replace Commons photos with the family's own photography and update `credits.html`

## Helping Hooves page
- [ ] Family review of the page copy, quotes and timeline
- [ ] Confirm the inbox for Helping Hooves messages (currently Be@Quadrozzi.com)
- [ ] Add an online donation link in `HOOVES.donate` (or keep donations by email)
- [ ] Replace stand-in photos (therapy, mission tiles) with the stable's own photos, with consent from anyone pictured, and update `tools/credits.json`
- [ ] Confirm whether the GallopNYC partnership is still active; the page describes it as starting in 2019

## Build
- [ ] Replace every `[PLACEHOLDER]` and `href="#"` marked with `<!-- LINK: ... -->` in `site/index.html`
- [x] Photos in place (Wikimedia Commons, credited on `credits.html`)
- [x] 1200×630 Open Graph image (`site/assets/og.jpg`)
- [ ] Add a favicon

## Hosting (GitHub Pages, the same setup as Brooklyn Equine)
- [x] GitHub repo created (DJMiddleFinger/quadrozzi-com), Pages source: **GitHub Actions**
- [ ] Add `site/CNAME` containing `quadrozzi.com`
- [ ] DNS at the registrar: four `A` records for the apex pointing to 185.199.108.153 / .109.153 / .110.153 / .111.153, plus `CNAME www → <user>.github.io`
- [ ] Turn on "Enforce HTTPS" once the certificate is issued

## QA
- [ ] Phone (360–414px), tablet and desktop: no horizontal scroll, menu works
- [ ] Every outbound link opens the correct venture in a new tab
- [ ] Lighthouse: Performance, Accessibility, Best Practices and SEO all 90+
- [ ] Keyboard-only navigation works with visible focus, and reduced motion is respected
- [ ] Test the social share preview (Open Graph) with the LinkedIn Post Inspector
