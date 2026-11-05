#!/usr/bin/env python3
"""Build the upload packages for Quadrozzi.com (Network Solutions hosting), then delete older zips.

    python3 tools/package_zips.py

Quadrozzi-site-upload.zip          the whole site/ folder (committed files only)
Quadrozzi-under-construction.zip   the home page, its contact page and 404; every menu link opens
                                   tools/under-construction.html
Both carry an .htaccess so the host serves the site's own 404 page.
Only the 2 newest zips in the project folder are kept; any older zip there is deleted.
"""
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


def under_construction_zip():
    home = (SITE / 'index.html').read_text(encoding='utf-8')
    swaps = {
        '<a href="gbx/terminals/bbx/">': '<a href="under-construction.html?site=bbx">',
        '<a href="gbx/">': '<a href="under-construction.html?site=gbx">',
        '<a href="gbx/terminals/vbx/">': '<a href="under-construction.html?site=vbx">',
        '<a href="https://djmiddlefinger.github.io/be-brooklyn-equine/" target="_blank" rel="noopener">': '<a href="under-construction.html?site=be">',
        ' ↗<span class="sr-only"> (opens in a new tab)</span>': '',
        '<a href="helping-hooves/">': '<a href="under-construction.html?site=hhi">',
        '<a href="sponsorships/">': '<a href="under-construction.html?site=sponsorships">',
        '<a href="sponsorships/?category=Environmental">': '<a href="under-construction.html?site=sponsorships">',
        '<a href="sponsorships/?category=Arts%20%E2%80%A2%20Theater%20%E2%80%A2%20Film">': '<a href="under-construction.html?site=sponsorships">',
        '<a class="division" href="news/">': '<a class="division" href="under-construction.html?site=news">',
        '<a class="division" href="special/">': '<a class="division" href="under-construction.html?site=special">',
    }
    for old, new in swaps.items():
        assert home.count(old) == 1, f'home page menu changed; update the swaps for: {old}'
        home = home.replace(old, new)
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
