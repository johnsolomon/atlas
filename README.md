# Nuclear Medicine Atlas

A single-file, offline-capable, evidence-graded nuclear medicine reference —
263 pages across 25 chapters, interactive calculators, a study/mock-exam
engine, guided learning paths, dark mode, and verified primary-source
citations. The entire site compiles to **one self-contained `nuclear-medicine-atlas.html`**.

## What's in this bundle

- `nuclear-medicine-atlas.html` — the compiled site (open it in any browser; works offline).
- `build_site.py` — the generator: turns `content/**/*.md` + `assets/` into the single HTML file, and emits `robots.txt` + `sitemap.xml`.
- `validate.py` — the health/QA harness (hard invariants + content report). Run after every build.
- `content/` — every page as Markdown with front-matter (the source of truth).
- `assets/` — `atlas.css`, `atlas.js`, and `assets/tools/*.html` (the interactive calculators).
- `CHANGELOG.md` — versioned release history.
- `LICENSE.md` — set the copyright holder / choose a license before publishing.

## Build & verify

```
python3 build_site.py      # writes nuclear-medicine-atlas.html, robots.txt, sitemap.xml
python3 validate.py        # must print "All hard invariants pass"
```

`validate.py` enforces: no un-rendered yield tokens, no broken internal
`#/page-id` links, no duplicate evidence keys, required front-matter, unique
titles, and a JS syntax check — plus a health report (review status, staleness,
evidence coverage).

## Before you publish — set two placeholders

In `build_site.py` (top of file):

- `SITE_URL` — the https origin you'll host at (e.g. `https://your-domain.org`). Drives the canonical link, Open Graph URL, `robots.txt`, and `sitemap.xml`.
- `CONTACT_EMAIL` — the address for the footer "Report an issue" / corrections link and the Disclaimer page.

Then rebuild. Also edit `LICENSE.md` (copyright holder / license choice) and
the **Disclaimer & Terms of Use** page if your terms differ.

## Deploy (it's a static site)

The output is a static file, so any static host works. Put
`nuclear-medicine-atlas.html` (renamed to `index.html`), `robots.txt`, and
`sitemap.xml` at the site root:

- **GitHub Pages** — commit to a repo, enable Pages on the branch/root.
- **Netlify / Cloudflare Pages / Vercel** — drag-and-drop the folder, or connect the repo (no build command needed; it's prebuilt).
- **Any web server** — copy the three files to the web root.

Add your custom domain in the host's dashboard, then set `SITE_URL` to match and rebuild.

### PWA / install
The build includes a web-app manifest, icon, and app-capable meta, so once
hosted over https the atlas installs to a phone/desktop home screen and opens
standalone. Saved locally, the single file already works fully offline (custom
fonts fall back to system fonts with no network).

## Editing content

Each page is a Markdown file in `content/<chapter>/` with front-matter
(`title`, `subtitle`, `chapter`, `order`, `review_status`, `last_updated`, …).
Add or edit a file, rebuild, and validate. New chapters are registered in the
`CHAPTERS` list in `build_site.py`. Contributed articles use the `authors:` /
`informs:` provenance system — see the **Contribute to the Atlas** page.

## The biggest remaining needs

- **Real scan images** — all figures are original vector schematics; licensed/CC0 scan images would elevate it.
- **Named expert peer review** — pages carry a `physician-reviewed` tag; genuine external review + named authorship is the credibility keystone (the contributor pipeline is built and waiting).
