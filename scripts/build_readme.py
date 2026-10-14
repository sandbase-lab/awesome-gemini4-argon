#!/usr/bin/env python3
"""Generate README.md, README.zh-CN.md and per-entry prompt pages (en + zh-CN) from data/videos.json."""
import html
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
VIDEOS = json.loads((ROOT / 'data/videos.json').read_text())
COLLECTION = json.loads((ROOT / 'data/collection.json').read_text())
MODEL_ID = COLLECTION['model']['id']
UTM = 'utm_source=github&utm_medium=readme&utm_campaign=awesome-gemini4-argon'
MODEL_PAGE = f"{COLLECTION['model']['sandbasePage']}?{UTM}"
SANDBASE = f'https://www.sandbase.ai/?{UTM}'
DOCS = f'https://www.sandbase.ai/docs/?{UTM}'
KEYS = f'https://www.sandbase.ai/console/keys?{UTM}'
SANDBOX = f'https://www.sandbase.ai/landing/sandbox?{UTM}'
REPO = 'https://github.com/sandbase-lab/awesome-gemini4-argon'
SEED = COLLECTION['seed']['repository']

CATEGORIES = {
    'motion': ('Motion graphics & animation', '动画与动态图形'),
    '3d': ('3D scenes & physics', '3D 场景与物理'),
    'interactive': ('Games & interactive experiences', '游戏与交互体验'),
}

