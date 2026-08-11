# Portfolio

Source for [akbar-khalid.vercel.app](https://akbar-khalid.vercel.app). Static, no build step at deploy time, no dependencies.

## Editing

`index.html` and the six case pages are **generated**. Do not edit them by hand, or the next build will overwrite the change. Edit `build.py` and re-run it:

```bash
python3 build.py
```

That rewrites `index.html`, the six case pages, and `vercel.json` from one source, so the one-pager and the case pages cannot drift apart.

Hand-maintained files:

| File | What it is |
|---|---|
| `build.py` | The generator: copy, exhibits, tooltips, architecture diagrams |
| `style.css` | Shared styles. Dark is the default, light is opt-in via `[data-theme="light"]` |
| `app.js` | Theme toggle, scroll reveal, floating tooltips |
| `media/*.png` | Social preview card and the LinkedIn project images |
| `media/src/*.html` | The HTML those PNGs are rendered from, at 1200x630 |

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

`media/og.png` is the social preview card. Regenerate it whenever the hero copy changes, or link previews will show the old headline.

## Deploying

Vercel is connected to this repository, so every push to `main` redeploys. Framework preset is Other, with no build command and no output directory.
