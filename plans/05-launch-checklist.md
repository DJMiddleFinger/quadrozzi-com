# 05 — Launch Checklist

## Content to collect
- [x] GBX page built at `/gbx/`
- [x] Helping Hoof Initiative page built at `/helping-hooves/` from published sources (6sqft, Brooklyn Eagle, Brooklyn Reporter, Patch, IRS/ProPublica)
- [ ] Contact emails (general, press, leasing) and a mailing address
- [ ] Verified heritage copy and figures for the stat tiles
- [x] Photos: hero, GBX, Brooklyn Equine, Helping Hoof Initiative, heritage (Commons + Brooklyn Equine; swap for family photography when available)
- [ ] Family approval of the positioning line and the pull quote

## GBX pages
- [x] GBX contact: info@Quadrozzi.com only; phone and street address removed from the page
- [ ] Decide how inquiries arrive: the email-app default, or a form service set in the `endpoint` in `inquiry_config` (`tools/build_site.py`)
- [ ] Review the "Spaces & Settings" descriptions against what's actually offered (interiors, base camp, piers)
- [ ] Optional: replace Commons photos with the family's own photography and update `tools/credits.json`

## Helping Hoof Initiative pages
- [ ] Family review of the page copy, quotes and timeline
- [x] Rebuilt from the hhi logo and the Home, About, Programs, Corporate Retreat, Meet the Team and Shop designs (Nov 2026)
- [ ] Confirm info@hhi.horse receives the form messages
- [ ] Set the Corporate Package price (blank on the flyer; the page says "Contact us for per-person pricing")
- [ ] Set shop prices and decide how orders work: the shop links open the Get involved form for now, because "Add to Cart" needs a store
- [ ] Replace the four shop images with real product photos (they look like AI-generated mockups, and two carry a generator mark)
- [ ] Add bios for Xiomara Peralta and Judith Gruntz, photos of Judith Gruntz and Williamsburg, and the ambassadors' ages and heights (blank on the design)
- [ ] Confirm the Horse Hangouts mentoring description (the design repeats the Intergenerational program sentence) and the spelling of Cavallucci
- [ ] Add the Horseplay turnout schedule and the Instagram and LinkedIn links; link helpinghoofinitiative.com once the domain is live
- [ ] Confirm the photos cropped from the designs are cleared to publish, with consent from anyone pictured, and swap in full-size originals
- [ ] Add an online donation link in `HOOVES.donate` (or keep donations by email)

## Build
- [x] Photos in place (Wikimedia Commons, credited on each site's `credits/` page)
- [x] 1200×630 Open Graph image (`site/assets/og.jpg`) and `og:image` tags on every page except Helping Hoof Initiative
- [ ] Switch `og:image` to https once quadrozzi.com has a valid certificate (`OG_IMAGE` in `tools/build_site.py`, plus `site/index.html` and `site/contact/index.html`)
- [ ] Share image for Helping Hoof Initiative
- [ ] Add a favicon

## Hosting (GitHub Pages, the same setup as Brooklyn Equine)
- [x] GitHub repo created (DJMiddleFinger/quadrozzi-com), Pages source: **GitHub Actions**
- [ ] Add `site/CNAME` containing `Quadrozzi.com`
- [ ] DNS at the registrar: four `A` records for the apex pointing to 185.199.108.153 / .109.153 / .110.153 / .111.153, plus `CNAME www → <user>.github.io`
- [ ] Turn on "Enforce HTTPS" once the certificate is issued

## QA
- [ ] Phone (360–414px), tablet and desktop: no horizontal scroll, menu works
- [ ] Every outbound link opens the correct venture in a new tab
- [ ] Lighthouse: Performance, Accessibility, Best Practices and SEO all 90+
- [ ] Keyboard-only navigation works with visible focus, and reduced motion is respected
- [ ] Test the social share preview (Open Graph) with the LinkedIn Post Inspector
