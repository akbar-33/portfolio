# Portfolio

Source for [akbar-khalid.vercel.app](https://akbar-khalid.vercel.app). Static, no build step at deploy time. The one exception is the contact form, which uses two Vercel functions and one dependency (`@vercel/blob`).

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
| `contact-form.js` | The `/contact` form: uploads files to Vercel Blob, then posts the message to `/api/contact` |
| `api/upload.js`, `api/contact.js`, `api/file.js`, `api/_sign.js` | The only server code: Blob upload tokens, the email via Resend, and signed download links |
| `vendor/blob-client.js` | `@vercel/blob/client` `upload()` bundled for the browser (see below) |
| `media/*.png` | Social preview card and the LinkedIn project images |
| `media/src/*.html` | The HTML those PNGs are rendered from, at 1200x630 |

## Narrow screens

The diagrams are horizontal chains, which needs a `min-width` and therefore a sideways drag on a phone. A `max-width: 640px` block in `style.css` restructures them into vertical stacks: lane labels become headings, nodes stack under them, and the arrows rotate to point down. Terminal blocks switch to `white-space: pre-wrap` so long lines fold instead of scrolling, while keeping the indentation that makes validator output readable.

**If you add a new diagram, add its narrow-screen rule at the same time.** Verify with a real measurement rather than by eye: at 320, 375 and 430px, every `.visual` should satisfy `scrollWidth <= clientWidth`, and `document.documentElement.scrollWidth` should equal `clientWidth`.

## Live embeds

The AI-Impact Map post embeds the real interactive tool, not a screenshot. `media/ai-impact-map.html` is the artifact build wrapped in a doctype and head (the source emits body-only HTML). The embed requests `?chart`, which hides the map's own title block and summary cards so the figure is just the matrix; the full-screen link opens the whole page. The iframe src deliberately keeps its `.html` extension: Vercel's `cleanUrls` 308-redirects it, which costs one hop, but the extensionless form 404s on a plain static server, so keeping the extension is what lets `python3 -m http.server` preview the page correctly. `app.js` inserts it as an iframe above 700px and sizes the frame to the iframe's own document height, which is readable because it is same-origin, so the figure has no inner scrollbar. Below 700px it inserts the still image instead and never fetches the 348KB page, since the bubbles are unusable at that width.

To refresh the map after re-running the pipeline, re-wrap the artifact and re-render the still:

```bash
python3 - <<'EOF'
import pathlib
src = pathlib.Path.home()/"Amakor Capital/AI_Matrix_v2/artifact.html"
out = pathlib.Path("media/ai-impact-map.html")
s = src.read_text(); i = s.find("</style>") + len("</style>")
body = s[:i] + "\n</head>\n<body>\n" + s[i:]
# the artifact labels SIC sections with em dashes; this repo does not use them
body = body.replace("\u2014", "\u00b7").replace("&mdash;", "&middot;")
out.write_text('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
  '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
  '<meta name="robots" content="noindex">\n' + body + "\n</body>\n</html>")
EOF
```

The wrap also swaps the em dashes in the section labels for middots, since nothing in this repo carries an em dash.

Three patches are applied to the vendored copy and must survive a re-wrap: `#plot{overflow:visible}` (the x-axis title and size legend are drawn just below the viewBox and an SVG clips its own content), the capture-phase `wheel` guard (the plot zooms on wheel, which hijacks page scrolling everywhere except fullscreen), and `touch-action:pan-y` on the plot so a swipe scrolls the page.

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

## Contact form

`/contact` (linked from every footer) takes a long message plus up to 10 files of 200 MB each and emails them to `akbarthesecond@gmail.com`. Files never pass through a function, which caps a request body at 4.5 MB: the browser asks `api/upload` for a 15-minute token and uploads straight to a **private** Vercel Blob store, then sends the text and the file paths to `api/contact`, which emails through Resend. Files up to 10 MB (25 MB in total) arrive as real attachments; every file is also linked.

Private blobs have no public URL. The email links point at `api/file`, carry an HMAC signature keyed on `BLOB_READ_WRITE_TOKEN`, and expire after 90 days (`LINK_DAYS` in `api/_sign.js`). `api/file` checks the signature and redirects to a Blob URL that is valid for ten minutes, so the bytes never pass through a function. Rotating the Blob token in Vercel revokes every link already sent.

Setup, once, in the Vercel project:

1. **Storage → Create → Blob**, access **Private**, connected to this project. That adds `BLOB_READ_WRITE_TOKEN`.
2. Create a Resend API key and add it as `RESEND_API_KEY`. Until a domain is verified in Resend, the sender is `onboarding@resend.dev`, which can only deliver to the address the Resend account was created with, so `CONTACT_TO` must be that address.
3. Redeploy so the functions see the variables.

Optional: `CONTACT_TO` changes the inbox (default `akbarthesecond@gmail.com`, the Resend account address), `CONTACT_FROM` the sender once a domain is verified, and `SITE_URL` the base of the download links (default: the host the form was sent from). Delete old uploads from the Blob store in the dashboard when you no longer need them; their links stop working.

`vendor/blob-client.js` is regenerated only when bumping `@vercel/blob`:

```bash
echo "export { upload } from '@vercel/blob/client';" > /tmp/entry.js
npx esbuild /tmp/entry.js --bundle --format=esm --platform=browser --minify --legal-comments=none --outfile=vendor/blob-client.js
```
