# Contributing

English · [简体中文](#简体中文)

Submit an original X post URL through the [submission form](https://github.com/sandbase-lab/awesome-gemini4-argon/issues/new?template=submit-video.yml) or a pull request.

An entry is eligible when:

- It is a finished creative work (animation, 3D scene, playable game, interactive piece) that the creator says was made with Gemini 4 Argon.
- The original post was published strictly after `2026-10-13T16:00:00Z`, checked against the post's Snowflake ID.
- The video is 120 seconds or shorter.
- It is not a model comparison, review, explainer, tutorial, production walkthrough or product demo.
- The credit goes to the original creator, never to a reposting account.

Prompts are copied verbatim from the creator's public posts or linked sources, with the source URL. Do not paraphrase, translate or reconstruct a prompt. If no exact prompt is public, set `prompt` to `null` and `promptStatus` to `not_published_in_reviewed_sources`.

Do not commit downloaded videos or credentials. Media is linked from X, not re-hosted.

After editing `data/videos.json`:

```bash
python3 scripts/sync_x.py        # verify against X and refresh thumbnails / media links
python3 scripts/build_readme.py  # regenerate READMEs and prompt pages
python3 scripts/validate.py
```

`README.md`, `README.zh-CN.md` and everything under `prompts/` are generated. Edit the data or the scripts, not the output.

## 简体中文

通过 [提交表单](https://github.com/sandbase-lab/awesome-gemini4-argon/issues/new?template=submit-video.yml) 或 Pull Request 提交 X 原帖链接。

收录条件：

- 成品创作（动画、3D 场景、可玩游戏、交互作品），且作者本人说明使用 Gemini 4 Argon 制作。
- 原帖发布时间严格晚于 `2026-10-13T16:00:00Z`，以帖子的 Snowflake ID 核对。
- 视频不超过 120 秒。
- 不是模型对比、测评、讲解、教程、制作过程或产品演示。
- 署名必须归属原作者，不能归属转发账号。

提示词必须从作者公开的帖子或链接来源中原文照录，并附来源链接。不要改写、翻译或复原提示词。若没有公开的确切提示词，`prompt` 设为 `null`，`promptStatus` 设为 `not_published_in_reviewed_sources`。

不要提交下载的视频或任何凭据。媒体只链接到 X，不做转存。

修改 `data/videos.json` 后依次运行上面的三条命令。`README.md`、`README.zh-CN.md` 和 `prompts/` 下的文件均为自动生成，请修改数据或脚本，不要直接改生成结果。
