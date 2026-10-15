# Gemini 4 Argon prompt guide: how to prompt Argon for video

English · [简体中文](zh-CN/prompt-guide.md) · [← Back to the collection](../README.md)

Gemini 4 Argon doesn't output video. It writes code (an HTML page with Three.js, Canvas or SVG), and the creator records that page playing. The patterns below come from prompts creators posted with their videos and from the fixed prompts SandBase Lab uses to test models. Each example links to the video it produced.

## 1. Say what file you want

Name the format and where it runs. The prompts that work in one shot nearly all start this way:

- "create an ultra realistic high quality, real video like animation of the solar system where the camera revolves around and gives a tour. **Single html file**" ([@analogalok][solar])
- "Build a **single-file HTML page (Three.js via CDN)** that opens into a live, interactive galaxy…" ([@Smlay_ero][galaxy])
- For SVG, ban scripts so it plays inside an `<img>`: "Use **CSS or SMIL animation only, no JavaScript**. The animation loops seamlessly." (Lab [Pelican Test][pelican])

## 2. For 3D, a style and a subject can be enough

Argon fills in a lot from a short brief when the style is clear. Voxel art is the most reliable:

- "voxel art of mercedes amg f1 car" ([@HarshithLucky3][f1-voxel])
- "Build a voxel F1 Car" ([@letdarky][f1-voxel-2])
- "build voxel art of dragon flying on temple" ([@marcthecreatorr][dragon])

Short prompts give you Argon's taste, not yours. Add detail when you need a specific result.

## 3. Describe the interaction, not just the look

Name every input and what happens on each one. Creators who listed interactions got working controls:

- "drag to tilt, shatter on click" ([@kinderlayer][cd])
- "Drag to orbit the camera, scroll to zoom in/out… zoom into a planet and it snaps to a close-up… Click a planet for a…" ([@Smlay_ero][galaxy])
- Games: list the keys. "Space or swipe up = jump. Down arrow or swipe down = slide." (Lab [Endless Runner][runner])

## 4. Set hard constraints up front

Long outputs fail in predictable ways: a missing CDN, a file cut off halfway, code that only runs on a server. Rule those out first:

- "Everything inline: no external files, fonts, images, libraries or CDNs. The file must work when opened from disk with no network connection." (Lab [Endless Runner][runner])
- "Return ONLY the complete HTML code. No markdown fences, no explanation." (same)
- "Output the complete code, don't abbreviate, don't write 'omitted here'." ([@lemomo_ai][watch], translated)
- Build textures in code and sounds with the Web Audio API, so there is nothing to load. (Lab [Watermelon Test][watermelon])

## 5. Ask for things it has to get right

Argon is at its best when the prompt has rules it must satisfy, not only a mood. [@lemomo_ai][watch] asked for a mechanical watch with at least 30 parts and real gear teeth, and said to "work out the tooth counts and gear ratios first, so the second hand turns once in 60 seconds" (translated). Correct mechanics are what make the video convincing.

Sometimes Argon adds this on its own. [@servasyy_ai][ik] gave it the bare prompt "生成一个svg动画：鹈鹕骑自行车，用H5给我展示下" ("make an SVG animation: a pelican riding a bicycle, show it in H5") and found the code solving two-bone inverse kinematics, so the feet stay locked to the pedals.

## 6. Use templates with a slot

When a prompt works, keep it and swap the subject. [@fofrAI][fourier] shared one:

> Make a slow-reveal Fourier epicycle video of [thing], make the video in the style of the attached reference image, add a cinematic soundtrack using Lyria 3.5 and sync the music.

The Lab prompts are written this way too: the brief is fixed and only the subject changes, which also makes results comparable across models.

## 7. Plan for the recording

If you want a video at the end, ask for it:

- A fixed camera move or an autoplay "tour" mode, so the page plays without a mouse ([@analogalok][solar]).
- A capture mode of fixed length. [@0xCarnagee][capture] asked for "a full Three.js game + 11s capture mode".
- State you can check. Lab's watermelon prompt makes the page set `document.body.dataset.bands` and `dataset.state = "burst"`, so a script knows when the interesting part happens.

Then record it with [`scripts/record.mjs`](../scripts/record.mjs) (see the [tutorial](tutorial.md#4-turn-the-page-into-a-video)).

## A prompt to start from

```text
Build [subject] as ONE self-contained HTML file.

Look: [style, e.g. voxel art / low-poly / cinematic PBR], [mood, lighting, palette].
Motion: [what moves and how]. Autoplay a [10]-second camera tour on load, then loop.
Interaction: [drag = …, scroll = …, click = …, keys = …].
Must be correct: [the rules that make it believable: physics, gear ratios, pedaling, collisions].

Technical:
- Use Three.js as an ES module from a CDN import map. No other libraries.
- No external images, models, fonts or audio: generate textures in code, sound with Web Audio.
- Fill the viewport, no scrolling, 60 fps on a laptop.
- Return only the complete HTML, from <!DOCTYPE html> to </html>. Do not abbreviate.
```

Try it on the [Lab text arena][arena] to run it on Argon and other models side by side, or with the API in the [tutorial](tutorial.md).

## Settings

- **Output budget.** On the Lab Pelican Test, Argon used a median of 9,436 output tokens for one SVG ([comparison](model-comparison.md)); creators report 18k to 28k for full 3D pages. Set `max_tokens` to 32,000 or more (SandBase allows up to 65,536) so the file isn't cut off.
- **Reasoning.** Creators who report their settings mostly used high reasoning in AI Studio or Antigravity.
- **One shot vs. iteration.** Most videos here are one shot. For longer pieces, creators let an agent iterate, and costs rise accordingly (see [creator-reported costs](model-comparison.md#what-creators-reported)).

For an A/B test of a minimal vs a structured prompt, with tokens and cost, see [Gemini 4 Argon prompts for creative coding](https://blog.sandbase.ai/gemini-4-argon-prompts-creative-coding-2026/?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon&utm_content=reading) on the SandBase blog.

---

Quotes are short excerpts credited to their authors; follow the links for full prompts and videos. Translations from Chinese are ours.

[solar]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110078889859203253?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[galaxy]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110361902064992440?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[f1-voxel]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110048102321365205?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[f1-voxel-2]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110093858549694597?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[dragon]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110105779294687341?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[cd]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110346627172983121?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[watch]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110187446906613901?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[ik]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110168263623938143?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[fourier]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110045963951956250?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[capture]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110082812233892193?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[pelican]: https://www.sandbase.ai/lab/pelican-test?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[runner]: https://www.sandbase.ai/lab/endless-runner?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[watermelon]: https://www.sandbase.ai/lab/watermelon-test?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[arena]: https://www.sandbase.ai/lab/x/llm-arena?models=google%2Fgemini-4-argon&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
