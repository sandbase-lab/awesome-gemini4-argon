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


DOC_UTM = 'utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon'
ARENA = 'https://www.sandbase.ai/lab/x/llm-arena?models=google%2Fgemini-4-argon'
PELICAN = 'https://www.sandbase.ai/lab/pelican-test'
VISIBLE = 6  # cards per category shown before "show all"


def arena(loc):
    return f'{ARENA}&{"lang=zh-CN&" if loc == "zh-CN" else ""}{UTM}&utm_content=quickstart'


T = {
    'en': {
        'h1': 'Awesome Gemini 4 Argon',
        'switch': 'English · [简体中文](README.zh-CN.md)',
        'tagline': 'A curated list of **Gemini 4 Argon examples**: videos, prompts and demos made with Google\'s Gemini 4 Argon model. Three.js and WebGL 3D scenes, SVG and canvas animation, motion graphics and playable browser games, each one written as code from a prompt, credited to its creator and linked to the original post.',
        'alt': 'Awesome Gemini 4 Argon: videos, prompts, tutorial and model comparison',
        'stats': lambda n, a, p: f'**{n} videos** from **{a} creators** · **{p}** with the creator\'s prompt · synced daily from [SandBase Lab]({lab(loc="en", content="stats")})',
        'start': 'Start here',
        'start_rows': lambda: [
            ('Watch the videos', f'[Browse by category](#contents) below, or [play them full-size on SandBase Lab]({lab(loc="en", content="quickstart")})'),
            ('Copy a prompt', '[Prompt index](docs/prompts.md): every video that comes with its prompt'),
            ('Write your own prompt', '[Prompt guide](docs/prompt-guide.md): 7 patterns and a fill-in template'),
            ('Make a video', '[Tutorial](docs/tutorial.md): prompt → HTML → MP4, with the API and a recording script'),
            ('Pick a model', '[Gemini 4 Argon vs. Claude Opus 5.5, GPT-6 and others](docs/model-comparison.md)'),
            ('Try it now', f'[Run Gemini 4 Argon in the Lab arena]({arena("en")}), next to other models'),
        ],
        'goal': 'I want to…', 'where': 'Go to',
        'how': 'Click a preview to play the video. Click a title for the post, the prompt and **Recreate** on SandBase Lab. **@handle** links to the creator\'s post on X.',
        'contents': 'Contents',
        'featured': 'Featured',
        'show_all': lambda n: f'Show all {n}',
        'recreate': 'Recreate a video with Gemini 4 Argon',
        'recreate_body': [
            f'Every video page on [SandBase Lab]({lab(loc="en", content="recreate")}) has a **Recreate** button: it sends the post to Gemini 4 Argon and returns the code, ready to play in the browser.',
            '',
            f'With the API, Gemini 4 Argon is `{MODEL_ID}` on SandBase (OpenAI-compatible). Put a prompt in `prompt.txt`, create a key in the [console]({KEYS}), and run:',
        ],
        'recreate_after': f'Open `argon.html` in a browser, or run it in a [SandBase Sandbox]({SANDBOX}) to keep generated code isolated. Full walkthrough: [tutorial](docs/tutorial.md). Pricing: [model page]({MODEL_PAGE}).',
        'prompt_tag': 'prompt',
        'more': lambda n: f'**[See all {n} on SandBase Lab →]({lab(loc="en", content="section")})**',
        'faq': 'FAQ',
        'faq_items': [
            ('What is Gemini 4 Argon?', 'Google\'s flagship reasoning model and the first of the Gemini 4 generation, generally available since October 13, 2026. It takes text, image, video, audio and PDF input with a 1M-token context window.'),
            ('How are these Gemini 4 Argon videos made?', 'Argon doesn\'t render video. It writes a web page (HTML with Three.js, WebGL, Canvas or SVG), and the creator records the page playing. See the [tutorial](docs/tutorial.md).'),
            ('Where do I find the prompt for a video?', 'Videos tagged **prompt** come with the creator\'s prompt on their Lab page. The [prompt index](docs/prompts.md) lists all of them.'),
            ('How do I write a good Gemini 4 Argon prompt?', 'Ask for one self-contained HTML file, describe the interaction, put hard constraints up front and leave room for 30K+ output tokens. Details and a template: [prompt guide](docs/prompt-guide.md).'),
            ('How do I use the Gemini 4 Argon API?', f'On SandBase the model id is `{MODEL_ID}` on the OpenAI-compatible `/v1/chat/completions` endpoint. One key works for every model. See [Recreate](#recreate) and the [model page]({MODEL_PAGE}).'),
            ('Is Gemini 4 Argon better than Claude Opus 5.5 or GPT-6?', f'On the Lab [Pelican Test]({PELICAN}?{DOC_UTM}) it ties for first with GPT-6 Astra and GPT-6.1 Sol, at a higher cost per drawing. Creators often prefer Opus 5.5 for visual polish but report Argon several times faster and cheaper. Numbers: [model comparison](docs/model-comparison.md).'),
            ('How much does one video cost?', 'Creators report a few cents to about $1 for a one-shot page, more when an agent iterates for an hour. Argon averaged $0.19 per SVG on the Lab Pelican Test.'),
            ('Can I reuse these videos?', 'No, not by default. They belong to their creators. See [MEDIA-RIGHTS](MEDIA-RIGHTS.md).'),
        ],
        'contribute': 'Suggest a video',
        'contribute_body': f'Know a Gemini 4 Argon creation that should be here? [Open a submission]({REPO}/issues/new?template=submit-video.yml) with the original X post. Accepted posts are added on SandBase Lab and show up here on the next daily sync. If this list helped you, a ⭐ helps others find it.',
        'credits': 'Credits & rights',
        'credits_body': [
            'Every video, prompt and post belongs to its creator. Cards credit the author and link to the original post. The MIT license covers this repository\'s scripts only. To correct a credit or remove a video, see [MEDIA-RIGHTS](MEDIA-RIGHTS.md).',
            'Not affiliated with or endorsed by Google.',
        ],
        'footer': f'Maintained by [SandBase Lab](https://www.sandbase.ai/lab/?{UTM}) · [All AI video collections](https://www.sandbase.ai/lab/ai-videos?{UTM})',
        # prompt index
        'p_title': 'Gemini 4 Argon prompts',
        'p_switch': 'English · [简体中文](zh-CN/prompts.md) · [← Back to the collection](../README.md)',
        'p_intro': lambda n: f'{n} Gemini 4 Argon videos whose creators shared the prompt. Open one to read the prompt, watch the video and **Recreate** it with Argon on SandBase Lab. New to prompting Argon? Start with the [prompt guide](prompt-guide.md).',
        'p_cols': ('Video', 'Creator', 'Length', 'Prompt & video'),
        'p_open': 'Open',
    },
    'zh-CN': {
        'h1': 'Awesome Gemini 4 Argon',
        'switch': '[English](README.md) · 简体中文',
        'tagline': '精选 **Gemini 4 Argon 案例**合集：用 Google Gemini 4 Argon 模型做出的视频、提示词和演示。包括 Three.js / WebGL 3D 场景、SVG 与 Canvas 动画、动效和可在浏览器里玩的游戏，每一个都是模型根据提示词写成的代码，均注明作者并链接原帖。',
        'alt': 'Awesome Gemini 4 Argon：视频、提示词、教程和模型对比',
        'stats': lambda n, a, p: f'共 **{n} 条视频**，来自 **{a} 位创作者** · **{p} 条**附作者提示词 · 每天从 [SandBase Lab]({lab(loc="zh-CN", content="stats")}) 同步',
        'start': '从这里开始',
        'start_rows': lambda: [
            ('看视频', f'在下方 [按分类浏览](#contents)，或 [在 SandBase Lab 大屏播放]({lab(loc="zh-CN", content="quickstart")})'),
            ('复制提示词', '[提示词索引](docs/zh-CN/prompts.md)：所有附带提示词的视频'),
            ('自己写提示词', '[提示词写法](docs/zh-CN/prompt-guide.md)：7 条写法和一个填空模板'),
            ('做一个视频', '[教程](docs/zh-CN/tutorial.md)：提示词 → HTML → MP4，含 API 调用和录屏脚本'),
            ('选模型', '[Gemini 4 Argon 对比 Claude Opus 5.5、GPT-6 等模型](docs/zh-CN/model-comparison.md)'),
            ('马上试试', f'[在 Lab 竞技场运行 Gemini 4 Argon]({arena("zh-CN")})，和其他模型并排对比'),
        ],
        'goal': '我想…', 'where': '去这里',
        'how': '点击预览图播放视频；点击标题前往 SandBase Lab 查看原帖、提示词，并一键 **复刻**；**@作者** 链接到 X 原帖。',
        'contents': '目录',
        'featured': '精选',
        'show_all': lambda n: f'展开全部 {n} 条',
        'recreate': '用 Gemini 4 Argon 复刻视频',
        'recreate_body': [
            f'[SandBase Lab]({lab(loc="zh-CN", content="recreate")}) 的每个视频页都有 **复刻** 按钮：把帖子内容发给 Gemini 4 Argon，返回可在浏览器直接播放的代码。',
            '',
            f'用 API 的话，Gemini 4 Argon 在 SandBase 上的模型 ID 是 `{MODEL_ID}`（兼容 OpenAI）。把提示词写进 `prompt.txt`，在 [控制台]({KEYS}) 创建 Key，然后运行：',
        ],
        'recreate_after': f'用浏览器打开 `argon.html`，或在 [SandBase Sandbox]({SANDBOX}) 中运行，让生成的代码保持隔离。完整步骤见 [教程](docs/zh-CN/tutorial.md)，价格见 [模型页]({MODEL_PAGE})。',
        'prompt_tag': '提示词',
        'more': lambda n: f'**[在 SandBase Lab 查看全部 {n} 条 →]({lab(loc="zh-CN", content="section")})**',
        'faq': '常见问题',
        'faq_items': [
            ('Gemini 4 Argon 是什么？', 'Google 的旗舰推理模型，也是 Gemini 4 系列的第一个模型，2026 年 10 月 13 日正式开放。支持文本、图片、视频、音频和 PDF 输入，上下文窗口 100 万 token。'),
            ('这些 Gemini 4 Argon 视频是怎么做出来的？', 'Argon 并不直接渲染视频。它写出一个网页（用 Three.js、WebGL、Canvas 或 SVG 的 HTML），作者再把页面播放过程录下来。见 [教程](docs/zh-CN/tutorial.md)。'),
            ('在哪里找到视频的提示词？', '标有 **提示词** 的视频，其 Lab 页面上有作者的提示词。[提示词索引](docs/zh-CN/prompts.md) 列出了全部。'),
            ('怎么写好 Gemini 4 Argon 提示词？', '要求输出一个独立的 HTML 文件，写清交互，把硬性约束放在前面，并给足 3 万以上的输出 token。详细写法和模板见 [提示词写法](docs/zh-CN/prompt-guide.md)。'),
            ('怎么调用 Gemini 4 Argon API？', f'在 SandBase 上模型 ID 是 `{MODEL_ID}`，使用兼容 OpenAI 的 `/v1/chat/completions` 接口，一个 Key 调用所有模型。见 [复刻](#recreate) 和 [模型页]({MODEL_PAGE})。'),
            ('Gemini 4 Argon 比 Claude Opus 5.5 或 GPT-6 更强吗？', f'在 Lab [Pelican Test]({PELICAN}?lang=zh-CN&{DOC_UTM}) 中，它与 GPT-6 Astra、GPT-6.1 Sol 并列第一，但单张成本更高。创作者常认为 Opus 5.5 的画面更精致，但 Argon 快好几倍、便宜得多。数据见 [模型对比](docs/zh-CN/model-comparison.md)。'),
            ('做一个视频要花多少钱？', '创作者报告一次生成一个页面从几美分到 1 美元左右；让 Agent 迭代一小时会更贵。在 Lab Pelican Test 中，Argon 每张 SVG 平均 $0.19。'),
            ('可以转用这些视频吗？', '默认不可以，视频归作者所有。见 [MEDIA-RIGHTS](MEDIA-RIGHTS.md)。'),
        ],
        'contribute': '推荐作品',
        'contribute_body': f'发现了应该收录的 Gemini 4 Argon 作品？附上 X 原帖 [提交给我们]({REPO}/issues/new?template=submit-video.yml)。通过后会先加入 SandBase Lab，下一次每日同步时出现在这里。觉得有用的话，点个 ⭐ 能让更多人看到。',
        'credits': '致谢与权利',
        'credits_body': [
            '所有视频、提示词和帖子归作者所有。每张卡片都注明作者并链接原帖。MIT 许可证只覆盖本仓库的脚本。更正署名或下架视频请见 [MEDIA-RIGHTS](MEDIA-RIGHTS.md)。',
            '与 Google 无隶属或背书关系。',
        ],
        'footer': f'由 [SandBase Lab](https://www.sandbase.ai/lab/?lang=zh-CN&{UTM}) 维护 · [全部 AI 视频合集](https://www.sandbase.ai/lab/ai-videos?lang=zh-CN&{UTM})',
        'p_title': 'Gemini 4 Argon 提示词',
        'p_switch': '[English](../prompts.md) · 简体中文 · [← 返回合集](../../README.zh-CN.md)',
        'p_intro': lambda n: f'共 {n} 条 Gemini 4 Argon 视频，作者公开了提示词。打开即可查看提示词、观看视频，并在 SandBase Lab 上用 Argon 一键 **复刻**。第一次写 Argon 提示词？先看 [提示词写法](prompt-guide.md)。',
        'p_cols': ('视频', '作者', '时长', '提示词与视频'),
        'p_open': '打开',
    },
}

