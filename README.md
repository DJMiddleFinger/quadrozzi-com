# quadrozzi.com

Plans and a static prototype for **quadrozzi.com**, the home of the Quadrozzi family of companies:

- **GBX — Gowanus Bay Terminal**: its own page on this site at `/gbx/`, with the terminal's history and a booking inquiry form for film, photo, events and maritime use
- **Be™ Brooklyn Equine**: https://DJMiddleFinger.github.io/be-brooklyn-equine/
- **Helping Hooves**: community initiatives

## What's here
```
plans/      01-brief · 02-sitemap · 03-design-system · 04-content-outline · 05-launch-checklist
site/       index.html (home), gbx/index.html (GBX page), credits.html (photo licenses), 404.html
            assets/css/site.css + assets/js/site.js (shared by every page), assets/*.jpg (photos — see assets/README.md)
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

## GBX inquiry form
The form at `/gbx/#inquire` has no server. By default, pressing **Send Inquiry** opens the visitor's email app
with every answer filled in, addressed to the GBX inbox. To change where inquiries go, edit the `GBX_INQUIRY`
block at the bottom of `site/gbx/index.html`:

```js
const GBX_INQUIRY = {
  email:    'gbx@quadrozzi.com',
  endpoint: ''   // optional: a form service URL (e.g. Formspree) to receive submissions directly
};
```
Setting `endpoint` sends submissions straight to that service with no email app involved. You'll need to create
the service account yourself.

## Placeholders still to fill
Search `index.html` for `[`. That turns up the founding year, the heritage copy, the pull quote,
the initiative names, the address and the stat figures. Also confirm the three contact email addresses. On the GBX page, confirm the phone number,
the street address (699 Columbia Street, taken from press coverage) and the GBX email address.

## Design
The layout is adapted from robertaspizza.com: oversized condensed uppercase headlines, a restrained
smoke/ivory palette with a single accent, divider bands, a marquee and a cascading title reveal. It's
tuned for a corporate holding company. The colors come from the Quadrozzi truck fleet: orange cabs,
yellow drums, black lettering and hazard stripes.
Details are in `plans/03-design-system.md`.

## Deploy
Push to a GitHub repo's `main` branch with Pages set to "GitHub Actions". See `plans/05-launch-checklist.md`
for the custom domain and DNS steps.
