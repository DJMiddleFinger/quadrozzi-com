# quadrozzi.com

Plans and a static prototype for **quadrozzi.com**, the home of the Quadrozzi family of companies:

- **GBX — Gowanus Bay Terminal**: grain terminal / industrial waterfront property
- **Be™ Brooklyn Equine**: https://DJMiddleFinger.github.io/be-brooklyn-equine/
- **Helping Hooves**: community initiatives

## What's here
```
plans/      01-brief · 02-sitemap · 03-design-system · 04-content-outline · 05-launch-checklist
site/       index.html (one-page site), 404.html, assets/ (photo slots — see assets/README.md)
.github/    GitHub Pages deploy workflow (publishes the site/ folder)
```

## Run locally
```bash
npm start
```
Then open http://localhost:8080.

## Editing the links (the one place to change)
In `site/index.html`, scroll to the bottom `<script>` and edit the `LINKS` object:

```js
const LINKS = {
  gbx:            '',   // GBX website
  brooklynEquine: 'https://DJMiddleFinger.github.io/be-brooklyn-equine/',
  helpingHooves:  '',
  initiative1: '', initiative2: '', initiative3: '',
  linkedin: '', instagram: ''
};
```
When a value is empty, its card shows "Link coming soon". When you fill one in, every button, card and
footer link for that venture updates and opens in a new tab.

## Placeholders still to fill
Search `index.html` for `[`. That turns up the founding year, the heritage copy, the pull quote,
the initiative names, the address and the stat figures. Also confirm the three contact email addresses.

## Design
The layout is adapted from robertaspizza.com: oversized condensed uppercase headlines, a restrained
smoke/ivory palette with a single accent, divider bands, a marquee and a cascading title reveal. It's
tuned for a corporate holding company (oxblood + brass, no mascots, no preloader).
Details are in `plans/03-design-system.md`.

## Deploy
Push to a GitHub repo's `main` branch with Pages set to "GitHub Actions". See `plans/05-launch-checklist.md`
for the custom domain and DNS steps.
