#!/usr/bin/env python3
"""Generate README.md and README.zh-CN.md from data/videos.json (pulled from SandBase Lab)."""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
VIDEOS = json.loads((ROOT / 'data/videos.json').read_text())
SYNC = json.loads((ROOT / 'data/sync.json').read_text())
MODEL_ID = 'google/gemini-4-argon'
UTM = 'utm_source=github&utm_medium=readme&utm_campaign=awesome-gemini4-argon'
LAB = 'https://www.sandbase.ai/lab/ai-videos/gemini-4-argon'
MODEL_PAGE = f'https://www.sandbase.ai/model/google/gemini-4-argon?{UTM}'
KEYS = f'https://www.sandbase.ai/console/keys?{UTM}'
SANDBOX = f'https://www.sandbase.ai/landing/sandbox?{UTM}'
REPO = 'https://github.com/sandbase-lab/awesome-gemini4-argon'

# Labels mirror shared/ai-videos.ts VIDEO_CATEGORIES in the Lab repo.
CATEGORIES = {
    '3d-scene': ('3D scenes', '3D 场景'),
    'motion-graphics': ('Motion graphics', '动效'),
    'game': ('Games', '游戏'),
    'ui-demo': ('Product UI', '产品界面'),
    'particles': ('Particles & shapes', '粒子与形状'),
    'data-viz': ('Charts & diagrams', '图表图解'),
    'kinetic-type': ('Kinetic type', '文字动效'),
    'explainer': ('Explainers', '讲解'),
    'launch-film': ('Launch films', '发布片'),
    'short-film': ('Short films', '短片'),
    'music-video': ('Music videos', '音乐视频'),
    'anime': ('Anime', '动画'),
    'action': ('Action', '动作'),
    'ad': ('Ads', '广告'),
    'comparison': ('Tests & comparisons', '测试对比'),
    'showcase': ('Model showcases', '模型展示'),
}


def lab(path='', loc='en', content=None):
    q = ('lang=zh-CN&' if loc == 'zh-CN' else '') + UTM + (f'&utm_content={content}' if content else '')
    return f'{LAB}{path}?{q}'


