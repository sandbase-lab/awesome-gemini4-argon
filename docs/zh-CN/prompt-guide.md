# Gemini 4 Argon 提示词写法：如何写出能做视频的提示词

[English](../prompt-guide.md) · 简体中文 · [← 返回合集](../../README.zh-CN.md)

Gemini 4 Argon 并不直接输出视频。它写的是代码（用 Three.js、Canvas 或 SVG 做的 HTML 页面），作者再把页面播放的过程录下来。下面的写法来自创作者随视频公开的提示词，以及 SandBase Lab 测试模型时使用的固定提示词。每个例子都链接到它生成的视频。

## 1. 先说清要什么文件

写明格式和运行环境。一次成功的提示词几乎都这样开头：

- "create an ultra realistic high quality, real video like animation of the solar system where the camera revolves around and gives a tour. **Single html file**"（[@analogalok][solar]）
- "Build a **single-file HTML page (Three.js via CDN)** that opens into a live, interactive galaxy…"（[@Smlay_ero][galaxy]）
- 做 SVG 时禁用脚本，这样放进 `<img>` 也能播放："Use **CSS or SMIL animation only, no JavaScript**. The animation loops seamlessly."（Lab [Pelican Test][pelican]）

## 2. 做 3D，风格加主体有时就够了

风格明确时，Argon 能从很短的描述里补全大量细节。体素风（voxel art）最稳定：

- "voxel art of mercedes amg f1 car"（[@HarshithLucky3][f1-voxel]）
- "Build a voxel F1 Car"（[@letdarky][f1-voxel-2]）
- "build voxel art of dragon flying on temple"（[@marcthecreatorr][dragon]）

短提示词得到的是 Argon 的审美，不是你的。需要特定效果时再补细节。

## 3. 写清交互，不只写外观

列出每种操作以及操作后发生什么。列了交互的作者，拿到的控制都能用：

- "drag to tilt, shatter on click"（[@kinderlayer][cd]）
- "Drag to orbit the camera, scroll to zoom in/out… zoom into a planet and it snaps to a close-up… Click a planet for a…"（[@Smlay_ero][galaxy]）
- 游戏要写明按键："Space or swipe up = jump. Down arrow or swipe down = slide."（Lab [Endless Runner][runner]）

## 4. 把硬性约束放在前面

长输出的失败方式很固定：CDN 没加载、文件写到一半被截断、代码只能在服务器上跑。先把这些排除掉：

- "Everything inline: no external files, fonts, images, libraries or CDNs. The file must work when opened from disk with no network connection."（Lab [Endless Runner][runner]）
- "Return ONLY the complete HTML code. No markdown fences, no explanation."（同上）
- "输出完整代码，不要省略，不要写'此处略'。"（[@lemomo_ai][watch]）
- 纹理用代码生成，声音用 Web Audio API 合成，不需要加载任何文件。（Lab [Watermelon Test][watermelon]）

## 5. 给它必须做对的规则

提示词里有必须满足的规则，而不只是氛围描述时，Argon 表现最好。[@lemomo_ai][watch] 要求做一只至少 30 个部件、齿形真实的机械表，并写明"先算好各齿轮的齿数和传动比，保证秒针 60 秒一圈"。机械关系对了，视频才可信。

有时 Argon 会自己加上这类规则。[@servasyy_ai][ik] 只给了一句"生成一个svg动画：鹈鹕骑自行车，用H5给我展示下"，发现代码里写了双连杆逆运动学求解，让脚始终锁在踏板上。

## 6. 用带占位符的模板

提示词好用就留下来，只换主体。[@fofrAI][fourier] 分享过一个：

> Make a slow-reveal Fourier epicycle video of [thing], make the video in the style of the attached reference image, add a cinematic soundtrack using Lyria 3.5 and sync the music.

Lab 的提示词也是这样写的：描述固定，只换主体，这样不同模型的结果也能直接比较。

## 7. 提前为录屏做准备

想最后得到视频，就在提示词里要求：

- 固定的镜头运动或自动播放的"导览"模式，不用鼠标也能播放（[@analogalok][solar]）。
- 固定时长的录制模式。[@0xCarnagee][capture] 要求的是"a full Three.js game + 11s capture mode"。
- 可检查的状态。Lab 的西瓜提示词要求页面设置 `document.body.dataset.bands` 和 `dataset.state = "burst"`，脚本据此知道精彩部分何时发生。

然后用 [`scripts/record.mjs`](../../scripts/record.mjs) 录制（见 [教程](tutorial.md#4-把页面录成视频)）。

## 可以直接套用的模板

```text
用一个独立的 HTML 文件做出 [主体]。

外观：[风格，如体素风 / 低多边形 / 电影感 PBR]，[氛围、光照、配色]。
运动：[哪些东西怎么动]。页面加载后自动播放 [10] 秒镜头导览，然后循环。
交互：[拖动 = …，滚轮 = …，点击 = …，按键 = …]。
必须正确：[让它可信的规则：物理、齿轮传动比、踩踏板动作、碰撞]。

技术要求：
- 通过 CDN import map 以 ES 模块方式引入 Three.js，不使用其他库。
- 不加载外部图片、模型、字体或音频：纹理用代码生成，声音用 Web Audio。
- 铺满视口，不出现滚动条，在笔记本上保持 60 fps。
- 只返回完整 HTML，从 <!DOCTYPE html> 到 </html>，不要省略任何部分。
```

可以在 [Lab 文本竞技场][arena] 里让 Argon 和其他模型并排运行，或按 [教程](tutorial.md) 用 API 调用。

## 参数设置

- **输出预算。** 在 Lab Pelican Test 中，Argon 生成一张 SVG 的输出 token 中位数是 9,436（见 [模型对比](model-comparison.md)）；创作者报告完整 3D 页面用了 1.8 万到 2.8 万。把 `max_tokens` 设为 32,000 以上（SandBase 最高支持 65,536），避免文件被截断。
- **推理强度。** 公开了设置的创作者大多在 AI Studio 或 Antigravity 中使用 high 推理。
- **一次生成还是多轮迭代。** 这里的大部分视频是一次生成。较长的作品，作者会让 Agent 多轮迭代，成本也相应上升（见 [创作者报告的成本](model-comparison.md#创作者报告的结果)）。

---

引用均为简短摘录并注明作者，完整提示词和视频请点链接查看。英文提示词保留原文。

[solar]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110078889859203253?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[galaxy]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110361902064992440?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[f1-voxel]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110048102321365205?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[f1-voxel-2]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110093858549694597?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[dragon]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110105779294687341?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[cd]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110346627172983121?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[watch]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110187446906613901?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[ik]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110168263623938143?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[fourier]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110045963951956250?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[capture]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110082812233892193?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[pelican]: https://www.sandbase.ai/lab/pelican-test?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[runner]: https://www.sandbase.ai/lab/endless-runner?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[watermelon]: https://www.sandbase.ai/lab/watermelon-test?lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[arena]: https://www.sandbase.ai/lab/x/llm-arena?models=google%2Fgemini-4-argon&lang=zh-CN&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
