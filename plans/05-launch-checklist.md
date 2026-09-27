# 05 — Launch Checklist

## Content to collect
- [ ] GBX website URL (or decide whether to build a `/gbx` page)
- [ ] Helping Hooves URL(s) and names for the three initiatives
- [ ] Contact emails (general, press, leasing) and a mailing address
- [ ] Verified heritage copy and figures for the stat tiles
- [ ] Photos: hero (harbor / terminal), GBX, Brooklyn Equine, Helping Hooves, and 2 heritage photos. At least 2000px wide, JPG/WebP
- [ ] Family approval of the positioning line and the pull quote

## Build
- [ ] Replace every `[PLACEHOLDER]` and `href="#"` marked with `<!-- LINK: ... -->` in `site/index.html`
- [ ] Drop photos into `site/assets/` using the file names listed in `site/assets/README.md`
- [ ] Add a favicon and a 1200×630 Open Graph image (`site/assets/og.jpg`)

## Hosting (GitHub Pages, the same setup as Brooklyn Equine)
- [ ] Create a GitHub repo, push this folder, and set Settings → Pages → Source: **GitHub Actions**
- [ ] Add `site/CNAME` containing `quadrozzi.com`
- [ ] DNS at the registrar: four `A` records for the apex pointing to 185.199.108.153 / .109.153 / .110.153 / .111.153, plus `CNAME www → <user>.github.io`
- [ ] Turn on "Enforce HTTPS" once the certificate is issued

## QA
- [ ] Phone (360–414px), tablet and desktop: no horizontal scroll, menu works
- [ ] Every outbound link opens the correct venture in a new tab
- [ ] Lighthouse: Performance, Accessibility, Best Practices and SEO all 90+
- [ ] Keyboard-only navigation works with visible focus, and reduced motion is respected
- [ ] Test the social share preview (Open Graph) with the LinkedIn Post Inspector
