#!/usr/bin/env python3
"""Rebuild site/credits.html from tools/credits.json.

Add or edit an entry in credits.json whenever a photo is added or replaced, then run:
    python3 tools/build_credits.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
credits = json.loads((ROOT / 'tools' / 'credits.json').read_text())
e = html.escape


def display_title(title):
    stem, dot, ext = title.rpartition('.')
    return stem if dot and ext.lower() in ('jpg', 'jpeg', 'png', 'tif', 'tiff') else title


rows = []
for c in credits:
    lic = (f'<a href="{e(c["license_url"])}" target="_blank" rel="noopener">{e(c["license"])}</a>'
           if c.get('license_url') else e(c['license']))
    byline = lic if c['license'].startswith('Courtesy') else f'By {e(c["artist"])} · {lic}'
    rows.append(f'''        <li class="credit">
          <img src="{e(c["file"])}" alt="" loading="lazy">
          <div>
            <span class="used">{e(c["used"])}</span>
            <h3><a href="{e(c["source"])}" target="_blank" rel="noopener">{e(display_title(c["title"]))}</a></h3>
            <p>{byline}</p>
          </div>
        </li>''')

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Photo Credits — Quadrozzi</title>
  <meta name="description" content="Photo credits and licenses for images used on quadrozzi.com.">
  <meta name="theme-color" content="#161616">
  <script>document.documentElement.classList.add('js');</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@800&family=Big+Shoulders+Display:wght@700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/site.css">
  <style>
    .site-header {{ background: var(--smoke); }}
    .credits {{ padding-top: calc(72px + clamp(3rem, 7vw, 5rem)); }}
    .credits h1 {{ font-size: clamp(3rem, 9vw, 6.5rem); line-height: .86; margin: .9rem 0 1.25rem; }}
    .credits .intro {{ color: var(--stone); max-width: 60ch; margin-bottom: 2.5rem; }}
    .credit-list {{ list-style: none; border-top: 1px solid var(--smoke); }}
    .credit {{ display: grid; grid-template-columns: 120px minmax(0, 1fr); gap: 1.25rem; align-items: center; padding: 1.1rem 0; border-bottom: 1px solid var(--line); }}
    .credit img {{ width: 120px; aspect-ratio: 4 / 3; object-fit: cover; background: var(--line); }}
    .credit .used {{ font-size: .7rem; font-weight: 600; letter-spacing: .16em; text-transform: uppercase; color: var(--orange-ink); }}
    .credit h3 {{ font-family: var(--sans); text-transform: none; font-size: 1rem; font-weight: 600; line-height: 1.35; margin: .25rem 0; overflow-wrap: anywhere; }}
    .credit h3 a:hover, .credit p a:hover {{ color: var(--orange-ink); }}
    .credit p {{ font-size: .9rem; color: var(--stone); }}
    .credit p a {{ text-decoration: underline; text-underline-offset: 3px; }}
    @media (max-width: 600px) {{ .credit {{ grid-template-columns: 84px minmax(0, 1fr); }} .credit img {{ width: 84px; }} }}
  </style>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header is-solid" id="header">
    <nav class="nav container" aria-label="Primary">
      <a href="./" class="wordmark" aria-label="Quadrozzi — home"><span class="mark" aria-hidden="true"></span>Quadrozzi</a>
      <a href="./" class="btn btn-ghost btn-sm">← Home</a>
    </nav>
  </header>

  <main id="main">
    <section class="credits">
      <div class="container">
        <span class="eyebrow">Image Licensing</span>
        <h1>Photo Credits</h1>
        <p class="intro">Most photographs on this site come from Wikimedia Commons and are used under the licenses listed below. Public-domain images from the Historic American Engineering Record and other collections are courtesy of the Library of Congress. Select a title to see the original file and its full license.</p>
        <ul class="credit-list">
{chr(10).join(rows)}
        </ul>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-legal">
        <span>© <span id="year">2026</span> Quadrozzi. All rights reserved.</span>
        <span><a href="./">Home</a> · <a href="gbx/">GBX</a> · <a href="helping-hooves/">Helping Hooves</a></span>
      </div>
    </div>
  </footer>
  <script src="assets/js/site.js"></script>
</body>
</html>
'''

(ROOT / 'site' / 'credits.html').write_text(page)
print(f'Wrote site/credits.html with {len(credits)} credits')
