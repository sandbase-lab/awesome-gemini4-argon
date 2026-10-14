# Gemini 4 Argon 对比 Claude Opus 5.5、GPT-6 等模型

[English](../model-comparison.md) · 简体中文 · [← 返回合集](../../README.zh-CN.md)

两类证据，分开呈现：

1. **我们实测的。** SandBase Lab 对每个模型使用同一个固定提示词并打分。样本小，但所有模型条件相同。
2. **创作者报告的。** 创作者在 X 上发布的同提示词对比，提示词、成本和耗时都是他们自己的。可作参考，我们没有核实。

## 我们实测的：Lab Pelican Test

[Pelican Test][pelican] 让每个模型画一张"鹈鹕骑自行车"的 SVG，静态一次、动画一次（轮子转、腿踩踏板，只能用 CSS/SMIL）。页面渲染成 PNG 后，由 `google/gemini-3.8-flash` 按四项打 0 到 5 分：认得出、真的在骑、车结构合理、好看。成本是 SandBase 上的实际扣费。

以下为 2026-10-14 [实时榜单][pelican] 的快照，共 20 个模型、61 条结果：

| 排名 | 模型 | 结果数 | 得分 | 能渲染 | 动画真的在动 | 平均成本 |
|---|---|---|---|---|---|---|
| 1 | **google/gemini-4-argon** | 2 | **3.75** | 100% | 100% | $0.193 |
| 1 | openai/gpt-6-astra | 4 | 3.75 | 100% | 100% | $0.134 |
| 1 | openai/gpt-6.1-sol | 4 | 3.75 | 100% | 100% | $0.028 |
| 4 | google/gemini-3.7-flash | 4 | 3.56 | 100% | 100% | $0.081 |
| 5 | anthropic/claude-opus-5.5 | 4 | 3.38 | 100% | 100% | $0.110 |
| 6 | openai/gpt-6-luna | 2 | 3.25 | 100% | 100% | $0.006 |
| 7 | anthropic/claude-sonnet-5.5 | 2 | 3.13 | 100% | 100% | $0.017 |
| 7 | deepseek/deepseek-v4.1-flash | 2 | 3.13 | 100% | 100% | $0.017 |
| 9 | moonshotai/kimi-k3 | 4 | 3.06 | 100% | 100% | $0.031 |
| 18 | google/gemini-3.8-flash | 2 | 1.75 | 50% | 0% | $0.092 |

完整 20 个模型见 [榜单][pelican]。

Argon 两次运行的明细（测试者 "david li"，2026-10-14）：

| | 静态 | 动画 |
|---|---|---|
| 得分 | 4.0 | 3.5 |
| 认得出 / 在骑 / 车 / 好看 | 4 / 4 / 4 / 4 | 4 / 3 / 3 / 4 |
| 输出 token | 10,592 | 8,281 |
| 耗时 | 82 秒 | 63 秒 |
| 成本 | $0.216 | $0.171 |
| 评委点评 | "A wonderfully charming pelican pedaling smoothly on a well-constructed cruiser." | "Pedals along nicely, even if it has to balance without a saddle."（没画车座） |

结论：

- **质量第一梯队，性价比不是。** Argon 并列第一，但 GPT-6.1 Sol 拿到同样分数，成本约为 Argon 的七分之一。Argon 很费 token：每张 SVG 输出中位数 9,436 个，Sol 是 2,440，Opus 5.5 是 1,303。
- **单张更慢。** 中位耗时 73 秒，Opus 5.5 是 14 秒，Sol 是 50 秒。
- **外观和辨识度最强**（两次都是 4/4）。动画那次在结构上扣了分：没画车座。
- **样本量。** Argon 只有两条结果，排名应理解为"在第一梯队"，而不是最终名次。欢迎 [自己跑一次][pelican-run] 补充结果。

Lab 另外两个代码测试 [Endless Runner][runner]（Canvas 游戏）和 [Watermelon Test][watermelon]（Three.js 玩具）暂时还没有 Argon 的结果。

## 创作者报告的结果

以下是创作者在 X 上发布的同提示词对比。数字均按作者原话：使用的工具不同（AI Studio、Antigravity、Devin、CLI），折扣不同，通常只跑了一次。点击链接可以观看两边的结果。

