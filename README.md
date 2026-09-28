# quadrozzi.com

Plans and a static site for **quadrozzi.com**, the home of the Quadrozzi family of companies:

- **GBX — Gowanus Bay Terminal**: its own page at `/gbx/`, with the terminal's history and a booking inquiry form for film, photo, events and maritime use
- **Be™ Brooklyn Equine**: https://DJMiddleFinger.github.io/be-brooklyn-equine/
- **Helping Hooves**: its own page at `/helping-hooves/`, covering the family's community work with horses (second-career horses, therapeutic riding, youth programs, compost for Red Hook gardens), with a get-involved form. It's run by **Helping Hoof, Inc.**, a 501(c)(3) nonprofit (EIN 88-3328025).

## What's here
```
plans/      01-brief · 02-sitemap · 03-design-system · 04-content-outline · 05-launch-checklist
site/       index.html (home), gbx/ (GBX page), helping-hooves/ (Helping Hooves page),
            credits.html (photo licenses), 404.html
            assets/css/site.css + assets/js/site.js (shared by every page), photos in assets/ (see assets/README.md)
tools/      credits.json + build_credits.py (rebuilds credits.html)
.github/    GitHub Pages deploy workflow (publishes the site/ folder)
```

## Run locally
```bash
npm start
```
Then open http://localhost:8080.

## Links on the home page
In `site/index.html`, scroll to the bottom `<script>` and edit the `LINKS` object. Any element with
`data-link="key"` picks up its address from there. Addresses on this site (like `gbx/`) open in the same tab,
and outside sites open in a new tab. An empty value shows "Link coming soon" on its card.

## Forms (GBX booking, Helping Hooves get-involved)
The site has no server, so by default pressing **Send** opens the visitor's email app with every answer
filled in. Each page sets where its messages go in a `window.INQUIRY` block near the bottom of the file:

| Page | File | Default inbox |
|---|---|---|
| GBX booking | `site/gbx/index.html` | gbx@quadrozzi.com (placeholder, confirm) |
| Helping Hooves | `site/helping-hooves/index.html` | Be@Quadrozzi.com (the stable's published address) |

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
This rewrites `site/credits.html`, which is linked from every page's footer and meets the attribution
requirement of the CC BY-SA photos.

## Placeholders still to fill
- **Home:** the founding year in the hero ("Est. [Year]"), the family-origins heritage paragraph, the office address, and confirmation of the info@ / press@ addresses
- **GBX:** the phone number, the GBX email, and the street address (699 Columbia Street, taken from press coverage)
- **Helping Hooves:** confirm the inbox, add a donation link, and swap stand-in photos for the stable's own (see `plans/05-launch-checklist.md`)

## Design
The layout is adapted from robertaspizza.com: oversized condensed uppercase headlines, a restrained
smoke/ivory palette with a single accent, divider bands, a marquee and a cascading title reveal. It's
tuned for a corporate holding company. The colors come from the Quadrozzi truck fleet: orange cabs,
yellow drums, black lettering and hazard stripes.
Details are in `plans/03-design-system.md`.

## Deploy
Every push to `main` republishes the site through GitHub Pages (Actions). See `plans/05-launch-checklist.md`
for the custom domain and DNS steps.
