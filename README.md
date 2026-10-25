# Nuclear Medicine Atlas

A single-file, offline-capable, evidence-graded nuclear medicine reference —
274 pages across 25 chapters, interactive calculators, a study/mock-exam
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

## How it is published

`nuc.med` is built and deployed by GitHub Actions (`.github/workflows/pages.yml`) on every
push to `main`. The workflow runs `build_site.py` with `STATIC_PAGES_DIR=_site` — which also
writes a crawlable copy of every entry at `https://nuc.med/<id>/` — then runs `validate.py`
(a failed check stops the deploy), and publishes the app, the static pages, `legal/`,
`assets/`, `robots.txt` and `sitemap.xml`.

`SITE_URL` and `CONTACT_EMAIL` at the top of `build_site.py` set the canonical address and the
corrections address. The committed `index.html` / `nuclear-medicine-atlas.html` are an
offline copy only; the live site is always rebuilt from `content/`.

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