| 作者 | 任务 | Argon | 对比模型 | 作者结论 |
|---|---|---|---|---|
| [@shownotover][burgers] | 15 秒 Three.js 短片：外星人买汉堡 | 约 8–10 分钟，约 2.76 万 token，约 $0.92 | Opus 5.5：31 分 54 秒，535 万 token，约 $6.63 | Argon 快约 3 倍；更喜欢 Opus 的画面 |
| [@0xRhinoX][jar] | 可以打开的萤火虫罐 | $0.19，8 分钟 | Opus 5.5：$15.00，64 分钟 | Opus 好得多（"真实的玻璃、月光"） |
| [@remoteugur][civ] | 从石器时代到未来的文明模拟 | 18 分钟，约 $1.7 | Opus 5.5：94 分钟，约 $25 | 让观众评判 |
| [@realbrucemartin][deck] | Roguelike 卡牌构筑游戏，单 HTML（Devin） | 56 分钟，约 $1.75，650 万输入 / 10.9 万输出 | SWE-2 Max：89 分钟 | Argon 代码量是 3 倍，快 33 分钟 |
| [@Adidotdev][quota] | 同一提示词，动效 | 10 分钟，约 1.5% 周额度 | Opus 5.5：15 分钟，4% | — |
| [@dpratyush02][house] | 樱花环绕的日式房屋 | — | GPT-6.1 Sol | Argon "absolutely nailed it" |
| [@marcthecreatorr][dragon] | 体素风巨龙飞越神庙 | — | GPT-6 Astra | Argon 在 3D 上明显领先 |
| [@0xShoopy][five] | 5 个提示词、4 个模型 | 赢了写作 | Opus 5.5 赢了 3D 和游戏；Astra 赢了首页设计 | 视觉上 Opus 领先 |
| [@yash_yk45][earth] | 展示地球之美的动效视频 | — | Opus 5.5 | Opus 更好 |
| [@EvoLinkAi][voxel] | 体素风世界 | — | Opus 5.5 | Opus 更好 |

只跑 Argon 并报告了成本的作品：

| 作者 | 任务 | 报告数据 |
|---|---|---|
| [@analogalok][solar] | 太阳系导览，单 HTML | 2.85 万输出 token（high 推理），$0.28 |
| [@analogalok][forest] | 可漫游的森林 | 2.7 万 token，$0.27 |
| [@SidraMiconi][lowpoly] | 低多边形 Three.js 场景，第三次尝试 | 输入 363，思考 6,387，输出 18,359；$0.25，4.4 分钟 |
| [@nex_ify][jelly] | 3D 游戏 "Jelly Jet Takeoff" | 11 分 6 秒，$1.16 |
| [@exploraX_][ski] | 滑雪场动画网站 | 超过 1 小时，五折后约 $7 |

两类数据呈现的规律：Argon 一次生成一个页面，成本从几美分到 1 美元左右，耗时几分钟。Opus 5.5 在视觉打磨上常被认为更好，但在这些 Agent 场景里耗时长好几倍，成本高 7 到 80 倍。

## 相信对比之前，先自己跑一遍

有两位作者发现爆火的 Argon 对比视频无法复现。[@MiaAI_lab][gummy] 重跑"软糖熊"提示词，Argon 的结果比视频里好得多；[@xueyu1125][boss] 在 Devin 中重跑 Boss 战提示词，远达不到视频里的精细度，并怀疑原视频经过视频模型处理。请自己跑一遍：把提示词贴进 [Lab 文本竞技场][arena]，同时选两三个模型，或参考 [教程](tutorial.md)。

---

Lab 数据：[Pelican Test][pelican]，2026-10-14 快照。创作者数据：见各自帖子链接，未经独立核实。

[pelican]: https://www.sandbase.ai/lab/pelican-test?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[pelican-run]: https://www.sandbase.ai/lab/pelican-test?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon&utm_content=run
[runner]: https://www.sandbase.ai/lab/endless-runner?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[watermelon]: https://www.sandbase.ai/lab/watermelon-test?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[arena]: https://www.sandbase.ai/lab/x/llm-arena?models=google%2Fgemini-4-argon&lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[burgers]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110274182046953661?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[jar]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110382089476407630?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[civ]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110155062664188395?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[deck]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110228350337687773?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[quota]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110047989280670072?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[house]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110347694447509797?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[dragon]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110105779294687341?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[five]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110075670332412079?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[earth]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110085876135112729?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[voxel]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110377592394031397?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[solar]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110078889859203253?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[forest]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110071798629036542?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[lowpoly]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110231429523309050?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[jelly]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110232072405065889?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[ski]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110285214102511672?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[gummy]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110363640213979398?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[boss]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110343586781000107?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
