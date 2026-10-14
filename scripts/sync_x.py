#!/usr/bin/env python3
"""Verify every catalog entry against its public X post and refresh X-hosted media links.

Usage:
  python3 scripts/sync_x.py                      # verify data/videos.json
  python3 scripts/sync_x.py --seed path/to/videos.json      # import a seed catalog first

Post metadata comes from the public FxTwitter JSON API (no X login, no credentials).
Videos are NOT downloaded or re-hosted: previews use X's own thumbnail (pbs.twimg.com)
and every card links back to the creator's original post.
"""
import argparse
import concurrent.futures as cf
import datetime as dt
import json
import pathlib
import re
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
CACHE = ROOT / '.cache' / 'fx'
UA = 'awesome-gemini4-argon/1.0 (+https://github.com/sandbase-lab/awesome-gemini4-argon)'
TWITTER_EPOCH_MS = 1288834974657

# Fields kept from the seed catalog. Media URLs from the seed (third-party CDN) are dropped.
SEED_FIELDS = ['id', 'title', 'category', 'author', 'creatorCredit', 'sourceUrl', 'publishedAt', 'originalPost',
               'prompt', 'promptStatus', 'promptSourceUrl', 'promptAuthor', 'modelAttribution', 'modelEvidenceUrl',
               'note', 'relatedSources', 'additionalPosts', 'mediaId']


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def post_id(entry_id: str) -> str:
    return entry_id.split('-')[0]


def snowflake_ts(pid: str) -> float:
    return ((int(pid) >> 22) + TWITTER_EPOCH_MS) / 1000


def norm(text: str) -> str:
    """Whitespace/link-insensitive comparison; FxTwitter expands t.co links and trims media URLs."""
    text = re.sub(r'https?://\S+', '', text or '')
    return re.sub(r'\s+', ' ', text).strip()


def http_json(url: str, retries: int = 3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (404, 401, 403):
                try:
                    return e.code, json.loads(e.read())
                except Exception:
                    return e.code, None
            time.sleep(2 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    return 0, None


def http_status(url: str) -> int:
    for method in ('HEAD', 'GET'):
        try:
            req = urllib.request.Request(url, method=method, headers={'User-Agent': UA, 'Range': 'bytes=0-0'})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if method == 'GET':
                return e.code
        except Exception:
            if method == 'GET':
                return 0
    return 0


def fetch_post(pid: str, refresh: bool):
    path = CACHE / f'{pid}.json'
    if path.exists() and not refresh:
        return json.loads(path.read_text())
    status, body = http_json(f'https://api.fxtwitter.com/status/{pid}')
    record = {'status': status, 'tweet': (body or {}).get('tweet'), 'fetchedAt': now()}
    if status in (200, 404):  # cache only definitive answers
        CACHE.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record, ensure_ascii=False))
    return record


def best_mp4(media: dict):
    mp4 = [f for f in media.get('formats') or media.get('variants') or [] if f.get('container') == 'mp4' or '.mp4' in f.get('url', '')]
    mp4.sort(key=lambda f: f.get('bitrate') or 0)
    return (mp4[-1]['url'] if mp4 else media.get('url'))


