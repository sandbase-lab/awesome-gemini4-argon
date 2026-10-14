#!/usr/bin/env python3
"""Offline checks on the Lab snapshot and the generated READMEs."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
videos = json.loads((ROOT / 'data/videos.json').read_text())
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


check(videos, 'catalog is empty')
check(len({v['id'] for v in videos}) == len(videos), 'duplicate post ids')
for v in videos:
    vid = v['id']
    check(re.fullmatch(r'\d+', vid), f'{vid}: bad id')
    check(v['postUrl'].startswith('https://x.com/') and vid in v['postUrl'], f'{vid}: postUrl must be the original X post')
    check(v['labUrl'] == f'https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/{vid}', f'{vid}: bad labUrl')
    check(v['title'] and v['title_zh'], f'{vid}: missing title')
    check((ROOT / 'previews' / f'{vid}.webp').exists(), f'{vid}: missing animated preview')
    check(v['mp4'].startswith('https://www.sandbase.ai/lab/media/x/gemini-4-argon/'), f'{vid}: video must be served by Lab')
    check('likes' not in v and 'views' not in v, f'{vid}: volatile counters must not be stored')
    if v['poster']:
        check(v['poster'].startswith('https://www.sandbase.ai/lab/media/x/gemini-4-argon/'), f'{vid}: poster must come from Lab R2')

featured = sum(v['featured'] is not None for v in videos)
check({p.stem for p in (ROOT / 'previews').glob('*.webp')} == {v['id'] for v in videos}, 'stale previews')
forbidden = re.compile(r'/Users/|/Volumes/|sk-sb-[A-Za-z0-9]{8,}')
for name, lang in (('README.md', ''), ('README.zh-CN.md', 'lang=zh-CN&')):
    text = (ROOT / name).read_text()
    check(text.count('<td width="33%"') == len(videos) + featured, f'{name}: card count mismatch')
    for v in videos:
        check(f'{v["labUrl"]}?{lang}utm_source=github' in text, f'{name}: {v["id"]} does not link to its Lab page')
    check(not forbidden.search(text), f'{name}: contains a local path or key')

if errors:
    print('\n'.join(f'FAIL: {e}' for e in errors[:50]))
    raise SystemExit(f'{len(errors)} problem(s)')
print(f'PASS: {len(videos)} posts ({featured} featured), every card links to SandBase Lab in both READMEs.')
