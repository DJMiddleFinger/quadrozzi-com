# quadrozzi.com

### 👉 [Visit the live site: djmiddlefinger.github.io/quadrozzi-com](https://djmiddlefinger.github.io/quadrozzi-com/)

| Site | Link |
|---|---|
| **Home** (Q logo face page + menu) | https://djmiddlefinger.github.io/quadrozzi-com/ |
| GBX Gowanus Bay Terminal | https://djmiddlefinger.github.io/quadrozzi-com/gbx/ |
| Be™ Brooklyn Equine | https://DJMiddleFinger.github.io/be-brooklyn-equine/ |
| Helping Hooves | https://djmiddlefinger.github.io/quadrozzi-com/helping-hooves/ |

The home page is a single no-scroll face page: the Q logo, plus a four-bar menu button that opens the
full company menu (independent expand/collapse sections; live sites open in a new tab; the contact line
lives at the bottom of the menu). GBX and Helping Hooves are standalone sites that live in this repo;
they share `site/assets/` (styles, script, photos) but each has its own nav, footer and photo credits.
Helping Hooves deliberately carries no Quadrozzi branding or affiliation wording; its only contact is
info@quadrozzi.com. Check with `grep -i quadrozzi site/helping-hooves/*.html` before publishing changes.

## What's here
```
plans/      01-brief · 02-sitemap · 03-design-system · 04-content-outline · 05-launch-checklist
site/       index.html (home), gbx/ and helping-hooves/ (each with its own credits.html), 404.html
            assets/q-logo.jpg (home), assets/css/site.css + assets/js/site.js + photos (GBX & Helping Hooves)
tools/      credits.json + build_credits.py (rebuilds both credits pages)
.github/    GitHub Pages deploy workflow (publishes the site/ folder)
```

## Run locally
```bash
npm start
```
Then open http://localhost:8080.

## Forms (GBX booking, Helping Hooves get-involved)
The site has no server, so by default pressing **Send** opens the visitor's email app with every answer
filled in. Each page sets where its messages go in a `window.INQUIRY` block near the bottom of the file:

| Page | File | Default inbox |
|---|---|---|
| GBX booking | `site/gbx/index.html` | gbx@quadrozzi.com (placeholder, confirm) |
| Helping Hooves | `site/helping-hooves/index.html` | info@quadrozzi.com |

```js
window.INQUIRY = {
  email:    'gbx@quadrozzi.com',
  endpoint: '',   // optional: a form service URL (e.g. Formspree) to receive submissions directly
  subject:  'GBX inquiry'
};
```
Setting `endpoint` sends submissions straight to that service with no email app involved. You'll need to
create the service account yourself. The shared form code lives in `site/assets/js/site.js`.

**Donations:** the Helping Hooves page also has a `HOOVES.donate` setting. Put an online donation page there
(PayPal, Givebutter, Stripe and so on) and every "Donate" link goes to it. While it's empty, "Donate" opens the
get-involved form with Donate selected.

## Photo credits
Most photos come from Wikimedia Commons (CC0, public domain or CC BY-SA). Each one is listed with its author
and license in `tools/credits.json`. After adding or replacing a photo, update that file and run:
```bash
python3 tools/build_credits.py
```
This rewrites `site/gbx/credits.html` and `site/helping-hooves/credits.html` (photos with "hooves" in their
path go on the Helping Hooves page), which are linked from each site's footer and meet the attribution
requirement of the CC BY-SA photos.

## Placeholders still to fill
- **GBX:** the phone number, the GBX email, and the street address (699 Columbia Street, taken from press coverage)
- **Helping Hooves:** add a donation link, and swap stand-in photos for the stable's own (see `plans/05-launch-checklist.md`)

## Design
The layout is adapted from robertaspizza.com: oversized condensed uppercase headlines, a restrained
smoke/ivory palette with a single accent, divider bands, a marquee and a cascading title reveal. It's
tuned for a corporate holding company. The colors come from the Quadrozzi truck fleet: orange cabs,
yellow drums, black lettering and hazard stripes.
Details are in `plans/03-design-system.md`.

## Deploy
Every push to `main` republishes the site through GitHub Pages (Actions). See `plans/05-launch-checklist.md`
for the custom domain and DNS steps.