CURL = '''```bash
jq -n --rawfile prompt prompt.txt \\
  '{model: "%s", max_tokens: 32000, messages: [{role: "user", content: $prompt}]}' |
curl -sS --max-time 900 https://api.sandbase.ai/v1/chat/completions \\
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
    prompts = sum(v['promptShared'] for v in VIDEOS)
    cats = sorted({v['category'] for v in VIDEOS}, key=lambda c: (list(CATEGORIES).index(c) if c in CATEGORIES else 99, c))
    featured = sorted((v for v in VIDEOS if v['featured'] is not None), key=lambda v: v['featured'])
    name = lambda c: CATEGORIES.get(c, (c, c))[1 if zh else 0]
    badges = ' '.join([
        '[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)',
        f'[![Videos](https://img.shields.io/badge/videos-{len(VIDEOS)}-blue)](#contents)',
        f'[![Prompts](https://img.shields.io/badge/prompts-{prompts}-green)]({"docs/zh-CN/prompts.md" if zh else "docs/prompts.md"})',
        f'[![Sync](https://github.com/sandbase-lab/awesome-gemini4-argon/actions/workflows/sync.yml/badge.svg)](https://github.com/sandbase-lab/awesome-gemini4-argon/actions/workflows/sync.yml)',
        f'[![Run on SandBase](https://img.shields.io/badge/run%20on-SandBase-black)]({MODEL_PAGE})',
    ])
    lines = [f'# {t["h1"]}', '', t['switch'], '', badges, '',
             f'[![{t["alt"]}](assets/banner.png)]({lab(loc=loc, content="banner")})', '',
             t['tagline'], '', t['stats'](len(VIDEOS), creators, prompts), '',
             f'## {t["start"]}', '', f'| {t["goal"]} | {t["where"]} |', '|---|---|',
             *[f'| {a} | {b} |' for a, b in t['start_rows']()], '',
             '<a id="contents"></a>', '', f'## {t["contents"]}', '']
    if featured:
        lines.append(f'- [{t["featured"]}](#featured) ({len(featured)})')
    lines += [f'- [{name(c)}](#{c}) ({sum(v["category"] == c for v in VIDEOS)})' for c in cats]
    lines += [f'- [{t["recreate"]}](#recreate)', f'- [{t["faq"]}](#faq)', f'- [{t["contribute"]}](#contribute)', '', t['how'], '']
    if featured:
        lines += ['<a id="featured"></a>', '', f'## {t["featured"]}', '', *table(featured, loc), '']
    for c in cats:
        group = [v for v in VIDEOS if v['category'] == c]
        lines += [f'<a id="{c}"></a>', '', f'## {name(c)}', '', *table(group[:VISIBLE], loc), '']
        if len(group) > VISIBLE:
            lines += ['<details>', f'<summary><b>{t["show_all"](len(group))}</b></summary>', '', *table(group[VISIBLE:], loc), '', '</details>', '']
    lines += [t['more'](len(VIDEOS)), '',
              '<a id="recreate"></a>', '', f'## {t["recreate"]}', '', *t['recreate_body'], '', CURL, '', t['recreate_after'], '',
              '<a id="faq"></a>', '', f'## {t["faq"]}', '']
    for q, a in t['faq_items']:
        lines += [f'### {q}', '', a, '']
    lines += ['<a id="contribute"></a>', '', f'## {t["contribute"]}', '', t['contribute_body'], '', f'## {t["credits"]}', '']
    for p in t['credits_body']:
        lines += [p, '']
    lines += ['---', '', t['footer'], '']
    return '\n'.join(lines)


def prompt_index(loc):
    t = T[loc]
    zh = loc == 'zh-CN'
    rows = [v for v in VIDEOS if v['promptShared']]
    lines = [f'# {t["p_title"]}', '', t['p_switch'], '', t['p_intro'](len(rows)), '']
    for c in sorted({v['category'] for v in rows}, key=lambda c: (list(CATEGORIES).index(c) if c in CATEGORIES else 99, c)):
        group = [v for v in rows if v['category'] == c]
        lines += [f'## {CATEGORIES.get(c, (c, c))[1 if zh else 0]} ({len(group)})', '',
                  '| ' + ' | '.join(t['p_cols']) + ' |', '|---|---|---|---|']
        for v in group:
            title = (v['title_zh'] if zh else v['title']).replace('|', '\\|')
            lines.append(f'| {title} | [@{v["author"]["handle"]}]({v["postUrl"]}) | {length(v["durationMs"]) or "—"} | '
                         f'[{t["p_open"]}]({lab("/" + v["id"], loc, "prompt-index").replace(UTM, DOC_UTM)}) |')
        lines.append('')
    return '\n'.join(lines)


def main():
    (ROOT / 'README.md').write_text(readme('en'))
    (ROOT / 'README.zh-CN.md').write_text(readme('zh-CN'))
    (ROOT / 'docs/prompts.md').write_text(prompt_index('en'))
    (ROOT / 'docs/zh-CN/prompts.md').write_text(prompt_index('zh-CN'))
    print(f'Built two READMEs with {len(VIDEOS)} cards each.')


if __name__ == '__main__':
    main()
