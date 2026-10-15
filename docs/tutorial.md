# Gemini 4 Argon tutorial: from prompt to video

English · [简体中文](zh-CN/tutorial.md) · [← Back to the collection](../README.md)

From a prompt to an MP4 in four steps. Argon writes a web page; you play it and record it.

## 1. Start from a video you like

Open any title in the [collection](../README.md) to reach its page on [SandBase Lab][lab]: the video, the original post and, when the creator shared one, the prompt. Press **Recreate**. Lab opens the text arena with the post loaded and Argon selected. Sign in, run it, and you get the HTML back, with a live preview.

No prompt shared? Write one with the [prompt guide](prompt-guide.md). It has a fill-in template.

## 2. Compare models on the same prompt

In the [text arena][arena], add one or two more models next to Argon (for example `anthropic/claude-opus-5.5` and `openai/gpt-6.1-sol`) and run once. Every model gets the same words, and each result shows its cost and time. That's the quickest way to check a claim from the [comparison page](model-comparison.md) on your own task.

## 3. Or call the API

Gemini 4 Argon is `google/gemini-4-argon` on SandBase, OpenAI-compatible.

1. Create a key in the [console][keys] and export it: `export SANDBASE_API_KEY=sk-sb-...`
2. Save your prompt as `prompt.txt`.
3. Run:

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

- `max_tokens: 32000`: full 3D pages run 18K to 28K output tokens; a low limit cuts the file off mid-script. SandBase allows up to 65,536.
- `--max-time 900`: one long page can take several minutes.
- `sed '/^```/d'` removes Markdown fences if the model added them.
- `usage` shows the tokens you were billed for. Prices are on the [model page][model].

Open `argon.html` in a browser. If it's blank, open the developer console: the usual causes are a truncated file (raise `max_tokens`) or a CDN that didn't load (ask for everything inline).

## 4. Turn the page into a video

Most creators screen-record the page. To get the same clip every time, record it headlessly with [`scripts/record.mjs`](../scripts/record.mjs):

```bash
npm i -D playwright@1.56.1
npx playwright install chromium          # or use your installed Chrome: export RECORD_CHANNEL=chrome
node scripts/record.mjs argon.html argon.mp4 12 1920 1080   # 12 seconds at 1080p
```

It opens the page at the size you give, records for that many seconds, and converts to H.264 MP4 with ffmpeg. For a clean result, ask in the prompt for an autoplay camera tour or a fixed-length capture mode (see [prompt guide §7](prompt-guide.md#7-plan-for-the-recording)), so nothing depends on a mouse.

Want sound? Several creators here add music made with a music model and sync it in the edit. [@fofrAI][fourier] had Argon itself write the soundtrack prompt for Lyria 3.5.

For a full Python walkthrough with streaming, tool calls and JSON output, see [Gemini 4 Argon API in Python](https://blog.sandbase.ai/gemini-4-argon-api-python-tutorial-2026/?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon&utm_content=reading). For a tested one-prompt game, see [a Gemini 4 Argon game from one prompt](https://blog.sandbase.ai/gemini-4-argon-browser-game-one-prompt-2026/?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon&utm_content=reading).

## Run generated code safely

The HTML is code you haven't read. Opening it from disk is usually fine for a single-file page, but it can still load scripts and make network requests. For anything you don't trust, or to run many pages automatically, use a [SandBase Sandbox][sandbox]: an isolated environment with a time limit and no access to your files or keys.

## Share it

Post your video on X with the prompt and mention Gemini 4 Argon. To have it added here, [submit it](https://github.com/sandbase-lab/awesome-gemini4-argon/issues/new?template=submit-video.yml); accepted posts go into the Lab collection and show up in this list on the next daily sync.

[lab]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[arena]: https://www.sandbase.ai/lab/x/llm-arena?models=google%2Fgemini-4-argon&utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[keys]: https://www.sandbase.ai/console/keys?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[model]: https://www.sandbase.ai/model/google/gemini-4-argon?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[sandbox]: https://www.sandbase.ai/landing/sandbox?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
[fourier]: https://www.sandbase.ai/lab/ai-videos/gemini-4-argon/2110045963951956250?utm_source=github&utm_medium=docs&utm_campaign=awesome-gemini4-argon
