#!/usr/bin/env python3
"""Build the portfolio: one index page plus six case pages, from one source of truth."""
import pathlib

OUT = pathlib.Path("/Users/mandalorian/portfolio")
SITE = "https://akbar-khalid.vercel.app"
GH = "https://github.com/akbar-33"

# ---------------------------------------------------------------- helpers
A = '<div class="ar" aria-hidden="true">&rarr;</div>'

def nd(b, sm="", cls="", tip=""):
    t = f' data-tip="{tip}"' if tip else ""
    s = f"<small>{sm}</small>" if sm else ""
    return f'<div class="nd {cls}"{t}><b>{b}</b>{s}</div>'

def flow(cap, lanes, hint="Hover any stage"):
    body = "".join(
        f'<div class="lane"><div class="lane-tag">{tag}</div><div class="chain">{A.join(nodes)}</div></div>'
        for tag, nodes in lanes)
    return (f'<div class="visual reveal" aria-label="{cap}">'
            f'<div class="visual-caption"><span>{cap}</span><span class="hint">{hint}</span></div>'
            f'<div class="flow">{body}</div></div>')

def head(title, desc, canonical, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/media/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="Abdullah Akbar Khalid">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23EC3013'/%3E%3Ctext x='16' y='23' font-family='monospace' font-size='20' font-weight='bold' fill='%23FBFAF7' text-anchor='middle'%3EA%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
<script>(function(){{try{{if(localStorage.getItem("ak-theme")==="light")document.documentElement.setAttribute("data-theme","light")}}catch(e){{}}}})();</script>
{extra}
</head>
<body>"""

def masthead(brand_link=True):
    brand = ('<a class="brand" href="/">Abdullah Akbar Khalid</a>' if brand_link
             else '<h1>Abdullah Akbar Khalid</h1>')
    return f"""<header class="masthead">
  <div class="wrap-wide masthead-row">
    {brand}
    <nav>
      <a href="/#exhibits">Work</a>
      <a href="{GH}">GitHub</a>
      <a href="https://www.linkedin.com/in/akbar-khalid/">LinkedIn</a>
      <a href="mailto:akbar.khalid@insead.edu">Email</a>
      <button class="theme-toggle" type="button"><span class="dot"></span><span class="label">Dark</span></button>
    </nav>
  </div>
</header>"""

FOOT = f"""<footer class="site">
  <div class="wrap-wide">
    <span>Built by hand, no template, like everything above.</span>
    <span><a href="mailto:akbar.khalid@insead.edu">akbar.khalid@insead.edu</a> · 2026</span>
  </div>
</footer>
<script src="/app.js"></script>
</body>
</html>"""

# ---------------------------------------------------------------- visuals
FUNNEL = """<div class="visual reveal" aria-label="Screening funnel from five million companies to a ranked shortlist">
  <div class="visual-caption"><span>The funnel: one register in, one shortlist out</span><span class="hint">Hover any stage</span></div>
  <div class="funnel">
    <div class="stage" data-tip="The full monthly bulk product from Companies House. Every live company in the UK, roughly 400 columns per row, about 470MB compressed."><div class="bar" style="--w:100%;max-width:24rem"></div><span class="lbl">~5,000,000 · UK register, bulk</span></div>
    <div class="stage" data-tip="First cut on SIC code. Cheap, coarse, and it removes the overwhelming majority before any expensive work begins."><div class="bar" style="--w:44%;max-width:24rem"></div><span class="lbl">tech / IT SIC filter</span></div>
    <div class="stage" data-tip="SIC codes are self-reported and often wrong or stale. The website is the ground truth, so the engine finds and scrapes it before judging what a company actually does."><div class="bar" style="--w:24%;max-width:24rem"></div><span class="lbl">website discovered &amp; scraped</span></div>
    <div class="stage" data-tip="Rules handle the obvious cases; Claude handles the ambiguous ones. Four axes: stack layer, function, business model, and vertical."><div class="bar" style="--w:11%;max-width:24rem"></div><span class="lbl">classified on 4-axis taxonomy</span></div>
    <div class="stage" data-tip="Accounts are filed as iXBRL, a machine-readable format almost nobody parses at scale. This is where revenue and EBITDA estimates come from."><div class="bar" style="--w:5%;max-width:24rem"></div><span class="lbl">financials recovered (iXBRL)</span></div>
    <div class="stage" data-tip="What survives is small enough for a human to read and defensible enough to take into an investment committee."><div class="bar" style="--w:2%;max-width:24rem"></div><span class="lbl">ranked, defensible shortlist</span></div>
  </div>
</div>"""

BANDS = """<div class="visual reveal" aria-label="Two Pret A Manger entities with opposite covenant grades">
  <div class="visual-caption"><span>Real register data: the example that carries the idea</span><span class="hint">Hover either entity</span></div>
  <div class="bands">
    <div class="band bad" data-tip="Incorporated in 2018 as JAB (ACQUISITION) LTD. A holding company by SIC code, filing under the subsidiary audit exemption, so there is no income statement to read. Signing a lease with this entity gets you the brand name and none of the trading history.">
      <div class="co">PRET A MANGER LIMITED</div>
      <div class="fact">No. 11391321 · inc. 2018<br>SIC 64209 · holding company<br>audit-exemption subsidiary</div>
      <div class="grade">Band C · 55/100</div>
      <div class="verdict">require guarantee or deposit</div>
    </div>
    <div class="band good" data-tip="Trading since 1984 and filing full accounts, which is the strongest disclosure level available. This is the entity with the sandwich shops, the revenue, and the covenant a landlord actually wants on the lease.">
      <div class="co">PRET A MANGER (EUROPE)&nbsp;LIMITED</div>
      <div class="fact">No. 01854213 · inc. 1984<br>SIC 47110 · retail, trading<br>full accounts filed</div>
      <div class="grade">Band A · 100/100</div>
      <div class="verdict">institutionally acceptable</div>
    </div>
  </div>
</div>"""

TERM = """<div class="visual reveal" aria-label="cited-memo self-grading terminal output">
  <div class="visual-caption"><span>The self-grade: real output format</span><span class="hint">Hover any line</span></div>
  <div class="term"><span class="row" data-tip="Every figure in the draft is located, then checked: does the sentence containing it cite a passage, and does that passage exist? 92% is a grade of the draft, not a promise about it.">traceable figures : <span class="ok">24/26  (92%)</span></span>
<span class="row" data-tip="A citation pointing at a passage that was never extracted. This is the failure mode people fear most from AI drafting, and it is the cheapest of the three to detect.">invalid citations : <span class="ok">0</span></span>
<span class="row" data-tip="Assertions with no evidence behind them. The tool refuses to hide these: it names them in full so the reviewer knows exactly which two sentences to check.">unsupported claims: <span class="warn">2</span></span>
<span class="row dim">  - EBITDA margin of 18% is expected to hold through FY26.
  - Management estimates a further £400k of synergies.</span></div>
</div>"""

TREE = """<div class="visual reveal" aria-label="Compliance repository mapped to obligations">
  <div class="visual-caption"><span>The repository is the database. Each path evidences an obligation.</span><span class="hint">Hover any path</span></div>
  <div class="tree">
    <div class="row root"><span class="path">your-compliance-repo/</span><span class="ob"></span></div>
    <div class="row" data-tip="Firm name and the staleness thresholds that decide when due diligence or a lifecycle review counts as overdue."><span class="path">├── config.yaml</span><span class="ob">firm, staleness thresholds</span></div>
    <div class="row" data-tip="The AI system register. A firm cannot govern what it has not written down, so this is the record everything else refers back to."><span class="path">├── systems/*.yaml</span><span class="ob"><b>Governance.</b> Every AI system, each with a named surveyor</span></div>
    <div class="row crown" data-tip="The crown jewel. A written decision on output reliability by a named, qualified surveyor, optionally bound to the SHA-256 of the exact output reviewed, so the record provably covers that output and no other."><span class="path">├── rdrs/&lt;engagement&gt;/</span><span class="ob"><b>Documentation.</b> The reliability decision, bound to the SHA-256 of the output</span></div>
    <div class="row" data-tip="Generated from the register rather than written by hand, so the wording a client sees stays consistent with what the firm actually runs."><span class="path">├── disclosures/*.md</span><span class="ob"><b>Client transparency.</b> ToE wording, generated from the register</span></div>
    <div class="row" data-tip="Procurement diligence on external AI vendors: data flows, retention, model provenance, exit terms. Goes stale after twelve months and the validator says so."><span class="path">├── dd/*.md</span><span class="ob"><b>Risk management.</b> Vendor procurement diligence</span></div>
    <div class="row" data-tip="A lived incident log reads as real governance. An empty one reads as theatre, which is exactly what a regulator is trained to notice."><span class="path">└── incidents/*.md</span><span class="ob"><b>Risk, lifecycle.</b> Outputs rejected and errors caught</span></div>
  </div>
</div>"""

GRID = """<div class="visual reveal" aria-label="Command Center surfaces with automation health highlighted">
  <div class="visual-caption"><span>Nine surfaces, one honest read</span><span class="hint">Hover any surface</span></div>
  <div class="grid-status">
    <div class="cell" data-tip="What actually needs to happen in the next few hours, not the whole backlog."><span class="dot"></span>Today</div>
    <div class="cell" data-tip="The full backlog, with capture from automated sources as well as by hand."><span class="dot"></span>Tasks</div>
    <div class="cell" data-tip="What slipped, surfaced rather than buried."><span class="dot"></span>Overdue</div>
    <div class="cell" data-tip="Commitments sitting alongside the task load instead of in a separate app."><span class="dot"></span>Calendar</div>
    <div class="cell" data-tip="Who I owe a reply, an introduction, or a follow-up."><span class="dot"></span>People</div>
    <div class="cell" data-tip="Application pipeline tracked through stages."><span class="dot"></span>Jobs</div>
    <div class="cell" data-tip="A single read on whether the week is going well."><span class="dot"></span>Score</div>
    <div class="cell" data-tip="What is left in the current window."><span class="dot"></span>Remaining</div>
    <div class="cell hot" data-tip="The page that justifies the project. Automations fail silently, and a briefing that stops arriving looks identical to a quiet news day until something checks."><span class="dot"></span><strong>Automation&nbsp;Health</strong></div>
  </div>
</div>"""

RELAY = """<div class="visual reveal" aria-label="Automation stack data flow">
  <div class="visual-caption"><span>One flow: sources in, decisions out</span><span class="hint">Hover any node</span></div>
  <div class="relay">
    <div class="col">
      <div class="node" data-tip="A trading community whose calls are worth reading but arrive faster than anyone can watch.">Discord</div>
      <div class="node" data-tip="Stories expire in 24 hours, so anything worth keeping has to be captured automatically or it is gone.">Instagram</div>
      <div class="node" data-tip="Blocked to plain fetching and to most headless browsers. Reading it needs a real, authenticated session.">LinkedIn</div>
      <div class="node" data-tip="Lever, Ashby and Greenhouse expose JSON APIs that return the whole board, which page scraping silently truncates.">job boards</div>
    </div>
    <div class="arrows" aria-hidden="true">&rarr;</div>
    <div class="col">
      <div class="node core" data-tip="Playwright for the pages that fight back, Claude for the judgement calls, launchd for the schedule. The ranking is the part that matters: raw capture is easy, deciding what deserves attention is not.">scrape · parse · rank<small>Python · Playwright · Claude · launchd</small></div>
    </div>
    <div class="arrows" aria-hidden="true">&rarr;</div>
    <div class="col out">
      <div class="node" data-tip="Twice a day, on a schedule, to the place I actually read. A dashboard I have to remember to open is a dashboard I will not open.">WhatsApp, 2×/day</div>
      <div class="node" data-tip="The automations need somewhere to land, and somewhere I can see whether they are still running.">Command Center</div>
    </div>
  </div>
</div>"""

ARCH = {
"screening": flow("How it operates: two pipelines over one register", [
  ("Pipeline 1<br>src/01-09", [
    nd("UK bulk register","~5M rows · 400+ cols","io","The monthly bulk product, about 470MB. Downloading it is trivial; making it mean something is the work."),
    nd("Filter","tech / IT SIC","","A coarse SIC cut first, because every later stage costs real money per company."),
    nd("Discover + scrape","find each site","","Most companies never file a website anywhere machine-readable, so the engine has to go and find it."),
    nd("Classify","rules + Claude · 4 axes","","Stack layer, function, business model, vertical. Rules take the obvious cases so the model is only asked the hard ones."),
    nd("Roll up + score","niche clustering","","Individual companies matter less than the niche they sit in. This is where a roll-up thesis actually forms.")]),
  ("Pipeline 2<br>scripts/10-31", [
    nd("Recover","sites + owners","","A second pass over everything the first pipeline failed to resolve, using different search providers."),
    nd("Pull accounts","Companies House iXBRL","","Filed accounts in a machine-readable format. Free, public, and almost nobody parses them at scale."),
    nd("Triangulate","revenue / EBITDA","","Small companies file abbreviated accounts, so revenue is never simply stated. It is inferred from what is disclosed."),
    nd("Defensibility","moat scoring","","Recurring revenue, switching costs, and contract shape, because a cheap multiple on a fragile business is not a bargain."),
    nd("Consolidate","one master table","","Everything deduped into a single table an analyst can sort, filter, and defend.")]),
  ("Output", [nd("Ranked, deduped target universe with estimated financials and defensibility scores","","out","The deliverable: a shortlist small enough to read and evidenced enough to argue for.")]),
]),
"covenant": flow("How it operates: register in, defensible verdict out", [
  ("Live path", [
    nd("Companies House API","free, public register","io","Live at the moment you look, so a certificate is never a stale photograph."),
    nd("covenant.py","deduction ledger, each rule names its filing","","Every entity starts at 100 and loses points only for reasons that cite the filing that evidences them."),
    nd("app.py (Flask)","search · certificate · compare","","Four views, each answering one question a surveyor actually asks."),
    nd("Band A to E + score","","out","A grade with its working shown, phrased in transaction language: require a guarantee, take a deposit, accept as is.")]),
  ("Scale path", [
    nd("Parquet snapshot","5,695,465 companies","io","The monthly bulk snapshot, roughly 470MB, dated the first of the month and visibly distinct from live readings."),
    nd("sweep.py + DuckDB","~0.6s per postcode, cached","","Fast enough to sweep a whole district interactively, which is what turns a single check into portfolio triage."),
    nd("freeze.py","renders the app to static HTML","","The public demo is the real app, frozen. No server to sleep, no API key to leak."),
    nd("GitHub Pages","demo that never sleeps","out","Anyone can click through real register data without installing anything.")]),
]),
"oversight": flow("How it operates: capture, store, enforce", [
  ("Capture", [
    nd("init","firm config","","Sets the firm name and the staleness thresholds the validator later enforces."),
    nd("add-system","the AI register","","Each system gets a named responsible surveyor and a lifecycle review date."),
    nd("rdr","binds SHA-256 of the output","","Pipe the AI output straight in and the record is bound to that exact output, not to a description of it."),
    nd("disclose","ToE text","","Generated from the register, so the client-facing wording cannot drift from what the firm runs."),
    nd("dd · incidents","","","Vendor diligence and the lived incident log, the two records that separate real governance from theatre.")]),
  ("Store", [nd("Plain files in a git repository: systems/ · rdrs/ · disclosures/ · dd/ · incidents/","the commit log is the evidence timeline","io","No database and no vendor holding records a firm must retain for years. Git already provides authorship, timestamps and append-only history.")]),
  ("Enforce", [
    nd("check","exits non-zero, names the obligation breached","gate","Runs in CI or as a pre-commit hook. Nine failure classes, each reported with the obligation it would breach."),
    nd("pack","refuses to render while any check fails","gate","The gate that gives the whole thing teeth."),
    nd("Regulator-ready record","","out","One HTML file, handed to a RICS review or a professional indemnity insurer.")]),
]),
"cited-memo": flow("How it operates: drafting is cheap, verification is the product", [
  ("Ingest", [
    nd("Source PDFs","the data room","io","Whatever the deal actually gave you, in whatever shape it arrived."),
    nd("Extract","every page becomes a numbered passage, tagged document and page","","The numbering is the whole trick. A citation can only be checked if the thing it points at has an address.")]),
  ("Draft", [nd("The model writes from those passages only, and must follow each figure with the citation it came from","","","Constraining the source material is what makes the output checkable at all.")]),
  ("Verify", [
    nd("Offline checker","no API key, no model in the loop","gate","Deliberately not an LLM. A model grading its own homework can be talked out of a failure; a parser cannot."),
    nd("Catches three failures","uncited figure · citation to a passage that does not exist · claim with no evidence","gate","Three distinct failure modes, each detected differently."),
    nd("Graded memo","coverage, invalid citations, unsupported claims","out","You check the two flagged sentences instead of all twenty-six.")]),
]),
}

# ---------------------------------------------------------------- exhibits
EX = [
 dict(slug="screening-engine", letter="A", label="Sourcing at register scale",
   title="Companies House Screening Engine", status="public · python", cite=1,
   tags=["Python","Claude API","iXBRL","Companies House bulk data"],
   pitch=['Which founder-owned tech-services firms actually fit a roll-up thesis, including the ones no keyword search would ever surface? This engine takes the <strong>entire UK register (~5M companies, 400+ columns)</strong> down to a ranked, defensible shortlist: it discovers each company\'s website, classifies it with rules + Claude on a four-axis taxonomy, recovers financials from iXBRL accounts, and scores defensibility.'],
   visuals=[FUNNEL, ARCH["screening"]]),
 dict(slug="covenant", letter="B", label="Covenant strength",
   title="Covenant", status="public · live demo", cite=2,
   tags=["Python","Companies House API","DuckDB","GitHub Pages demo"],
   pitch=['A lease is offered by entity X. <em>Is that covenant real?</em> Search the register for "Pret A Manger" and twenty entities come back, two of them named almost identically. One is the trading company filing full accounts since 1984. The other is a 2018 acquisition vehicle, formerly JAB (ACQUISITION) LTD. Same brand, same registered address, opposite covenant.<a class="cite" href="/#ref-3">[3]</a>',
          'Covenant screens tenant strength from free, public Companies House data (one tenant, a rent roll, or the whole country) instead of a per-report credit agency fee.'],
   visuals=[BANDS, ARCH["covenant"]]),
 dict(slug="oversight", letter="C", label="Governed AI",
   title="Oversight", status="public · live evidence pack", cite=4,
   tags=["Python","Jinja2","git as the database","SHA-256 output binding"],
   pitch=['Since 9 March 2026, a RICS member whose AI use materially affects surveying work has to be able to show four things: which AI systems the firm uses, that a named qualified surveyor wrote a decision on how reliable the output was, that the client was told in the Terms of Engagement, and that the vendor was diligenced.<a class="cite" href="/#ref-5">[5]</a> That is a records problem, and I could not find a single tool built for it.',
          'Oversight keeps those records as plain files in a git repository, so authorship, timestamps and append-only history come free: the audit trail is the repo. <strong>check</strong> exits non-zero and names the obligation each failure would breach. <strong>pack</strong> renders the regulator-ready evidence pack and refuses to run while any check fails, so a pack existing is itself evidence the records were coherent when it was made.'],
   visuals=[TREE, ARCH["oversight"]]),
 dict(slug="cited-memo", letter="D", label="Provenance",
   title="cited-memo", status="public · python", cite=6,
   tags=["Python","PDF extraction","offline verification"],
   pitch=['AI drafts a plausible investment memo in seconds. The problem is the next hour, when an associate re-checks every figure against the data room because nobody can tell which numbers came from the accounts and which the model invented. cited-memo inverts it: it drafts from source documents only, cites the exact page behind every figure, then <strong>grades its own output</strong> (offline, no API key).',
          'You check the two flagged sentences instead of all twenty-six.'],
   visuals=[TERM, ARCH["cited-memo"]]),
 dict(slug="command-center", letter="E", label="Operations",
   title="Command Center", status="public · react + supabase", cite=7,
   tags=["React","TypeScript","Supabase","row-level auth","edge functions"],
   pitch=['One dashboard for what six apps and my head used to hold: today\'s priorities, the backlog, overdue items, people I owe a reply, the job pipeline. My AI automations capture into it all day. The page that justifies the project is <strong>Automation Health</strong>, because automations fail silently and a briefing that stops arriving looks identical to a quiet news day until something checks.'],
   visuals=[GRID]),
 dict(slug="automation-stack", letter="F", label="The automation stack",
   title="The systems that run my day", status='private by necessity<a class="cite" href="/#ref-8">[8]</a>', cite=None,
   tags=["Python","Playwright","Claude API","launchd","WhatsApp bridge"],
   pitch=['No repo for these; they hold my sessions and keys. A scraping engine that reads pages bot-detection blocks, including LinkedIn. A Discord to WhatsApp relay that reformats a trading community\'s calls into structured tables in real time. An Instagram story archiver with review notes. And a briefing pipeline that ranks everything I\'m tracking and pushes a top-five to my WhatsApp twice a day, on a launchd schedule.'],
   visuals=[RELAY]),
]

# ---------------------------------------------------------------- index
def build_index():
    arts = []
    for e in EX:
        cite = f'<a class="cite" href="/#ref-{e["cite"]}">[{e["cite"]}]</a>' if e["cite"] else ""
        pitches = "".join(f'<p class="pitch reveal">{p}</p>' for p in e["pitch"])
        vis = "".join(e["visuals"])
        tags = "".join(f"<span>{t}</span>" for t in e["tags"])
        extra = ""
        if e["slug"] == "oversight":
            extra = ('<p class="pitch reveal" style="margin-top:1.2rem">The example firm registers '
                     '<a href="/covenant">Covenant</a> as one of its AI systems, with a real reliability decision '
                     'record for a real screening. One tool doing surveying work with AI, one tool governing AI to '
                     'surveying standards.</p>')
        arts.append(f"""<article class="exhibit" id="{e['slug']}">
  <div class="wrap">
    <div class="ex-head reveal">
      <span class="ex-label">Exhibit {e['letter']} · {e['label']}</span>
      <span class="ex-status">{e['status']}</span>
    </div>
    <h3 class="reveal"><a href="/{e['slug']}">{e['title']}</a>{cite}</h3>
    {pitches}
    {vis}
    {extra}
    <div class="tags reveal">{tags}</div>
    <a class="more" href="/{e['slug']}">Read the full case<span class="arrow">&rarr;</span></a>
  </div>
</article>""")

    refs = f"""<section class="refs" id="references">
  <div class="wrap">
    <h4>References</h4>
    <ol>
      <li id="ref-1"><span class="n">[1]</span><span><a href="{GH}/companies-house-screening-engine">github.com/akbar-33/companies-house-screening-engine</a></span></li>
      <li id="ref-2"><span class="n">[2]</span><span><a href="{GH}/covenant">github.com/akbar-33/covenant</a> · <a href="https://akbar-33.github.io/covenant/">live demo</a></span></li>
      <li id="ref-3"><span class="n">[3]</span><span>Companies House: <a href="https://find-and-update.company-information.service.gov.uk/company/11391321">No. 11391321</a> · <a href="https://find-and-update.company-information.service.gov.uk/company/01854213">No. 01854213</a></span></li>
      <li id="ref-4"><span class="n">[4]</span><span><a href="{GH}/oversight">github.com/akbar-33/oversight</a> · <a href="https://akbar-33.github.io/oversight/">example evidence pack</a></span></li>
      <li id="ref-5"><span class="n">[5]</span><span>RICS professional standard, <a href="https://www.rics.org/profession-standards/rics-standards-and-guidance/conduct-competence/responsible-use-of-ai"><i>Responsible use of AI in surveying practice</i></a>, in force 9 March 2026. Oversight is independent tooling and is not endorsed by RICS.</span></li>
      <li id="ref-6"><span class="n">[6]</span><span><a href="{GH}/cited-memo">github.com/akbar-33/cited-memo</a></span></li>
      <li id="ref-7"><span class="n">[7]</span><span><a href="{GH}/command-center-companion">github.com/akbar-33/command-center-companion</a></span></li>
      <li id="ref-8"><span class="n">[8]</span><span class="note">source withheld: these systems carry live credentials and personal data. Demos on request.</span></li>
    </ol>
  </div>
</section>"""

    body = f"""{masthead(brand_link=False)}
<section class="thesis">
  <div class="wrap">
    <p class="eyebrow reveal">Operator-founder · INSEAD MBA · UK &amp; EU private markets</p>
    <h2 class="reveal d1">Most people can read a deal or build a product. I do <em>both</em>.</h2>
    <p class="reveal d2">I build the tooling I need for the job, then open-source it: deal sourcing at register scale, covenant checks, AI governance records, memo verification. The diligence stack I wanted and couldn't buy.</p>
    <p class="repos reveal d3">Source: <a href="{GH}/companies-house-screening-engine">screening engine</a> · <a href="{GH}/covenant">covenant</a> · <a href="{GH}/oversight">oversight</a> · <a href="{GH}/cited-memo">cited-memo</a> · <a href="{GH}/command-center-companion">command center</a> · <a href="{GH}">everything on GitHub</a><br>Live demos: <a href="https://akbar-33.github.io/covenant/">covenant dashboard</a> · <a href="https://akbar-33.github.io/oversight/">oversight evidence pack</a></p>
  </div>
</section>
<div id="exhibits">{''.join(arts)}</div>
{refs}
{FOOT}"""
    (OUT/"index.html").write_text(
        head("Abdullah Akbar Khalid · Exhibits",
             "Systems I built for private-markets work: register-scale screening, covenant checks, AI governance records, self-verifying memos. Every claim cites its source.",
             SITE + "/") + body)

build_index()

# ---------------------------------------------------------------- case pages
def dec(title, body):
    return f'<div class="decision"><b>{title}</b>{body}</div>'

CASES = {
"screening-engine": dict(
  eyebrow="Exhibit A · Sourcing at register scale",
  h1="Screening five million companies into a shortlist you can defend",
  lede="A sourcing engine for buy-and-build. It reads the entire UK Companies House register and returns a ranked target universe, including the companies no keyword search would ever surface.",
  meta=[("Status","Public, actively used"),("Stack","Python · Claude API · pandas · Parquet"),
        ("Source",f'<a href="{GH}/companies-house-screening-engine">github.com/akbar-33/companies-house-screening-engine</a>')],
  secs=[
   ("The problem", """<p>A search fund or a buy-and-build thesis lives or dies on sourcing. The dream is the easy part; the grind is reading through thousands of companies to find the few that fit. The standard tools all start from a keyword, which means they can only return companies that describe themselves the way you happen to have phrased it.</p>
<p>The UK register is free, public and structured. Roughly five million live companies, about 400 columns each. Nobody screens it systematically because the raw file is unusable on its own: SIC codes are self-reported and often stale, most rows carry no website, and small companies file abbreviated accounts with no revenue line at all.</p>""",
    [FUNNEL]),
   ("How it operates", """<p>Two pipelines run over one register. The first decides what each company <em>is</em>. The second recovers what it is <em>worth</em>. Every stage caches its output, so a failed run resumes rather than restarting, which matters when a full pass costs real money in API calls.</p>""",
    [ARCH["screening"]]),
   ("Decisions worth defending",
    dec("Cheap filters before expensive ones",
        "<p>SIC filtering is coarse and imperfect, but it runs on a laptop in seconds and removes most of the register before anything bills per company. Ordering the pipeline by cost per row is the difference between a run that is affordable and one that is not.</p>") +
    dec("The website is the ground truth, not the SIC code",
        "<p>A company's own description of itself, scraped from its site, is far more reliable than a code it picked at incorporation and never revisited. So the engine spends real effort finding sites that were never filed anywhere machine-readable, then judges the company on what it says it does.</p>") +
    dec("Rules first, model second",
        "<p>Claude is asked only the genuinely ambiguous cases. Rules handle the obvious ones deterministically, which keeps the classification reproducible, cheaper, and auditable. A four-axis taxonomy (stack layer, function, business model, vertical) means a company can be described precisely instead of dropped into one blunt bucket.</p>") +
    dec("Estimate the financials, and say that they are estimates",
        "<p>Small companies do not file a revenue line. The engine triangulates from what is disclosed in iXBRL filings and labels the result as an estimate throughout. A number presented with false confidence is worse than no number.</p>"), []),
   ("What it produces", """<p>A single deduped master table: the target universe, ranked, with estimated financials and defensibility scores attached. Small enough for a partner to read, and evidenced enough to argue for in an investment committee.</p>
<p>A second lightweight entry point runs a fast SIC-only first cut over the same bulk register, for when you want a rough sector map rather than a full classification pass.</p>""", []),
  ]),

"covenant": dict(
  eyebrow="Exhibit B · Covenant strength",
  h1="Is that covenant real, and if not, where does the money actually sit?",
  lede="Screening the covenant strength of UK commercial tenants from free public filings, at any scale from one lease to an entire postcode district.",
  meta=[("Status","Public, live demo"),("Stack","Python · Companies House API · DuckDB · Flask"),
        ("Source",f'<a href="{GH}/covenant">github.com/akbar-33/covenant</a>'),
        ("Demo",'<a href="https://akbar-33.github.io/covenant/">akbar-33.github.io/covenant</a>')],
  secs=[
   ("The problem", """<p>In UK commercial property the building is almost secondary. What you are buying is the rental income stream, and that stream is only as good as the tenant's ability to keep paying. Surveyors call this covenant strength and assess it constantly, today either by paying a credit reference agency per report or by eyeballing it.</p>
<p>Meanwhile every UK company files public, structured, machine-readable records for free, and the strongest early warnings of tenant failure are buried in them. Almost nobody reads them systematically, because doing it by hand across a rent roll is tedious.</p>""", []),
   ("The example that carries the whole idea", """<p>Search the register for "Pret A Manger" and twenty entities come back, several dissolved, two of them named almost identically. One is a 2018 acquisition vehicle, formerly JAB (ACQUISITION) LTD, filing under the subsidiary audit exemption. The other has traded since 1984 and files full accounts.</p>
<p>Same brand. Same registered address. Opposite covenant. A landlord who signs the first entity believes they have the sandwich chain, and actually holds a shell. That distinction is free, public and structured, and this is the machinery for checking it.</p>""",
    [BANDS]),
   ("How it operates", """<p>Two paths with deliberately different currencies. A certificate is fetched live from the Companies House API at the moment you look at it. A sweep runs over a monthly bulk snapshot of 5,695,465 companies, dated the first of the month. The interface keeps the two visibly distinct, because presenting a month-old reading as live would be exactly the kind of quiet error this tool exists to catch.</p>""",
    [ARCH["covenant"]]),
   ("Decisions worth defending",
    dec("Deduction-based scoring, never a black box",
        "<p>Every entity starts at 100 and loses points only for reasons that name the filing evidencing them. A surveyor can disagree with a deduction and go read the source. A score with no ledger behind it is an opinion wearing a number's clothing.</p>") +
    dec("Transaction language, not adjectives",
        "<p>The output says require a guarantee, take a six to twelve month deposit, or accept as is. Those are the decisions a lease negotiation actually turns on. Describing a tenant as 'moderate risk' helps nobody.</p>") +
    dec("The demo is the real app, frozen",
        "<p>The public dashboard is generated by rendering the live application to static HTML. No server to fall asleep, no API key to leak, and no risk of a demo drifting away from the tool it claims to represent.</p>") +
    dec("A screen, not an opinion",
        "<p>Nothing here is a Red Book valuation or investment advice. It tells you which entities deserve an hour of a surveyor's attention, which is a genuinely useful thing to automate and a dangerous thing to overclaim.</p>"), []),
   ("At portfolio scale", """<p>The sweep scores a whole postcode district in about six tenths of a second per postcode once cached. A single W1 run scores 7,746 companies, returns the band distribution, the weakest names, a distress league across the district, and a sector panel. That is what turns a one-lease check into portfolio triage.</p>""", []),
  ]),

"oversight": dict(
  eyebrow="Exhibit C · Governed AI",
  h1="The RICS AI standard is a records problem, and nobody had built the records tool",
  lede="Compliance tooling for the professional standard on responsible use of AI in surveying practice, in force since 9 March 2026.",
  meta=[("Status","Public, live evidence pack"),("Stack","Python · Jinja2 · git"),
        ("Source",f'<a href="{GH}/oversight">github.com/akbar-33/oversight</a>'),
        ("Demo",'<a href="https://akbar-33.github.io/oversight/">example evidence pack</a>')],
  secs=[
   ("The problem", """<p>Since 9 March 2026, RICS members and regulated firms whose AI use has a material impact on the delivery of surveying services must be able to show four things: what AI they use, that a named qualified surveyor made a written decision about the reliability of AI outputs, that clients were told in the Terms of Engagement, and that AI procurement was diligenced.</p>
<p>That is not a modelling problem. It is a records problem, and when I looked there was no tooling for it at all.</p>""", []),
   ("The design bet: compliance records are plain files in a git repository", """<p>No database, no SaaS, no vendor holding records a firm must retain for years. Git already provides append-only history, authorship and timestamps, which is what an audit trail <em>is</em>. A regulator-ready evidence pack then becomes a render of the repository, with the commit log as the evidence timeline.</p>""",
    [TREE]),
   ("How it operates", """<p>Commands capture each record, the repository stores them, and the validator refuses to let an incomplete set become a document anyone could rely on.</p>""",
    [ARCH["oversight"]]),
   ("The teeth", """<p><code>oversight check</code> validates every record and exits non-zero on failure, so it runs in CI or as a pre-commit hook. Every failure cites the obligation it would breach:</p>
<div class="visual reveal"><div class="visual-caption"><span>Real validator output</span></div><div class="term">  FAIL  systems/leasereader.yaml
        external system with no procurement due-diligence record on file
        <span class="dim">&#8627; Risk management: procurement due diligence, data governance, and
          review through the AI lifecycle</span>

  FAIL  rdrs/2026-114/
        engagement used AI but has no ToE disclosure on file: run 'oversight disclose'
        <span class="dim">&#8627; Client transparency: material AI use disclosed in the Terms of Engagement</span></div></div>
<p>It catches unnamed responsible surveyors, external systems without due diligence, diligence gone stale past twelve months, overdue lifecycle reviews, unsigned or malformed decision records, records referencing unregistered systems, engagements that used AI with no client disclosure, and template placeholders left sitting in a record.</p>""", []),
   ("Decisions worth defending",
    dec("The pack refuses to render while any check fails",
        "<p>This is the whole point. If a pack can always be produced, its existence proves nothing. Because it cannot, a pack is itself evidence that the records were coherent at the moment it was generated.</p>") +
    dec("Bind the decision to the output, not to a description of it",
        "<p>A reliability decision can be bound to the SHA-256 of the exact output reviewed, so the record provably covers that output and no other. Without it, a decision record is an assertion that some review happened, some time, about something.</p>") +
    dec("Paraphrase the obligations, never invent clause numbers",
        "<p>The published RICS text is authoritative and this tool is not it. Obligation text is deliberately paraphrased and no clause numbers are fabricated, so nobody can mistake independent tooling for the standard itself.</p>"), []),
  ]),

"cited-memo": dict(
  eyebrow="Exhibit D · Provenance",
  h1="AI drafting is cheap. Checking the draft is what costs you an hour.",
  lede="An investment memo drafted only from source documents, where every figure cites its page, and the tool grades its own provenance before you read a word.",
  meta=[("Status","Public"),("Stack","Python · PDF extraction · offline verifier"),
        ("Source",f'<a href="{GH}/cited-memo">github.com/akbar-33/cited-memo</a>')],
  secs=[
   ("The problem", """<p>AI writes a plausible investment memo in seconds. The problem is the next hour, when an associate re-checks every figure against the data room because nobody can tell which numbers came from the accounts and which the model invented.</p>
<p>That verification cost is why most AI drafting tools quietly stop being used around week three. The draft was never the expensive part.</p>""", []),
   ("The inversion", """<p>The tool drafts from source documents only, cites the exact page behind every figure, and then grades its own output. Two uncited claims surfaced by name means you check two sentences instead of twenty-six.</p>""",
    [TERM]),
   ("How it operates", """<p>Three steps, and the third is the one that matters.</p>""",
    [ARCH["cited-memo"]]),
   ("Decisions worth defending",
    dec("The verifier is not a language model",
        "<p>It runs offline with no API key and no model in the loop. A model asked to grade its own homework can be argued out of a failure; a parser that looks for a citation and checks whether the passage exists cannot. Making verification dumber made it trustworthy.</p>") +
    dec("Numbering the passages is the whole trick",
        "<p>A citation can only be checked if the thing it points at has an address. Turning every page into a numbered passage tagged with its document and page number is what makes the rest mechanically verifiable.</p>") +
    dec("Name the unsupported claims in full",
        "<p>A coverage percentage on its own invites you to shrug. Printing the exact sentences that lack evidence turns a score into a two-minute task.</p>"), []),
   ("Three failure modes, caught separately", """<p>Verification catches a figure with no citation at all, a citation pointing at a passage that does not exist, and a claim asserted without evidence. They fail differently and are detected differently, which is why a single confidence score would hide more than it reveals.</p>""", []),
  ]),

"command-center": dict(
  eyebrow="Exhibit E · Operations",
  h1="Automations need somewhere to land, and somewhere you can see them fail",
  lede="One dashboard for what six apps and my head used to hold, and one page that tells me whether the machinery behind it is still running.",
  meta=[("Status","Public"),("Stack","React · TypeScript · Vite · Supabase"),
        ("Source",f'<a href="{GH}/command-center-companion">github.com/akbar-33/command-center-companion</a>')],
  secs=[
   ("The problem", """<p>I run a lot of my working life through AI automations: briefings, task capture, inbox triage, follow-ups. Those automations need somewhere to put their output, and I need somewhere to go to see whether they are still working.</p>""",
    [GRID]),
   ("The page that justifies the project", """<p>Automation Health. Automations fail silently, and that is the entire danger. A briefing that stops arriving looks exactly like a quiet news day until you go looking, by which point you have been quietly uninformed for a fortnight.</p>
<p>The page shows whether each background job actually ran, when it last succeeded, and what it expected its own schedule to be. It is the difference between a dashboard that reports on the world and one that also reports on itself.</p>""", []),
   ("Decisions worth defending",
    dec("Row-level auth from the start",
        "<p>Personal data, contacts and application pipeline live here. Access control belongs in the database, enforced per row, rather than in the client where it is one bug away from not existing.</p>") +
    dec("Capture from automated sources, not just by hand",
        "<p>A task list only I can write into becomes stale the first busy week. Edge functions let the automations file directly into the same backlog I read.</p>"), []),
  ]),

"automation-stack": dict(
  eyebrow="Exhibit F · The automation stack",
  h1="The systems that run my day, and why none of them have a repository",
  lede="A scraping engine, a real-time relay, an archiver and a ranked twice-daily briefing. All working, all private, because they hold live sessions and keys.",
  meta=[("Status","Private by necessity"),("Stack","Python · Playwright · Claude API · launchd"),
        ("Source","Source withheld. Demos on request.")],
  secs=[
   ("Why there is no repository", """<p>These carry authenticated browser sessions, API keys and personal data. Publishing them would mean either shipping credentials or gutting the parts that make them work. So they are described here rather than linked, and labelled private rather than left vaguely implied.</p>""",
    [RELAY]),
   ("What they do", """<p><strong>A universal scraper.</strong> Renders with an undetected browser and extracts structured data with a model, for the pages that return a block page or an empty shell to anything simpler. It reads sites that defeat plain fetching, including LinkedIn.</p>
<p><strong>A Discord to WhatsApp relay.</strong> Watches a trading community and reformats its calls into structured tables, in real time, in the place I actually read messages. Planned setups stay in their own section rather than being mixed in with live calls, because conflating the two is how you act on something that was never a signal.</p>
<p><strong>An Instagram story archiver.</strong> Stories expire in 24 hours, so anything worth keeping has to be captured automatically or it is gone. Captures with review notes attached.</p>
<p><strong>A briefing pipeline.</strong> Ranks everything I am tracking and pushes a top five to WhatsApp twice a day on a launchd schedule. The ranking is the hard part: capture is easy, deciding what deserves attention is not.</p>""", []),
   ("Decisions worth defending",
    dec("Deliver to where attention already is",
        "<p>A dashboard I have to remember to open is a dashboard I will not open. The briefing goes to WhatsApp because that is where I already look, and the dashboard exists for when I want depth rather than a nudge.</p>") +
    dec("Rank, do not just collect",
        "<p>An unranked feed is a second inbox, which is a cost rather than a tool. Five items, ordered, twice a day, is a decision aid.</p>"), []),
  ]),
}

for e in EX:
    c = CASES[e["slug"]]
    meta = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in c["meta"])
    secs = []
    for title, html, vis in c["secs"]:
        secs.append(f'<section class="sec"><div class="wrap"><h2 class="reveal">{title}</h2>'
                    f'<div class="reveal">{html}</div>{"".join(vis)}</div></section>')
    body = f"""{masthead()}
<section class="case-hero">
  <div class="wrap">
    <a class="backlink" href="/#{e['slug']}">&larr; All exhibits</a>
    <p class="eyebrow reveal" style="margin-top:1rem">{c['eyebrow']}</p>
    <h1 class="reveal d1">{c['h1']}</h1>
    <p class="lede reveal d2">{c['lede']}</p>
    <div class="case-meta reveal d3">{meta}</div>
  </div>
</section>
{''.join(secs)}
<section class="sec"><div class="wrap">
  <a class="more" href="/#{e['slug']}">Back to all exhibits<span class="arrow">&rarr;</span></a>
</div></section>
{FOOT}"""
    (OUT/f"{e['slug']}.html").write_text(
        head(f"{e['title']} · Abdullah Akbar Khalid", c["lede"], f"{SITE}/{e['slug']}") + body)

(OUT/"vercel.json").write_text('{\n  "cleanUrls": true,\n  "trailingSlash": false\n}\n')
print(f"built index.html + {len(EX)} case pages + vercel.json")
