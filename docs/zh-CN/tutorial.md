# 教程：用 Gemini 4 Argon 做一个视频

[English](../tutorial.md) · 简体中文 · [← 返回合集](../../README.zh-CN.md)

从提示词到 MP4，四步。Argon 写出网页，你负责播放和录制。

## 1. 从喜欢的视频开始

在 [合集](../../README.zh-CN.md) 里点任意标题，进入它在 [SandBase Lab][lab] 的页面：视频、原帖，以及作者公开的提示词（如果有）。点 **复刻**，Lab 会打开文本竞技场，自动填好帖子内容并选中 Argon。登录后运行，就能拿到 HTML，并带实时预览。

作者没公开提示词？参考 [提示词写法](prompt-guide.md) 自己写一个，里面有可以直接填空的模板。

## 2. 同一提示词对比多个模型

在 [文本竞技场][arena] 里，在 Argon 旁边再加一两个模型（例如 `anthropic/claude-opus-5.5` 和 `openai/gpt-6.1-sol`），运行一次。每个模型拿到的提示词完全相同，每条结果都会显示成本和耗时。想在自己的任务上验证 [模型对比](model-comparison.md) 里的说法，这是最快的方式。

## 3. 或者调用 API

Gemini 4 Argon 在 SandBase 上的模型 ID 是 `google/gemini-4-argon`，兼容 OpenAI 接口。

1. 在 [控制台][keys] 创建 Key 并导出：`export SANDBASE_API_KEY=sk-sb-...`
2. 把提示词保存为 `prompt.txt`。
3. 运行：

```bash
jq -n --rawfile prompt prompt.txt '{
  model: "google/gemini-4-argon",
  max_tokens: 32000,
  messages: [{role: "user", content: $prompt}]
}' |
curl -sS --max-time 900 https://api.sandbase.ai/v1/chat/completions \
  -H "Authorization: Bearer $SANDBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- > response.json

jq -r '.choices[0].message.content' response.json | sed '/^```/d' > argon.html
jq '.usage' response.json
```

- `max_tokens: 32000`：完整的 3D 页面输出约 1.8 万到 2.8 万 token；上限太低，文件会在脚本中途被截断。SandBase 最高支持 65,536。
- `--max-time 900`：生成一个长页面可能要几分钟。
- `sed '/^```/d'`：去掉模型可能加上的 Markdown 代码围栏。
- `usage`：本次计费的 token 数。价格见 [模型页][model]。

用浏览器打开 `argon.html`。如果是空白页，打开开发者控制台看报错：常见原因是文件被截断（调高 `max_tokens`），或 CDN 没加载上（在提示词里要求全部内联）。

## 4. 把页面录成视频

大多数作者是直接录屏。想每次得到一样的片段，可以用 [`scripts/record.mjs`](../../scripts/record.mjs) 无头录制：

```bash
npm i -D playwright@1.56.1
npx playwright install chromium          # 或使用本机已安装的 Chrome：export RECORD_CHANNEL=chrome
node scripts/record.mjs argon.html argon.mp4 12 1920 1080   # 录 12 秒，1080p
```

脚本按指定尺寸打开页面，录制指定秒数，再用 ffmpeg 转成 H.264 MP4。想要干净的画面，就在提示词里要求自动播放的镜头导览或固定时长的录制模式（见 [提示词写法第 7 节](prompt-guide.md#7-提前为录屏做准备)），不依赖鼠标操作。

想加声音？这里有几位作者用音乐模型生成配乐，再在剪辑时对齐。[@fofrAI][fourier] 直接让 Argon 为 Lyria 3.5 写配乐提示词。

## 安全运行生成的代码

这些 HTML 是你没读过的代码。单文件页面从本地打开通常没问题，但它仍然可以加载脚本、发起网络请求。对不信任的代码，或者需要批量自动运行时，请使用 [SandBase Sandbox][sandbox]：隔离的运行环境，有时间限制，无法访问你的文件和密钥。

## 分享

把视频连同提示词发到 X，并注明 Gemini 4 Argon。想收录到这里，请 [提交作品](https://github.com/sandbase-lab/awesome-gemini4-argon/issues/new?template=submit-video.yml)；通过审核的作品会加入 Lab 合集，并在下一次每日同步时出现在本列表。

[lab]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[arena]: https://www.sandbase.ai/lab/x/llm-arena?models=google%2Fgemini-4-argon&lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[keys]: https://www.sandbase.ai/console/keys?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[model]: https://www.sandbase.ai/model/google/gemini-4-argon?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[sandbox]: https://www.sandbase.ai/landing/sandbox?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[fourier]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110045963951956250?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