T = {
    'en': {
        'switch': 'English · [简体中文](README.zh-CN.md)',
        'tagline': 'What people are making with **Google Gemini 4 Argon**, collected from X and credited to their creators: Three.js scenes, canvas animations, motion graphics and playable games, all written as code from a prompt.',
        'cta': lambda: f'**[▶ Watch them all on SandBase Lab]({lab(loc="en", content="hero")})** · full-size playback, the original post and prompt, and one click to recreate any video with Gemini 4 Argon.',
        'stats': lambda n, a, p: f'- **{n} videos** from **{a} creators**, newest last in each section. **{p}** of them come with the creator\'s prompt.',
        'synced': lambda t: f'- Synced daily from SandBase Lab. Lab list updated `{t}`.',
        'how': '- Click a preview to open the video. Click a title for the post, the prompt and a one-click **Recreate** on SandBase Lab. **@handle** links to the original post on X.',
        'contents': 'Contents',
        'featured': 'Featured',
        'recreate': 'Recreate one with Gemini 4 Argon',
        'recreate_body': [
            f'Gemini 4 Argon writes these videos as code. Every video page on [SandBase Lab]({lab(loc="en", content="recreate")}) has a **Recreate** button that sends the post to Argon and gives you the code back to play in the browser.',
            '',
            f'Prefer the API? Argon is `{MODEL_ID}` on SandBase. Put a prompt in `prompt.txt`, create a key in the [console]({KEYS}), and run:',
        ],
        'recreate_after': f'Open `argon.html` in a browser, or run it in a [SandBase Sandbox]({SANDBOX}) to keep generated code isolated. Pricing and limits: [model page]({MODEL_PAGE}).',
        'prompt_tag': 'prompt',
        'more': lambda n: f'**[See all {n} on SandBase Lab →]({lab(loc="en", content="section")})**',
        'contribute': 'Suggest a video',
        'contribute_body': f'Know a Gemini 4 Argon creation that should be here? [Open a submission]({REPO}/issues/new?template=submit-video.yml) with the original X post. Accepted posts are added on SandBase Lab and show up here on the next daily sync.',
        'credits': 'Credits & rights',
        'credits_body': [
            'Every video, prompt and post belongs to its creator. Cards credit the author and link to the original post. The MIT license covers this repository\'s scripts only. To correct a credit or remove a video, see [MEDIA-RIGHTS](MEDIA-RIGHTS.md).',
            'Not affiliated with or endorsed by Google.',
        ],
        'footer': f'Maintained by [SandBase Lab](https://www.sandbase.ai/lab/?{UTM}) · [All AI video collections](https://www.sandbase.ai/lab/ai-videos?{UTM})',
    },
    'zh-CN': {
        'switch': '[English](README.md) · 简体中文',
        'tagline': '收录 X 上的 **Google Gemini 4 Argon** 精选作品，并注明作者：Three.js 场景、Canvas 动画、动效和可玩游戏，全部由模型根据提示词写成代码。',
        'cta': lambda: f'**[▶ 在 SandBase Lab 观看全部作品]({lab(loc="zh-CN", content="hero")})** · 大屏播放、查看原帖和提示词，一键用 Gemini 4 Argon 复刻任意视频。',
        'stats': lambda n, a, p: f'- 共 **{n} 条视频**，来自 **{a} 位创作者**，每个分类内按发布时间排列；其中 **{p} 条** 附有作者的提示词。',
        'synced': lambda t: f'- 每天从 SandBase Lab 自动同步。Lab 列表更新时间：`{t}`。',
        'how': '- 点击预览图直接打开视频；点击标题前往 SandBase Lab 查看原帖、提示词，并一键 **复刻**；**@作者** 链接到 X 原帖。',
        'contents': '目录',
        'featured': '精选',
        'recreate': '用 Gemini 4 Argon 复刻',
        'recreate_body': [
            f'Gemini 4 Argon 用代码写出这些视频。[SandBase Lab]({lab(loc="zh-CN", content="recreate")}) 的每个视频页都有 **复刻** 按钮，会把帖子内容发给 Argon，返回可在浏览器直接播放的代码。',
            '',
            f'想用 API？Argon 在 SandBase 上的模型 ID 是 `{MODEL_ID}`。把提示词写进 `prompt.txt`，在 [控制台]({KEYS}) 创建 Key，然后运行：',
        ],
        'recreate_after': f'用浏览器打开 `argon.html`，或在 [SandBase Sandbox]({SANDBOX}) 中运行，让生成的代码保持隔离。价格与限制见 [模型页]({MODEL_PAGE})。',
        'prompt_tag': '提示词',
        'more': lambda n: f'**[在 SandBase Lab 查看全部 {n} 条 →]({lab(loc="zh-CN", content="section")})**',
        'contribute': '推荐作品',
        'contribute_body': f'发现了应该收录的 Gemini 4 Argon 作品？附上 X 原帖 [提交给我们]({REPO}/issues/new?template=submit-video.yml)。通过后会先加入 SandBase Lab，下一次每日同步时出现在这里。',
        'credits': '致谢与权利',
        'credits_body': [
            '所有视频、提示词和帖子归作者所有。每张卡片都注明作者并链接原帖。MIT 许可证只覆盖本仓库的脚本。更正署名或下架视频请见 [MEDIA-RIGHTS](MEDIA-RIGHTS.md)。',
            '与 Google 无隶属或背书关系。',
        ],
        'footer': f'由 [SandBase Lab](https://www.sandbase.ai/lab/?lang=zh-CN&{UTM}) 维护 · [全部 AI 视频合集](https://www.sandbase.ai/lab/ai-videos?lang=zh-CN&{UTM})',
    },
}