def verify(entry: dict, record: dict) -> dict:
    pid = post_id(entry['id'])
    result = {'id': entry['id'], 'postId': pid, 'checkedAt': record.get('fetchedAt'), 'postStatus': record.get('status')}
    tweet = record.get('tweet')
    if record.get('status') != 200 or not tweet:
        result['decision'] = 'removed'
        result['reason'] = 'post_unavailable'
        return result
    published = tweet.get('created_timestamp')
    result['authorMatch'] = tweet['author']['screen_name'].lower() == entry['author']['handle'].lower()
    result['snowflakeMatch'] = published is not None and abs(snowflake_ts(pid) - published) < 2
    result['textMatch'] = norm(tweet.get('text')) == norm(entry['originalPost'])
    media = next((m for m in (tweet.get('media') or {}).get('all', []) if m.get('type') in ('video', 'gif') and str(m.get('id')) == str(entry['mediaId'])), None)
    result['mediaFound'] = media is not None
    if not result['authorMatch']:
        result.update(decision='removed', reason='author_mismatch')
    elif not result['snowflakeMatch']:
        result.update(decision='removed', reason='timestamp_mismatch')
    elif not media:
        result.update(decision='removed', reason='media_missing')
    else:
        result['decision'] = 'kept'
        result['media'] = {
            'thumbnailUrl': media.get('thumbnail_url'),
            'videoUrl': best_mp4(media),
            'duration': media.get('duration'),
            'width': media.get('width'),
            'height': media.get('height'),
        }
        result['publishedAt'] = dt.datetime.fromtimestamp(published, dt.timezone.utc).isoformat().replace('+00:00', 'Z')
        result['engagement'] = {k: tweet.get(k) for k in ('likes', 'retweets', 'replies', 'views')}
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', help='Import entries from a seed catalog before verifying')
    ap.add_argument('--refresh', action='store_true', help='Ignore cached FxTwitter responses')
    ap.add_argument('--workers', type=int, default=6)
    args = ap.parse_args()

    if args.seed:
        seed = json.loads(pathlib.Path(args.seed).read_text())
        catalog = [{k: v[k] for k in SEED_FIELDS if k in v} | {'seededFrom': 'yihui-dev/awesome-gemini4-argon-videos'} for v in seed]
    else:
        catalog = json.loads((DATA / 'videos.json').read_text())

    pids = sorted({post_id(v['id']) for v in catalog})
    with cf.ThreadPoolExecutor(args.workers) as pool:
        records = dict(zip(pids, pool.map(lambda p: fetch_post(p, args.refresh), pids)))

    results = [verify(v, records[post_id(v['id'])]) for v in catalog]
    kept_results = [r for r in results if r['decision'] == 'kept']
    with cf.ThreadPoolExecutor(args.workers) as pool:
        statuses = list(pool.map(lambda r: http_status(r['media']['thumbnailUrl']) if r['media']['thumbnailUrl'] else 0, kept_results))
    for r, s in zip(kept_results, statuses):
        r['thumbnailHttp'] = s
        if s not in (200, 206):
            r.update(decision='removed', reason='thumbnail_unavailable')

    by_id = {r['id']: r for r in results}
    videos, removed = [], []
    for v in catalog:
        r = by_id[v['id']]
        if r['decision'] != 'kept':
            removed.append({'id': v['id'], 'sourceUrl': v['sourceUrl'], 'reason': r['reason'], 'checkedAt': r['checkedAt']})
            continue
        m = r['media']
        v.update(publishedAt=r['publishedAt'], thumbnailUrl=m['thumbnailUrl'], videoUrl=m['videoUrl'],
                 duration=m['duration'], width=m['width'], height=m['height'])
        videos.append(v)
    videos.sort(key=lambda v: (v['publishedAt'], v['id']))

    (DATA / 'videos.json').write_text(json.dumps(videos, ensure_ascii=False, indent=1) + '\n')
    (DATA / 'verification.json').write_text(json.dumps({
        'verifiedAt': now(),
        'method': 'Each source post fetched from the public FxTwitter JSON API. Author handle, Snowflake-derived publication time (within 2 s) and the presence of the catalogued video media ID are required; thumbnails must return HTTP 200. Post text equality is recorded but not required, because FxTwitter expands links.',
        'entryCount': len(results),
        'keptCount': len(videos),
        'entries': [{k: r[k] for k in r if k != 'media'} for r in results],
    }, ensure_ascii=False, indent=1) + '\n')

    collection_path = DATA / 'collection.json'
    collection = json.loads(collection_path.read_text()) if collection_path.exists() else {}
    previous = {e['id']: e for e in collection.get('removedByVerification', [])}
    previous.update({e['id']: e for e in removed})
    collection['removedByVerification'] = sorted(previous.values(), key=lambda e: e['id'])
    collection_path.write_text(json.dumps(collection, ensure_ascii=False, indent=1) + '\n')

    reasons = {}
    for e in removed:
        reasons[e['reason']] = reasons.get(e['reason'], 0) + 1
    print(f'Verified {len(results)} entries: kept {len(videos)}, removed {len(removed)} {reasons or ""}; '
          f'text matches {sum(bool(r.get("textMatch")) for r in results)}.')


if __name__ == '__main__':
    main()
