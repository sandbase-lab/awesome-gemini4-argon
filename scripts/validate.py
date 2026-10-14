#!/usr/bin/env python3
"""Offline checks: provenance, cutoff, verification coverage, generated files and bilingual parity."""
import datetime as dt
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
load = lambda name: json.loads((ROOT / 'data' / name).read_text())
videos = load('videos.json')
collection = load('collection.json')
verification = {e['id']: e for e in load('verification.json')['entries']}
cutoff = dt.datetime.fromisoformat(collection['publicationCutoffUtc'].replace('Z', '+00:00'))
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


check(videos, 'catalog is empty')
check(len({v['id'] for v in videos}) == len(videos), 'duplicate entry ids')
check(len({v['mediaId'] for v in videos}) == len(videos), 'duplicate media ids')
removed = {e['id'] for e in collection.get('removedByVerification', [])}
for v in videos:
    vid, pid = v['id'], v['id'].split('-')[0]
    published = dt.datetime.fromisoformat(v['publishedAt'].replace('Z', '+00:00'))
    check(published > cutoff, f'{vid}: published before cutoff')
    check(abs(((int(pid) >> 22) + 1288834974657) / 1000 - published.timestamp()) < 2, f'{vid}: timestamp does not match Snowflake id')
    check(pid in v['sourceUrl'] and v['sourceUrl'].startswith(f'https://x.com/{v["author"]["handle"]}/status/'), f'{vid}: bad sourceUrl')
    check(v['category'] in collection['categories'], f'{vid}: unknown category')
    check(bool(v.get('prompt')) == bool(v.get('promptSourceUrl')), f'{vid}: prompt and promptSourceUrl must go together')
    check(v['promptStatus'].startswith('verbatim') if v.get('prompt') else v['promptStatus'] == 'not_published_in_reviewed_sources', f'{vid}: inconsistent promptStatus')
    check(v['thumbnailUrl'].startswith('https://pbs.twimg.com/'), f'{vid}: thumbnail must be served by X')
    check(v['videoUrl'].startswith('https://video.twimg.com/'), f'{vid}: video link must point to X')
    check(vid not in removed, f'{vid}: re-added after removal')
    r = verification.get(vid)
    check(r and r['decision'] == 'kept' and r['authorMatch'] and r['snowflakeMatch'] and r['mediaFound'] and r['thumbnailHttp'] in (200, 206), f'{vid}: not verified')
    for loc in ('', 'zh-CN/'):
        check((ROOT / 'prompts' / f'{loc}{vid}.md').exists(), f'{vid}: missing prompts/{loc}{vid}.md')

for loc in ('', 'zh-CN/'):
    pages = {p.stem for p in (ROOT / 'prompts' / loc).glob('*.md')}
    check(pages == {v['id'] for v in videos}, f'stale or missing pages in prompts/{loc}')

forbidden = re.compile(r'/Users/|/Volumes/|media\.skillry\.dev|sk-sb-[A-Za-z0-9]{8,}')
for path in [ROOT / 'README.md', ROOT / 'README.zh-CN.md', *(ROOT / 'prompts').rglob('*.md')]:
    text = path.read_text()
    check(not forbidden.search(text), f'{path.relative_to(ROOT)}: contains a local path, third-party media host or key')
for name in ('README.md', 'README.zh-CN.md'):
    text = (ROOT / name).read_text()
    check(text.count('<td width="33%"') == len(videos), f'{name}: card count mismatch')
    check('utm_campaign=awesome-gemini4-argon' in text, f'{name}: missing SandBase CTA')

if errors:
    print('\n'.join(f'FAIL: {e}' for e in errors[:50]))
    raise SystemExit(f'{len(errors)} problem(s)')
print(f'PASS: {len(videos)} verified entries, {len(videos) * 2} prompt pages (en + zh-CN), two README walls.')