CURL = '''```bash
jq -n --rawfile prompt prompt.txt \\
  '{model: "%s", messages: [{role: "user", content: $prompt}]}' |
curl -sS https://api.sandbase.ai/v1/chat/completions \\
  -H "Authorization: Bearer $SANDBASE_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d @- | jq -r '.choices[0].message.content' | sed '/^```/d' > argon.html
```''' % MODEL_ID


def length(ms):
    if not ms:
        return None
    s = round(ms / 1000)
    return f'{s // 60}:{s % 60:02d}'


def card(v, loc):
    title = v['title_zh'] if loc == 'zh-CN' else v['title']
    page = lab(f'/{v["id"]}', loc, 'card')
    alt = html.escape(title, quote=True)
    # The animated preview opens the video file itself (served by Lab); the title opens the Lab page.
    picture = f'<a href="{v["mp4"]}"><img src="previews/{v["id"]}.webp" alt="{alt}" width="100%"></a><br>'
    meta = [f'<a href="{v["postUrl"]}">@{html.escape(v["author"]["handle"])}</a>']
    if length(v['durationMs']):
        meta.append(length(v['durationMs']))
    if v['promptShared']:
        meta.append(f'<a href="{page}">{T[loc]["prompt_tag"]}</a>')
    return (f'<td width="33%" valign="top">{picture}<a href="{page}"><b>{html.escape(title)}</b></a>'
            f'<br><sub>{" · ".join(meta)}</sub></td>')


def table(group, loc):
    rows = ['<table>']
    for i in range(0, len(group), 3):
        rows.append('<tr>' + ''.join(card(v, loc) for v in group[i:i + 3]) + '</tr>')
    return rows + ['</table>']


def readme(loc):
    t = T[loc]
    zh = loc == 'zh-CN'
    creators = len({v['author']['handle'].lower() for v in VIDEOS})
    lines = ['# Awesome Gemini 4 Argon', '', t['switch'], '', t['tagline'], '', t['cta'](), '',
             t['stats'](len(VIDEOS), creators, sum(v['promptShared'] for v in VIDEOS)),
             t['synced'](SYNC['labSyncedAt']), t['how'], '']
    cats = sorted({v['category'] for v in VIDEOS}, key=lambda c: (list(CATEGORIES).index(c) if c in CATEGORIES else 99, c))
    featured = sorted((v for v in VIDEOS if v['featured'] is not None), key=lambda v: v['featured'])
    name = lambda c: CATEGORIES.get(c, (c, c))[1 if zh else 0]
    lines += [f'## {t["contents"]}', '']
    if featured:
        lines.append(f'- [{t["featured"]}](#featured) ({len(featured)})')
    lines += [f'- [{name(c)}](#{c}) ({sum(v["category"] == c for v in VIDEOS)})' for c in cats]
    lines += [f'- [{t["recreate"]}](#recreate)', f'- [{t["contribute"]}](#contribute)', '']
    if featured:
        lines += ['<a id="featured"></a>', '', f'## {t["featured"]}', '', *table(featured, loc), '']
    for c in cats:
        group = [v for v in VIDEOS if v['category'] == c]
        lines += [f'<a id="{c}"></a>', '', f'## {name(c)}', '', *table(group, loc), '']
    lines += [t['more'](len(VIDEOS)), '',
              '<a id="recreate"></a>', '', f'## {t["recreate"]}', '', *t['recreate_body'], '', CURL, '', t['recreate_after'], '',
              '<a id="contribute"></a>', '', f'## {t["contribute"]}', '', t['contribute_body'], '',
              f'## {t["credits"]}', '']
    for p in t['credits_body']:
        lines += [p, '']
    lines += ['---', '', t['footer'], '']
    return '\n'.join(lines)


def main():
    (ROOT / 'README.md').write_text(readme('en'))
    (ROOT / 'README.zh-CN.md').write_text(readme('zh-CN'))
    print(f'Built two READMEs with {len(VIDEOS)} cards each.')


if __name__ == '__main__':
    main()