# Every user-visible string lives here, keyed by locale. `en` is the reference.
T = {
    'en': {
        'switch': 'English · [简体中文](README.zh-CN.md)',
        'tagline': 'A curated, verified collection of what people are building with **Gemini 4 Argon**: code-generated animation, 3D scenes and playable games shared on X, with creator credits, full post text and every publicly shared prompt.',
        'cta': f'**[▶ Run Gemini 4 Argon on SandBase]({MODEL_PAGE})** · one API key, OpenAI-compatible, pay per call.',
        'stats': lambda n, a, p: f'- **{n} videos** from **{a} creators**, listed in publication order within each section.\n- **{p} entries** include the creator\'s verbatim prompt; the rest say so explicitly. We never reconstruct prompts.',
        'media': '- Previews are X\'s own thumbnails. Click a preview to watch on the creator\'s original post; click a title for the full post, prompt and sources.',
        'scope': '- Finished creative work only: no model comparisons, reviews, tutorials or product walkthroughs. New submissions must be 2 minutes or shorter.',
        'verified': lambda t: f'- Every entry is re-checked against its public X post (author, Snowflake timestamp, video media ID). Last verification: `{t}`.',
        'contents': 'Contents',
        'reproduce': 'Reproduce a prompt on SandBase',
        'reproduce_body': [
            f'Gemini 4 Argon is available on SandBase as `{MODEL_ID}`. Most entries here are **code** (HTML, SVG, Canvas, three.js) that the creator rendered and recorded, so a re-run gives you code to open in a browser, not an MP4.',
            '',
            '1. Pick an entry marked **prompt** and copy its prompt into `prompt.txt`.',
            f'2. Create an API key in the [SandBase console]({KEYS}) and export it as `SANDBASE_API_KEY`.',
            '3. Call the OpenAI-compatible endpoint:',
        ],
        'reproduce_after': [
            'Open the generated `argon.html` (Markdown fences are stripped) in a browser, or run it inside a [SandBase Sandbox](' + SANDBOX + ') to keep untrusted generated code isolated. Results vary between runs and depend on the reasoning effort; check the [model page](' + MODEL_PAGE + ') for current pricing and limits.',
        ],
        'prompt_tag': 'prompt',
        'data': 'Data & verification',
        'data_items': [
            '[`data/videos.json`](data/videos.json): catalog, credits, prompts, X media links',
            '[`data/verification.json`](data/verification.json): per-entry verification result',
            '[`data/collection.json`](data/collection.json): scope, cutoff, curation policy and removals',
            '`python3 scripts/sync_x.py && python3 scripts/build_readme.py && python3 scripts/validate.py` rebuilds everything.',
        ],
        'contribute': 'Contribute',
        'contribute_body': f'Know a finished Gemini 4 Argon creation we are missing? [Submit it]({REPO}/issues/new?template=submit-video.yml) with the original X post URL. Read [CONTRIBUTING](CONTRIBUTING.md) first.',
        'credits': 'Credits & rights',
        'credits_body': [
            'All videos, prompts and quoted post text belong to their creators. The MIT license covers this repository\'s tooling and curation structure only and does not relicense third-party content. [Rights, corrections and removals](MEDIA-RIGHTS.md).',
            f'The initial catalog was seeded from [yihui-dev/awesome-gemini4-argon-videos]({SEED}) (MIT) and independently re-verified against X. Thanks to its maintainers.',
            'This community collection is not affiliated with or endorsed by Google. SandBase links are from the maintainers and do not imply creator endorsement.',
        ],
        'footer': f'Maintained by [SandBase Lab](https://github.com/sandbase-lab) · [SandBase]({SANDBASE}) · [Docs]({DOCS})',
        # prompt pages
        'back': '← Back to the collection',
        'page_switch': lambda i: f'English · [简体中文](zh-CN/{i}.md)',
        'watch': 'Watch on X',
        'raw': 'Direct video file (X CDN)',
        'credit': 'Author / credit',
        'duration': lambda d, w, h: f'Duration: {d:.0f} s · {w} × {h}',
        'published': 'Published',
        'status': 'Prompt status',
        'prompt': 'Prompt',
        'no_prompt': 'The creator did not publish an exact prompt in the sources we reviewed. The original post below is a description, **not a reconstructed prompt**.',
        'template': 'The creator shared this as a template; the exact filled-in subject or reference image was not published.',
        'prompt_source': 'Prompt source',
        'run': 'Run this prompt on SandBase',
        'run_body': f'Save the prompt above as `prompt.txt`, then follow [the reproduce steps](../README.md#reproduce). Model: `{MODEL_ID}` · [pricing & limits]({MODEL_PAGE}).',
        'original': 'Original post',
        'sources': 'Sources & attribution',
        'prompt_author': 'Prompt author',
        'model_context': 'Model attribution context',
        'additional': 'Additional post by the creator',
        'source_post': 'source post',
        'page_rights': 'Model attribution follows the creator\'s published account; it is not an audit of the generation process. The video, prompt and post text remain the property of the creator. See [media rights](../MEDIA-RIGHTS.md).',
        'try': f'[Try Gemini 4 Argon on SandBase →]({MODEL_PAGE})',
    },
    'zh-CN': {
        'switch': '[English](README.md) · 简体中文',
        'tagline': '精选并逐条核验的 **Gemini 4 Argon** 作品合集：创作者在 X 上分享的代码生成动画、3D 场景和可玩游戏，保留作者署名、帖子原文和全部公开提示词。',
        'cta': f'**[▶ 在 SandBase 上调用 Gemini 4 Argon]({MODEL_PAGE})** · 一个 API Key，兼容 OpenAI 接口，按调用计费。',
        'stats': lambda n, a, p: f'- 共 **{n} 条视频**，来自 **{a} 位创作者**；每个分类内按发布时间排列。\n- 其中 **{p} 条** 附有作者公开的原文提示词，其余条目会明确标注未公开。我们不编造或复原提示词。',
        'media': '- 预览图使用 X 自身的视频封面。点击预览图前往作者原帖观看；点击标题查看完整原文、提示词和来源。',
        'scope': '- 只收录成品作品：不收录模型对比、测评、教程或产品功能演示。新提交的视频不超过 2 分钟。',
        'verified': lambda t: f'- 每个条目都会对照公开的 X 原帖重新核验（作者、Snowflake 时间戳、视频媒体 ID）。最近一次核验：`{t}`。',
        'contents': '目录',
        'reproduce': '在 SandBase 上复现提示词',
        'reproduce_body': [
            f'Gemini 4 Argon 在 SandBase 上的模型 ID 是 `{MODEL_ID}`。这里的大部分作品是作者用模型生成**代码**（HTML、SVG、Canvas、three.js）后渲染录屏得到的，所以复现得到的是可在浏览器打开的代码，而不是 MP4。',
            '',
            '1. 选择标有 **prompt** 的条目，把提示词保存为 `prompt.txt`。',
            f'2. 在 [SandBase 控制台]({KEYS}) 创建 API Key，并导出为 `SANDBASE_API_KEY`。',
            '3. 调用兼容 OpenAI 的接口：',
        ],
        'reproduce_after': [
            '生成的 `argon.html`（已去掉 Markdown 代码围栏）可直接用浏览器打开；也可以在 [SandBase Sandbox](' + SANDBOX + ') 中运行，让不可信的生成代码保持隔离。每次结果会有差异，也取决于推理强度；当前价格和限制请以 [模型页](' + MODEL_PAGE + ') 为准。',
        ],
        'prompt_tag': 'prompt',
        'data': '数据与核验',
        'data_items': [
            '[`data/videos.json`](data/videos.json)：作品目录、署名、提示词、X 媒体链接',
            '[`data/verification.json`](data/verification.json)：逐条核验结果',
            '[`data/collection.json`](data/collection.json)：收录范围、截止时间、策展规则和移除记录',
            '运行 `python3 scripts/sync_x.py && python3 scripts/build_readme.py && python3 scripts/validate.py` 即可重新生成全部内容。',
        ],
        'contribute': '参与贡献',
        'contribute_body': f'发现了未收录的 Gemini 4 Argon 成品作品？请附上 X 原帖链接 [提交给我们]({REPO}/issues/new?template=submit-video.yml)。提交前请先阅读 [CONTRIBUTING](CONTRIBUTING.md)。',
        'credits': '致谢与权利',
        'credits_body': [
            '所有视频、提示词和引用的帖子原文归各自创作者所有。MIT 许可证只覆盖本仓库的工具和策展结构，不会重新授权第三方内容。[权利、更正与下架说明](MEDIA-RIGHTS.md)。',
            f'初始目录基于 [yihui-dev/awesome-gemini4-argon-videos]({SEED})（MIT）导入，并对照 X 独立重新核验。感谢原项目维护者。',
            '本社区合集与 Google 无隶属或背书关系。SandBase 链接由维护者添加，不代表创作者为其背书。',
        ],
        'footer': f'由 [SandBase Lab](https://github.com/sandbase-lab) 维护 · [SandBase]({SANDBASE}) · [文档]({DOCS})',
        'back': '← 返回合集',
        'page_switch': lambda i: f'[English](../{i}.md) · 简体中文',
        'watch': '在 X 上观看',
        'raw': '视频直链（X CDN）',
        'credit': '作者 / 署名',
        'duration': lambda d, w, h: f'时长：{d:.0f} 秒 · {w} × {h}',
        'published': '发布时间',
        'status': '提示词状态',
        'prompt': '提示词',
        'no_prompt': '在我们查阅的来源中，作者没有公开确切的提示词。下方原帖内容只是作品描述，**不是复原的提示词**。',
        'template': '作者以模板形式分享了这段提示词，没有公开实际填入的主题或参考图。',
        'prompt_source': '提示词来源',
        'run': '在 SandBase 上运行这段提示词',
        'run_body': f'把上面的提示词保存为 `prompt.txt`，然后按照 [复现步骤](../../README.zh-CN.md#reproduce) 操作。模型：`{MODEL_ID}` · [价格与限制]({MODEL_PAGE})。',
        'original': '帖子原文',
        'sources': '来源与署名',
        'prompt_author': '提示词作者',
        'model_context': '模型归属说明',
        'additional': '作者的补充帖子',
        'source_post': '原帖',
        'page_rights': '模型归属以作者公开说明为准，并非对生成过程的审计。视频、提示词和帖子原文归作者所有。详见 [媒体权利说明](../../MEDIA-RIGHTS.md)。',
        'try': f'[在 SandBase 上试用 Gemini 4 Argon →]({MODEL_PAGE})',
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


def fence(text: str) -> str:
    """Pick a fence longer than any backtick run inside verbatim text."""
    longest, run = 0, 0
    for ch in text:
        run = run + 1 if ch == '`' else 0
        longest = max(longest, run)
    tick = '`' * max(3, longest + 1)
    return f'{tick}text\n{text}\n{tick}'


def credit(v):
    return v.get('creatorCredit') or f"{v['author']['name']} (@{v['author']['handle']})"


def prompt_page(v, loc):
    t = T[loc]
    up = '..' if loc == 'en' else '../..'
    readme = 'README.md' if loc == 'en' else 'README.zh-CN.md'
    lines = [f'# {v["title"]}', '', t['page_switch'](v['id']), '', f'[{t["back"]}]({up}/{readme})', '',
             f'[![{html.escape(v["title"], quote=True)}]({v["thumbnailUrl"]})]({v["sourceUrl"]})', '',
             f'**[▶ {t["watch"]}]({v["sourceUrl"]})** · [{t["raw"]}]({v["videoUrl"]})', '',
             f'- {t["credit"]}: {credit(v)}',
             f'- {t["duration"](v["duration"], v["width"], v["height"])}',
             f'- {t["published"]}: `{v["publishedAt"]}`',
             f'- {t["status"]}: `{v["promptStatus"]}`']
    if v.get('note'):
        lines += ['', f'> {v["note"]}']
    lines += ['', f'## {t["prompt"]}', '']
    if v.get('prompt'):
        if v['promptStatus'] == 'verbatim_template':
            lines += [t['template'], '']
        lines += [fence(v['prompt']), '', f'{t["prompt_source"]}: {v["promptSourceUrl"]}', '',
                  f'### {t["run"]}', '', t['run_body']]
    else:
        lines.append(t['no_prompt'])
    lines += ['', f'## {t["original"]}', '', fence(v['originalPost']), '', f'## {t["sources"]}', '',
              f'- [{v["author"]["name"]}]({v["author"]["url"]}) · [{t["source_post"]}]({v["sourceUrl"]})']
    if v.get('promptAuthor'):
        lines.append(f'- {t["prompt_author"]}: {v["promptAuthor"]} · {v["promptSourceUrl"]}')
    if v.get('modelEvidenceUrl'):
        lines.append(f'- {t["model_context"]}: {v["modelEvidenceUrl"]}')
    for x in v.get('relatedSources', []):
        lines.append(f'- [{x["label"]}]({x["url"]})')
    for x in v.get('additionalPosts', []):
        lines += ['', f'### {t["additional"]} · [{t["source_post"]}]({x["url"]})', '', fence(x['text'])]
    lines += ['', t['page_rights'], '', t['try'], '']
    return '\n'.join(lines)


def card(v, loc):
    page = f'prompts/{v["id"]}.md' if loc == 'en' else f'prompts/zh-CN/{v["id"]}.md'
    alt = html.escape(v['title'], quote=True)
    tag = f' · <a href="{page}#{"prompt" if loc == "en" else "提示词"}">{T[loc]["prompt_tag"]}</a>' if v.get('prompt') else ''
    return (f'<td width="33%" valign="top"><a href="{v["sourceUrl"]}"><img src="{v["thumbnailUrl"]}" alt="{alt}" width="100%"></a>'
            f'<br><a href="{page}"><b>{html.escape(v["title"])}</b></a>'
            f'<br><sub><a href="{v["author"]["url"]}">@{v["author"]["handle"]}</a> · {v["duration"]:.0f}s{tag}</sub></td>')


def readme(loc):
    t = T[loc]
    zh = loc == 'zh-CN'
    creators = len({v['author']['handle'].lower() for v in VIDEOS})
    prompts = sum(bool(v.get('prompt')) for v in VIDEOS)
    verified_at = json.loads((ROOT / 'data/verification.json').read_text())['verifiedAt']
    lines = ['# Awesome Gemini 4 Argon', '', t['switch'], '', t['tagline'], '', t['cta'], '',
             t['stats'](len(VIDEOS), creators, prompts), t['media'], t['scope'], t['verified'](verified_at), '',
             f'## {t["contents"]}', '']
    for key, names in CATEGORIES.items():
        lines.append(f'- [{names[1] if zh else names[0]}](#{key}) ({sum(v["category"] == key for v in VIDEOS)})')
    lines += [f'- [{t["reproduce"]}](#reproduce)', f'- [{t["contribute"]}](#contribute)', '']
    for key, names in CATEGORIES.items():
        group = [v for v in VIDEOS if v['category'] == key]
        lines += [f'<a id="{key}"></a>', '', f'## {names[1] if zh else names[0]}', '', '<table>']
        for i in range(0, len(group), 3):
            lines.append('<tr>' + ''.join(card(v, loc) for v in group[i:i + 3]) + '</tr>')
        lines += ['</table>', '']
    lines += ['<a id="reproduce"></a>', '', f'## {t["reproduce"]}', '', *t['reproduce_body'], '', CURL, '', *t['reproduce_after'], '',
              f'## {t["data"]}', '', *[f'- {x}' for x in t['data_items']], '',
              '<a id="contribute"></a>', '', f'## {t["contribute"]}', '', t['contribute_body'], '',
              f'## {t["credits"]}', '']
    for p in t['credits_body']:
        lines += [p, '']
    lines += ['---', '', t['footer'], '']
    return '\n'.join(lines)


def main():
    for d in (ROOT / 'prompts', ROOT / 'prompts/zh-CN'):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
    for v in VIDEOS:
        (ROOT / 'prompts' / f'{v["id"]}.md').write_text(prompt_page(v, 'en'))
        (ROOT / 'prompts/zh-CN' / f'{v["id"]}.md').write_text(prompt_page(v, 'zh-CN'))
    (ROOT / 'README.md').write_text(readme('en'))
    (ROOT / 'README.zh-CN.md').write_text(readme('zh-CN'))
    print(f'Built {len(VIDEOS)} entries: 2 READMEs and {len(VIDEOS) * 2} prompt pages (en + zh-CN).')


if __name__ == '__main__':
    main()
