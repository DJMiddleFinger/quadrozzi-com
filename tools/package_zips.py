#!/usr/bin/env python3
"""Build the upload packages for Quadrozzi.com (Network Solutions hosting), then delete older zips.

    python3 tools/package_zips.py

Quadrozzi-site-upload.zip          the whole site/ folder (committed files only)
Quadrozzi-under-construction.zip   the home page, its contact page and 404; every menu division is a
                                   button (no dropdowns) that opens tools/under-construction.html
Both carry an .htaccess so the host serves the site's own 404 page.
Only the 2 newest zips in the project folder are kept; any older zip there is deleted.
"""
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
HTACCESS = 'ErrorDocument 404 /404.html\n'


def site_zip():
    files = subprocess.run(['git', 'ls-files', 'site'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    with zipfile.ZipFile(ROOT / 'Quadrozzi-site-upload.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(ROOT / f, f.removeprefix('site/'))
        z.writestr('.htaccess', HTACCESS)


def under_construction_home(home):
    """The home page with every menu division as a plain button to the under construction page."""
    def button(name):
        return f'<a class="division" href="under-construction.html?site={name.lower().replace(" ", "-")}">{name}</a>'

    home = re.sub(r'<details>\s*<summary class="division">(.+?)</summary>.*?</details>',
                  lambda m: f'<div>{button(m[1])}</div>', home, flags=re.S)
    home = re.sub(r'<a class="division" href="[^"]*">(.+?)</a>', lambda m: button(m[1]), home)
    # Nothing in the menu may lead anywhere but the under construction page, except Contact us
    menu = re.search(r'<nav class="menu".*?</nav>', home, re.S)[0]
    links = re.findall(r'href="([^"]*)"', menu)
    assert '<details' not in menu and links, 'home page menu changed; update under_construction_home'
    assert all(link.startswith('under-construction.html?site=') or link == 'contact/' for link in links), links
    return home


def under_construction_zip():
    home = under_construction_home((SITE / 'index.html').read_text(encoding='utf-8'))
    with zipfile.ZipFile(ROOT / 'Quadrozzi-under-construction.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('index.html', home)
        z.write(ROOT / 'tools' / 'under-construction.html', 'under-construction.html')
        z.write(SITE / 'contact' / 'index.html', 'contact/index.html')
        z.write(SITE / '404.html', '404.html')
        z.write(SITE / 'assets' / 'q-logo.jpg', 'assets/q-logo.jpg')
        z.write(SITE / 'assets' / 'js' / 'truck-intro.js', 'assets/js/truck-intro.js')
        z.write(SITE / 'assets' / 'truck.bin', 'assets/truck.bin')
        z.writestr('.htaccess', HTACCESS)


def keep_newest(n=2):
    zips = sorted(ROOT.glob('*.zip'), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in zips[n:]:
        old.unlink()
        print(f'Deleted {old.name}')


if __name__ == '__main__':
    site_zip()
    under_construction_zip()
    keep_newest()
    for z in sorted(ROOT.glob('*.zip')):
        print(f'{z.name}  {z.stat().st_size // 1024} KB')
