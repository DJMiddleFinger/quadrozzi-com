"""Build site/assets/data/news.json Sponsorship entries from the portfolio text export (soffice --convert-to txt).
Usage: python tools/import_sponsorships.py portfolio.txt"""
import json, re, sys
lines = open(sys.argv[1], encoding='utf-8', errors='replace').read().splitlines()
start = next(i for i, l in enumerate(lines) if l.strip() == '- Sponsorships')
end = next(i for i, l in enumerate(lines) if i > start and l.strip() == '- Collegiate Studios')
out, org, sub = [], None, ''
for l in lines[start + 1:end]:
    t = l.strip()
    if not t: continue
    indent = len(l) - len(l.lstrip())
    m = re.match(r'^[?-]\s*((?:19|20)\d\d)\s+(.+)$', t)
    if m:
        if org:
            title = m.group(2).strip().rstrip('.:').strip()
            out.append(dict(type='Sponsorship', date=f'{m.group(1)}-01-01', name=org,
                            title=(sub + ': ' if sub else '') + title))
    elif t.startswith('?') and indent <= 8:
        txt = t.lstrip('? ').strip()
        org = re.split(r'\s+-\s*', txt)[0].strip(' .')
        org = re.sub(r',? Red Hook Brooklyn$|\s*\(formally[^)]*\)', '', org)
        sub = ''
    elif t.startswith('?') and indent > 8:
        sub = re.split(r'\s+-\s+', t.lstrip('? ').strip())[0].strip()
        if not sub: sub = ''
json.dump(out, open('site/assets/data/news.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'entries', len({e['name'] for e in out}), 'organizations')
