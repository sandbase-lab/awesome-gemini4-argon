# Gemini 4 Argon vs. other models

English · [简体中文](zh-CN/model-comparison.md) · [← Back to the collection](../README.md)

Two kinds of evidence, kept apart:

1. **What we measured.** SandBase Lab runs the same fixed prompt on every model and scores the result. Small samples, but the same conditions for everyone.
2. **What creators reported.** Head-to-heads posted on X with their own prompts, costs and times. Useful context, not verified by us.

## What we measured: Lab Pelican Test

The [Pelican Test][pelican] asks each model for an SVG of a pelican riding a bicycle, once static and once animated (wheels spin, legs pedal, CSS/SMIL only). The page is rendered to PNG and scored 0 to 5 by `google/gemini-3.8-flash` on four questions: recognizable, actually riding, a bike that works, looks good. Cost is the real billed amount on SandBase.

Snapshot from the [live leaderboard][pelican] on 2026-10-14, 20 models, 61 results:

| Rank | Model | Results | Score | Renders | Animation moves | Avg cost |
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

Full table of 20 on the [leaderboard][pelican].

Argon's two runs in detail (run by tester "david li", 2026-10-14):

| | Static | Animated |
|---|---|---|
| Score | 4.0 | 3.5 |
| Recognizable / riding / bike / looks | 4 / 4 / 4 / 4 | 4 / 3 / 3 / 4 |
| Output tokens | 10,592 | 8,281 |
| Time | 82 s | 63 s |
| Cost | $0.216 | $0.171 |
| Judge's note | "A wonderfully charming pelican pedaling smoothly on a well-constructed cruiser." | "Pedals along nicely, even if it has to balance without a saddle." |

What this says:

- **Top quality, not top value.** Argon ties for first, but GPT-6.1 Sol got the same score for about a seventh of the cost. Argon spends tokens: a median 9,436 output tokens per SVG, against 2,440 for Sol and 1,303 for Opus 5.5.
- **Slower per drawing.** Median 73 s, against 14 s for Opus 5.5 and 50 s for Sol.
- **Strongest at looks and recognizability** (4/4 on both runs). The animated run lost points on structure: no saddle.
- **Sample size.** Two results for Argon. Treat the rank as "in the top group", not a final order. [Run it yourself][pelican-run] to add results.

The other Lab code tests, [Endless Runner][runner] (a canvas game) and [Watermelon Test][watermelon] (a Three.js toy), don't have Argon results yet.

## What creators reported

Same-prompt comparisons posted on X. Numbers are as the creator stated them: different tools (AI Studio, Antigravity, Devin, CLI), different discounts, often one run. Click through to watch both results.

| Creator | Task | Argon | Other model | Creator's verdict |
|---|---|---|---|---|
| [@shownotover][burgers] | 15 s Three.js short, aliens at a burger stand | ~8–10 min, ~27.6K tokens, ~$0.92 | Opus 5.5: 31m54s, 5.35M tokens, ~$6.63 | Argon ~3x faster; prefers Opus's visuals |
| [@0xRhinoX][jar] | Firefly jar you can open | $0.19, 8 min | Opus 5.5: $15.00, 64 min | Opus far better ("real glass, moonlight") |
| [@remoteugur][civ] | Civilization sim, stone age to future | 18 min, ~$1.7 | Opus 5.5: 94 min, ~$25 | Asks viewers |
| [@realbrucemartin][deck] | Roguelike deck-builder, one HTML file (Devin) | 56 min, ~$1.75, 6.5M in / 109K out | SWE-2 Max: 89 min | Argon wrote 3x the code, 33 min faster |
| [@Adidotdev][quota] | Same prompt, motion graphics | 10 min, ~1.5% weekly quota | Opus 5.5: 15 min, 4% | — |
| [@dpratyush02][house] | Japanese house with cherry blossoms | — | GPT-6.1 Sol | Argon "absolutely nailed it" |
| [@marcthecreatorr][dragon] | Voxel dragon over a temple | — | GPT-6 Astra | Argon clearly ahead in 3D |
| [@0xShoopy][five] | 5 prompts, 4 models | Won writing | Opus 5.5 won 3D and game; Astra won homepage | Opus ahead on visuals |
| [@yash_yk45][earth] | Motion design, Earth's beauty | — | Opus 5.5 | Opus better |
| [@EvoLinkAi][voxel] | Voxel art world | — | Opus 5.5 | Opus better |

Solo Argon runs with reported cost:

| Creator | Task | Reported |
|---|---|---|
| [@analogalok][solar] | Solar system tour, single HTML | 28.5K output tokens (high reasoning), $0.28 |
| [@analogalok][forest] | Navigable forest | 27K tokens, $0.27 |
| [@SidraMiconi][lowpoly] | Low-poly Three.js scene, third try | 363 in, 6,387 thinking, 18,359 out; $0.25, 4.4 min |
| [@nex_ify][jelly] | 3D game "Jelly Jet Takeoff" | 11m6s, $1.16 |
| [@exploraX_][ski] | Animated ski-resort website | Over 1 hour, ~$7 at 50% off |

The pattern across both sources: a one-shot Argon page costs cents to about a dollar and takes minutes. Opus 5.5 is often preferred on visual polish but, in these agent setups, took several times longer and cost 7x to 80x more.

## Rerun before you trust a comparison

Two creators found viral Argon comparisons they couldn't reproduce. [@MiaAI_lab][gummy] reran a "gummy bear" prompt and got a much better Argon result than the video showed; [@xueyu1125][boss] reran a boss-fight prompt in Devin and couldn't get near the posted quality, and suspects the clip was edited with a video model. Run the prompt yourself: paste it into the [Lab text arena][arena] with two or three models selected, or see the [tutorial](tutorial.md).

---

Lab data: [Pelican Test][pelican], snapshot 2026-10-14. Creator data: their posts, linked; not independently verified.

[pelican]: https://www.sandbase.ai/lab/pelican-test?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[pelican-run]: https://www.sandbase.ai/lab/pelican-test?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon&utm_content=run
[runner]: https://www.sandbase.ai/lab/endless-runner?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[watermelon]: https://www.sandbase.ai/lab/watermelon-test?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[arena]: https://www.sandbase.ai/lab/x/llm-arena?models=google%2Fgemini-4-argon&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[burgers]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110274182046953661?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[jar]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110382089476407630?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[civ]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110155062664188395?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[deck]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110228350337687773?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[quota]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110047989280670072?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[house]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110347694447509797?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[dragon]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110105779294687341?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[five]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110075670332412079?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[earth]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110085876135112729?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[voxel]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110377592394031397?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[solar]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110078889859203253?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[forest]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110071798629036542?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[lowpoly]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110231429523309050?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[jelly]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110232072405065889?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[ski]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110285214102511672?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[gummy]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110363640213979398?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[boss]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110343586781000107?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
