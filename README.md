# Portfolio

Source for [akbar-khalid.vercel.app](https://akbar-khalid.vercel.app). Static, no build step at deploy time, no dependencies.

## Editing

`index.html`, the six case pages, and everything under `ideas/` are **generated**. Posts come from the `POSTS` list in `build.py`; add a post there, not as a new HTML file. Do not edit them by hand, or the next build will overwrite the change. Edit `build.py` and re-run it:

```bash
python3 build.py
```

That rewrites `index.html`, the six case pages, the ideas index and posts, and `vercel.json` from one source, so the one-pager and the case pages cannot drift apart.

Hand-maintained files:

| File | What it is |
|---|---|
| `build.py` | The generator: copy, exhibits, tooltips, architecture diagrams |
| `style.css` | Shared styles. Dark is the default, light is opt-in via `[data-theme="light"]` |
| `app.js` | Theme toggle, scroll reveal, floating tooltips |
| `media/*.png` | Social preview card and the LinkedIn project images |
| `media/src/*.html` | The HTML those PNGs are rendered from, at 1200x630 |

## Narrow screens

The diagrams are horizontal chains, which needs a `min-width` and therefore a sideways drag on a phone. A `max-width: 640px` block in `style.css` restructures them into vertical stacks: lane labels become headings, nodes stack under them, and the arrows rotate to point down. Terminal blocks switch to `white-space: pre-wrap` so long lines fold instead of scrolling, while keeping the indentation that makes validator output readable.

**If you add a new diagram, add its narrow-screen rule at the same time.** Verify with a real measurement rather than by eye: at 320, 375 and 430px, every `.visual` should satisfy `scrollWidth <= clientWidth`, and `document.documentElement.scrollWidth` should equal `clientWidth`.

## Live embeds

The AI-Impact Map post embeds the real interactive tool, not a screenshot. `media/ai-impact-map.html` is the artifact build wrapped in a doctype and head (the source emits body-only HTML). `app.js` inserts it as an iframe above 700px and sizes the frame to the iframe's own document height, which is readable because it is same-origin, so the figure has no inner scrollbar. Below 700px it inserts the still image instead and never fetches the 348KB page, since the bubbles are unusable at that width.

To refresh the map after re-running the pipeline, re-wrap the artifact and re-render the still:

```bash
python3 - <<'EOF'
import pathlib
src = pathlib.Path.home()/"Amakor Capital/AI_Matrix_v2/artifact.html"
out = pathlib.Path("media/ai-impact-map.html")
s = src.read_text(); i = s.find("</style>") + len("</style>")
out.write_text('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
  '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
  '<meta name="robots" content="noindex">\n' + s[:i] + "\n</head>\n<body>\n" + s[i:] + "\n</body>\n</html>")
EOF
```

**Check it for client references before publishing.** The source lives in a client folder. Grep for the client and engagement names; the only legitimate hits are data content, including a subsector named "Confidential shredding & data destruction".

## Two things that will bite you

**Tooltips must render into a floating node on `body`.** The diagram cards use `overflow-x:auto` so wide diagrams scroll on narrow screens, and that clips absolutely positioned children. A CSS `::after` tooltip inside a card gets sliced at its edge.

**Tooltips reposition on scroll rather than hiding.** `scroll-behavior:smooth` keeps firing scroll events after the page settles, so a hide-on-scroll handler dismisses them the instant they appear.

## Regenerating the images

The PNGs in `media/` are rendered from `media/src/*.html` at 1200x630:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --window-size=1200,630 --hide-scrollbars --virtual-time-budget=5000 \
  --screenshot=media/og.png "file://$PWD/media/src/og.html"
```

The social preview card is the one declared as `og:image` in `build.py`, currently `media/og-v2.png`. Regenerate it whenever the hero copy changes, or link previews keep showing the old headline.

**Replacing the file in place is not enough.** WhatsApp, iMessage and Slack cache previews by URL and will not refetch, so an updated image at the same path never reaches anyone who already has the link cached. Bump the filename (`og-v3.png`) and update the `og:image` line in `build.py`. Keep the old file: links already cached elsewhere still point at it.

To force a refresh for a link already in circulation, run the page through [Facebook's Sharing Debugger](https://developers.facebook.com/tools/debug/), which shares crawler infrastructure with WhatsApp, and [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/) for LinkedIn.

## Deploying

Vercel is connected to this repository, so every push to `main` redeploys. Framework preset is Other, with no build command and no output directory.
