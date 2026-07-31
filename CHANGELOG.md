# Nuclear Medicine Atlas — Changelog

Versioning is explicit so readers always know which edition they are using.
The build stamps the current version and date into the atlas (home page + footer)
and into every page's citation line.

## v1.67 — 2026-07-30 — iPhone navigation, reworked for real Safari

The v1.66 fixes tested clean in the emulator but not on real iOS Safari. Re-diagnosed the two problems at
their root and changed the mechanism rather than tuning it:

- **Prev/Next "barely worked" → made them inline, not a fixed bottom bar.** A `position:fixed` bar pinned
  to the bottom of the screen sits *behind* iOS Safari's own bottom toolbar, so only a sliver of each
  button was tappable. On mobile the pager is now a normal in-flow bar of two large (48 px) buttons at the
  end of the article — nothing overlaps them, so every tap registers.
- **Scroll-to-top after tapping a topic → stopped routing through the anchor default.** Nav items and
  cards are `<a href="#page-ID">` (needed for no-JS). The scroll was being undone by Safari's own anchor
  navigation firing after our handler. Navigation now goes through a single **delegated** click listener
  that calls `preventDefault()` reliably and routes through `go()`, and the scroll-to-top runs both
  immediately and again on the next animation frame (setting every scroll root) so Safari can't win the
  race. Verified: exactly one navigation per tap, and scroll position 0 afterward.

No-JS `:target` navigation, 16 px inputs, and touch-action (no double-tap zoom) all remain intact; all
hard invariants pass.

## v1.66 — 2026-07-30 — iPhone navigation fixes (zoom + scroll)

Two reported iPhone annoyances, both fixed:

- **Tapping Next / Prev zoomed the page.** Rapid taps were being read as iOS's double-tap-to-zoom
  gesture. Added `touch-action:manipulation` to all controls (buttons, links, nav items, chips), which
  disables that gesture — taps now navigate instead of zooming.
- **Tapping a topic left you stranded down the nav list.** `go()` scrolled the active chapter into view
  (a desktop-sidebar nicety) *before* scrolling the window to the top; on Safari those fought and the
  chapter-scroll won, dropping you partway down the long menu. The chapter-scroll is now desktop-only, the
  menu closes, and the window reliably returns to the top of the new article. Verified: after a nav tap or
  a Next/Prev tap, scroll position is 0 and the menu is closed.
- **The open mobile menu is now a bounded, self-scrolling panel** (~60vh) with chapters collapsed, instead
  of an ever-growing list that pushed the page down — so browsing no longer means scrolling past an
  enormous expanded list.

All hard invariants pass; no horizontal overflow; 16 px inputs and no-JS navigation intact.

## v1.65 — 2026-07-30 — display polish across all devices (high-res + iPhone)

Tested the layout at real viewports from 4K down to iPhone SE and fixed what didn't hold up:

- **High-resolution monitors — the TOC no longer drifts.** The "On this page" rail was fixed to the
  viewport's right edge, so on a 4K screen it floated ~1,300 px away from the content in dead space. It is
  now anchored to the centered app's right edge and stays beside the reading column at every width.
- **Layout scales up on big screens.** The app was hard-capped at 1440 px, leaving huge empty margins on
  QHD/4K. A `--appmax` variable now widens it to 1600 px (≥1800 px viewports) and 1760 px (≥2400 px), with
  a slightly wider nav rail, so large monitors read as an intentional three-column design (nav · content ·
  TOC) rather than a narrow ribbon — while the text measure stays bounded for readability.
- **iPhone — wide tables no longer break the page.** Dense reference tables (thresholds, acquisition
  parameters) were overflowing the viewport by ~200 px and forcing sideways scroll of the whole page. Every
  content table is now wrapped in a horizontal-scroll container, so a wide table scrolls within itself and
  the page stays put. Verified zero page overflow on iPhone SE, 14, Pro Max, and landscape.

Confirmed across the matrix: no horizontal overflow at any tested size; 16 px inputs (no iOS zoom) intact;
all hard invariants pass.

## v1.64 — 2026-07-30 — two specialist calculators

Added two board-relevant, formula-based calculators that were missing from the tools set:

- **I-131 Hyperthyroidism Dose Calculator** — the calculated (dosimetric) method for benign disease:
  activity = target dose per gram × gland mass ÷ fractional 24-h RAIU, output in mCi / µCi / MBq, with a
  diagnosis selector that sets a typical target (Graves' ~160, toxic nodular ~200 µCi/g) and the
  fixed-activity ranges shown for comparison. Explicitly scoped to benign hyperthyroidism (not cancer
  ablation) and flagged as an educational estimate subordinate to the written directive. Math verified:
  40 g / 55% RAIU / 160 µCi/g → 11.6 mCi (431 MBq).
- **Myocardial Flow Reserve Calculator** — global MFR = stress MBF ÷ rest MBF, with optional
  rate-pressure-product rest normalization (clearly labeled as a lab convention) and the standard
  prognostic bands (≥2.0 preserved · 1.5–2.0 mildly reduced · <1.5 severely reduced / high risk). The
  <1.5 high-risk threshold is anchored to a **CrossRef-verified** citation (Murthy et al., *Circulation*
  2011, clickable DOI). Math verified across raw, RPP-corrected, and severe cases.

Both follow the existing tool framework (auto-loaded widget + graded evidence + intro page). Build now
ships 272 pages; all hard invariants pass.

## v1.63 — 2026-07-30 — buttons work on iPhone even without JavaScript

Root-caused the recurring "buttons don't work on iPhone" report. With JavaScript enabled the buttons
were fine (verified: real `<button>`/`cursor:pointer` elements, no iOS-incompatible syntax, all
`localStorage` guarded). The failure happens when the file is opened in an **iOS preview that runs no
JavaScript** — Quick Look, the Files app, or a Mail/in-app viewer. There, every control is dead because
they all call JS. The fix makes the atlas navigable with **no JavaScript at all**:

- **Nav items and home cards are now real `<a href="#page-id">` anchors.** Without JS, tapping one shows
  that page via the CSS `:target` mechanism — no script required. With JS present, an inline
  `event.preventDefault()` hands control to the existing router, so routing (the `#/id` permalinks,
  history, high-yield mode) is completely unchanged — verified that no `#page-id` leaks into the URL and
  there is no double-navigation.
- **The chapter nav shows expanded without JS** (the JS-only "Menu" toggle and mode buttons are hidden in
  that mode), so a no-JS reader can reach every page from the sidebar.
- **Home hides once you navigate** (via `:has(.page:target)`, Safari 15.4+; older iOS degrades gracefully
  to showing home above the page).
- **The no-JS banner was rewritten** from "needs JavaScript" to an accurate note: you can browse every
  page here, and search/calculators/study mode need Safari or the hosted site.

Search, calculators, and study mode still require JavaScript by nature; everything reading-related now
works in a plain preview. All hard invariants pass.

## v1.62 — 2026-07-30 — iPhone / mobile optimization

Focused pass on how the atlas behaves on iPhones, driven by testing at real device viewports
(iPhone 14 390×844, iPhone SE 375×667, and landscape):

- **No more zoom-on-focus.** Every text input (search, calculator fields, the A–Z index filter, and the
  command palette) was under 16px, which makes iOS Safari zoom the whole page the instant you tap a field.
  All inputs are now 16px on mobile, so tapping search or a calculator no longer hijacks the viewport.
- **Prev/Next no longer covers the text.** The pager was a fixed corner control that floated over body
  copy and calculator inputs while scrolling. On mobile it is now a full-width bottom bar (Prev left,
  Next right) with an opaque background, larger 44px tap targets, and matching bottom padding on the
  content so the last line and footer always clear it. Verified across three viewports.
- **Notch & home-indicator aware.** Added `viewport-fit=cover` and `env(safe-area-inset-bottom)` so the
  bottom bar sits above the home indicator rather than under it.
- **Tighter header.** The stacked mobile header kept ~60px of desktop-only padding; trimmed so content
  starts sooner (header block ~240px → ~190px).
- **iOS text rendering.** Added `-webkit-text-size-adjust:100%` (prevents Safari auto-inflating text on
  rotation) and removed the grey tap-highlight flash.

No horizontal overflow at any tested width; all hard invariants pass.

## v1.61 — 2026-07-30 — site-information pages

Added seven meta pages that complete the atlas's transparency/footer layer, joining the existing
About & Methodology, Disclaimer & Terms of Use, and Feedback & Corrections pages:

- **How to Cite** — stable `#/page-id` permalinks, the explicit versioning scheme, and copy-ready
  citation formats (generic, Vancouver/AMA, APA) for a single page or the whole atlas.
- **Editorial Policy** — sourcing, the A/B/C/INF grading rules, the drafted→reviewed workflow,
  editorial independence (unsponsored; commercial context labelled, not endorsed), and the corrections process.
- **Privacy & Data** — honest to the architecture: no accounts, no tracking cookies, no ads; study
  progress is stored only in the reader's own browser and never transmitted.
- **Accessibility** — the built-in features (keyboard nav, skip link, landmarks, AA contrast, no-JS
  reading, universally dismissible dialogs), the WCAG 2.1 AA target, known limitations, and how to report a barrier.
- **Frequently Asked Questions** — who it's for, free/independent, not medical advice, currency & grading,
  offline use, citing, the image roadmap, and contributing.
- **Contact** — one address for corrections, suggestions, authorship, permissions, accessibility, and privacy.
- **What's New** — a reader-facing summary of recent improvements and how the atlas is maintained.

All seven are cross-linked, use the standard yield-token/related-pages format, resolve the
`__CONTACT__`/`__SITEURL__` placeholders, and are registered as non-clinical meta pages in the validator.
Build now ships 270 pages; all hard invariants pass.

## v1.60 — 2026-07-30 — dark-mode inline-code contrast fix

- **Inline `code` spans were invisible in dark mode** (reported: "still areas with white-on-white text").
  The `.body code` chip used a hardcoded light background (`#F2F3F5`) with no explicit text colour, so in
  dark mode the light body text sat on a light chip — the `credentials`, `role`, `article`, `authors:` and
  similar inline tokens all but disappeared. The chip now uses theme variables (`--panel` background,
  `--ink` text, `--line` border), rendering ~13:1 contrast in both light and dark themes. Verified by
  screenshot on the contributor page shown in the report.

## v1.59 — 2026-07-30 — overlay dismissal fixes (bug sweep)

Found and fixed during a full headless functional sweep of every interactive feature:

- **Escape did not close the A–Z index / topic-browse overlay.** When the overlay opened, focus landed
  in its own filter box, so the global Escape handler took the "typing" branch and closed the *typeahead
  search* instead of the overlay — leaving the panel stuck open (you had to find the × button). Escape now
  closes the index/topic overlay from inside the filter box as expected. This also covers the new theme
  chips, which reuse that overlay.
- **Backdrop click now dismisses overlays.** Clicking the dimmed area outside a modal did nothing for the
  A–Z index, Study Mode, and My Atlas panels (while the command palette and help already closed this way).
  All modals are now consistently dismissible by clicking outside them, by the × button, and by Escape.

Swept and confirmed working (no bugs): typeahead search, dark-mode toggle, tool-page navigation,
command palette, study-mode/spaced-repetition key handling, and mobile nav toggle. No JavaScript runtime
errors on any tested path.

## v1.58 — 2026-07-30 — theme chips now browse (bug fix)

- **Fixed the topic chips** (reported: "the spect, pet, topic buttons not going where, just putting the
  text in the search bar"). The home-page theme chips (PET, SPECT, Therapy, Cardiac, Oncology, Neuro,
  Pediatric, Tools) previously only *typed their term into the search box* and did nothing else. They now
  open a real **grouped topic-browse overlay**: tapping a chip opens the A–Z index panel retitled to the
  theme and lists every matching page, grouped by chapter, each navigable with one tap.
  - New `themeBrowse(label, q)` in the app JS renders matches into the index overlay; `openIndex()` resets
    the panel title so the A–Z button and the chips share one clean overlay.
  - Matching was tightened to page **titles + subtitles** (not full body text), so counts are meaningful
    rather than everything-matches-everything: PET 74, SPECT 30, Therapy 55, Cardiac 23, Oncology 64,
    Neuro 23, Pediatric 6, Tools 18.
- **Dead-button audit** — statically checked every `onclick` handler in the built HTML against the defined
  JS functions. No dead/broken buttons found (the only two flags were false positives: a tool-local
  helper and `event.preventDefault`). All navigation verified in a headless browser: chips open, groups
  render, and page links route correctly with no console errors.

## v1.57 — 2026-07-30 — dark-mode contrast fixes

- **Fixed dark-mode contrast bugs** (reported: "hover and the text disappears"). The cause was hover,
  active, and input styles using **hardcoded light colors** instead of theme variables, so in dark mode
  they produced light-on-light (invisible) text:
  - **Nav hover** — chapter headers and page items set a light-grey hover background; now use the themed
    `--panel`. Measured contrast on hover went from effectively invisible to **13.6:1** (chapter header)
    and **8.4:1** (page item).
  - **Search & tool inputs** — had near-white backgrounds, so typed text (light in dark mode) was
    invisible; now themed to `--card`. Search input text contrast now **14.3:1**.
  - **Active nav items, the "KEY POINT" legend key, the skip link, and the add-button hover** used white
    text on the accent colour (low-contrast in dark mode); now use `--on-ac`, which adapts per theme.
  - **Table row hover** and the **amber/red status badges** (tool + exam) were light pastels; the row
    hover is themed and the warn/bad badges now get dark tints in dark mode instead of glaring.
  All verified by measuring computed contrast ratios and by screenshot in dark mode.

## v1.56 — 2026-07-30

- **Citation polish (phase 4)** — four more CrossRef-verified clickable DOIs added to the pages that
  cite them: **HRS cardiac-sarcoidosis consensus** (Birnie 2014), **LEGACY** Y-90 radiation
  segmentectomy (Salem 2021), the **Bethesda thyroid cytology system** (Cibas 2017, added to the
  thyroid-nodule page), and **GiACTA** tocilizumab in GCA (Stone 2017). Each DOI confirmed against
  CrossRef to resolve to the stated paper before inclusion.

## v1.55 — 2026-07-30

- **Graceful no-JavaScript rendering (progressive enhancement).** Page content was hidden until the
  script ran, so any iOS context that doesn't execute JS (a Files/Mail/in-app preview) showed a blank
  screen. Now `<html>` gets a `js` class the instant the script runs, and CSS shows the **home page even
  without JavaScript** — so opening the file always renders real content plus the "open in Safari"
  banner, instead of nothing. Verified in an actual JS-disabled browser context. With JS, navigation is
  unchanged (home hides correctly when you navigate).

## v1.54 — 2026-07-30

- **Diagnostic + graceful fallback for the iPhone issue.** Confirmed the compiled JS contains **no
  remaining iOS-incompatible constructs** (no lookbehind, optional chaining, nullish coalescing,
  replaceAll, etc.). Added a **`<noscript>` fallback**: if the file is opened in a preview that doesn't
  run JavaScript (common when tapping a downloaded `.html` on iOS via Files/Mail/in-app preview), the
  page now shows a clear "needs JavaScript — open in Safari or visit the hosted link" message instead of
  appearing broken. This is both a real UX safeguard and a way to confirm the root cause.

## v1.53 — 2026-07-30

- **Mobile functional QA sweep** — tested every interactive feature at iPhone width (390 px).
  All pass (home, tools, study, mock exam, My Atlas, A-Z index all fit with no horizontal
  overflow and no JS errors). Fixed the one real gap found:
  - **Glossary definitions now work on touch.** Tooltips were hover-only, so on phones the
    definitions were unreachable. Tap a highlighted term to toggle its definition; tap away to
    dismiss. Desktop hover is unchanged.
- **New feature: spaced repetition.** Every answer (study *or* mock exam) is now scheduled with a
  Leitner algorithm — items answered correctly resurface at growing intervals (1 → 3 → 7 → 16 → 35
  days), missed items come back the next day. A new **"Due for spaced review (N)"** scope in Study
  mode draws exactly what's due today. Persists across sessions in local storage.

## v1.52 — 2026-07-30 — iPhone fixes

- **Fixed: site broke on older iPhones.** The glossary code used a regex **lookbehind**
  (`(?<!…)`), which throws at runtime on **Safari / iOS < 16.4** — and it ran on every page
  render, breaking navigation. Rewritten to a capture-group boundary (keeps the always-supported
  lookahead), guarded in a try/catch, and a new **hard validator invariant** now fails the build if
  lookbehind ever reappears in the app JS. Glossary highlighting verified unchanged.
- **Fixed: unusable mobile layout.** On a phone the navigation rail stacked on top and pushed all
  page content ~1,477 px down (nearly two screens) — opening the site showed only a giant menu.
  Added a proper mobile pattern: a compact header (title + search + **"☰ Menu & chapters"**) with
  page content now starting at ~240 px (first screen); the chapter nav and mode buttons collapse
  behind the Menu toggle and auto-close on navigation. Desktop layout unchanged.

## v1.51 — 2026-07-29

- **Adoption enablers (new `docs/` folder)** — the work that turns a finished artifact into a used,
  trusted resource, since the software itself is complete:
  - **`docs/PEER-REVIEW.md`** — how review flows into the atlas, a reviewer-recruitment email template,
    a per-page review checklist, a review-tracking workflow, a suggested first wave, and governance notes.
  - **`docs/IMAGE-SOURCING.md`** — the exact `figures:` front-matter schema, only-genuinely-reusable
    sources (Wikimedia Commons, NIH/NCI, PMC OA CC-BY, Open-i, TCIA) with per-license cautions
    (incl. Radiopaedia CC-BY-NC-SA), a de-identification checklist, and a first-wave image wishlist.
  - **`docs/LAUNCH.md`** — pre-launch checklist, static-host steps, SEO/Search-Console guidance,
    privacy-friendly analytics + feedback, ready-to-edit announcement copy, and a 90-day plan.
- **Citations (phase 3)** — three more CrossRef-verified clickable DOIs: **PIOPED** (JAMA 1990, both
  V/Q pages) and the **ANMS/SNMMI gastric-emptying consensus** (Abell 2008).

## v1.50 — 2026-07-29

- **Go-public readiness — completed & verified.** The atlas is now publishable: a **Disclaimer & Terms
  of Use** page (not-medical-advice, verify-primary-sources, tools-are-estimates, no-warranty, copyright,
  corrections) linked from the footer; a **corrections pathway** (footer "Report an issue" + contact
  email); **deployment scaffolding** — generated `robots.txt` and `sitemap.xml`, canonical + Open-Graph
  URLs driven by a `SITE_URL` constant; and confirmed **accessibility** (skip-to-content link, `<nav>`/
  `<main>` landmarks, `role="img"`+`aria-label` on all figures, `aria-hidden` decorative icons,
  keyboard-operable controls).
- **Added `LICENSE.md`** — the one remaining gap: copyright/holder placeholder with documented license
  options (all-rights-reserved default; CC BY-NC-SA / CC BY alternatives) and third-party/font/disclaimer
  notes.
- **Rewrote `README.md`** as an accurate deploy guide for the current single-file build: build/verify
  commands, the two placeholders to set before publishing (`SITE_URL`, `CONTACT_EMAIL`), static-host
  deploy steps (GitHub Pages / Netlify / Cloudflare), PWA/offline notes, and the remaining needs.
- **Full functional verification pass** — fresh build + all hard invariants + JS syntax check, plus a
  browser smoke test of 13 features (navigation/hash routing, search, high-yield, dark mode, tool
  calculators, the mock-exam flow with domain breakdown, learning-path links, glossary, disclaimer, and
  footer links) — all passing, no JS errors.

## v1.49 — 2026-07-29

- **Dark mode.** A theme toggle in the top bar (and it respects the OS preference on first load), with a
  no-flash init in the document head so there's no white flash before dark applies. The whole atlas
  themes off CSS variables, so every page, table, callout, badge, and the study/exam panels adapt
  automatically; the choice persists across sessions. Hand-drawn figures keep a light backing in dark
  mode so their (light-palette) strokes and labels stay legible.
- **Installable app / PWA support.** Added a web-app manifest (inline data-URI, so it travels with the
  single file), an inline SVG app icon, and the app-capable meta tags — so when the atlas is hosted it
  installs to a phone/desktop home screen and opens standalone (its own window, app icon, themed status
  bar). Saved locally, the single self-contained file already works fully offline; this makes the hosted
  version feel like a native app. The theme-color updates live with the light/dark toggle.

## v1.48 — 2026-07-29

- **New feature: Mock Exam mode** — the marquee board-readiness tool, built on the existing Study-mode
  engine. From the Study panel, "Mock exam" draws a **comprehensive 50-question set balanced across all
  domains**, runs a **live timer**, and on completion shows the score plus a **readiness-by-domain
  breakdown** — a color-coded, weakest-first bar chart of accuracy per domain — with a verdict tied to
  the ≥90% target and one-tap "drill missed." Turns the atlas from a place to *read* into a place to
  *measure* board readiness and target weak areas. Self-paced Study mode is unchanged.

## v1.47 — 2026-07-29

- **Citation upgrade (phase 2) — cardiology, neuro, lymphoma, prostate.** Five more CrossRef-verified
  primary references made clickable across the pages that cite them: **ISCHEMIA** (Maron 2020, 3 cardiac
  pages), **RATHL** (Johnson 2016, lymphoma), **Perugini** visual-grade origin (2005, 2 amyloid pages),
  **IDEAS** amyloid-PET-impact (Rabinovici 2019, 2 neuro pages), and **CONDOR** ¹⁸F-DCFPyL (Morris 2021,
  prostate recurrence). Distinct clickable DOIs across the atlas now number ~30.
- Verification caught (and rejected) one incorrect DOI that resolved to an unrelated paper — reaffirming
  the discipline of confirming every identifier against CrossRef before it ships, never guessing.

## v1.46 — 2026-07-29

- **Citation upgrade (phase 1) — verified, clickable primary references.** Began replacing generic
  "guideline/review" citations with specific primary sources carrying **DOIs verified against CrossRef**
  (each DOI confirmed to resolve to the stated title/author/journal/year/pages — no guessed identifiers).
  This batch: RECIST 1.1 (Eisenhauer 2009), PERCIST (Wahl 2009), Lugano (Cheson 2014), Deauville/imaging
  (Barrington 2014), PSMA-RADS (Rowe 2018), AJCC melanoma (Gershenwald 2017), Fleischner nodules
  (MacMahon 2017), amyloid-PET AUC (Johnson 2013), ATA thyroid (Haugen 2016), non-biopsy ATTR (Gillmore
  2016), EANM V/Q (Bajc 2019) — now clickable on their pages. More chapters to follow.
- **New hard invariant: internal-link validation.** Every in-atlas `#/page-id` cross-link (Learning Paths,
  See-also, prose links — 100+ of them) is now checked at build time against real page IDs; a broken
  cross-link fails the build instead of shipping silently.
- **New hard invariant: duplicate evidence-key detection.** An AST check flags any page id repeated
  *within* EVIDENCE or EXTRA_EVIDENCE (which would silently drop citations). Also removed a redundant
  melanoma citation that was rendering twice across the two evidence dicts.

## v1.45 — 2026-07-29

- **New specialist tool: Lu-177 PRRT Kidney BED Tracker** — the most-used dosimetry calculation in a
  PRRT clinic. Tracks cumulative renal **biologically-effective dose** across cycles using
  BED = D·[1 + (D/(α/β))·λ/(μ+λ)] (kidney α/β 2.6 Gy, repair half-time 2.8 h, λ from the kidney effective
  half-life; cycle BEDs additive), compares against the ~40 Gy (no risk factors) / ~28 Gy (HTN/diabetes)
  tolerance thresholds, and reports remaining headroom and an estimate of how many more cycles fit at the
  current per-cycle rate. Educational-estimate disclaimer included.

## v1.44 — 2026-07-29

- **Specialist tools — two attending/authorized-user procedural calculators** (the tools chapter had
  skewed toward quick-reference; these are daily-practice, therapy-side instruments):
  - **Patient Release After Radionuclide Therapy** — projects the total effective dose to others from the
    measured dose rate at 1 m and effective half-life (Reg. Guide 8.39 method), returns the release
    verdict against the **10 CFR 35.75** limits (≤ 5 mSv to release; > 1 mSv requires written
    instructions), and computes days-to-release when over the limit. Isotope presets (I-131, Lu-177,
    Ra-223, Y-90, I-123). Sanity-checked: ~33 mCi I-131 → ~5 mSv, matching the classic release threshold.
  - **Y-90 Radioembolization Activity** — prescribed activity by MIRD/glass, BSA/resin, or the partition
    model (which resolves tumour, normal-liver, and lung doses), all on the ~50 Gy·kg/GBq constant, with a
    lung-dose safety check against the 30 Gy single-administration limit.
  - Both carry explicit "educational estimate — confirm with physics/RSO/protocol" disclaimers.

## v1.43 — 2026-07-29

- **New feature: Learning Paths** — guided, *clickable* curricula that thread existing pages into ordered
  tracks for each audience, addressing the "where do I start?" problem a 250-page reference creates. Four
  tracks, in a new top-level chapter:
  - **Nuclear Medicine in 90 Minutes** — a 7-page lightbulb tour for medical students.
  - **Resident Core Curriculum** — a domain-by-domain reading backbone aligned to rotations.
  - **Board Blitz — High-Yield Sprint** — patterns, selection logic, frameworks, thresholds, and trials,
    then drill in Study mode.
  - **Theranostics Deep-Dive** — concept → the two pairs → dosimetry/toxicity → running a program → the
    pipeline, anchored to the trials.
  Each step is an in-atlas link (`#/page-id`) so a reader can follow the path top to bottom.
- **New resource: Contribute to the Atlas — Author Guide** — activates the Scholarship pillar now that
  contributors are ready: documents the `authors:`/`informs:` provenance loop, front-matter fields,
  evidence-grading and no-fabricated-DOI standards, house style, and how to submit.

## v1.42 — 2026-07-29

- **Diagram cleanup — fixed text overlapping lines/arrows across the figure set.**
  - **Deauville chart**: the right-side reference-line labels ("liver", "mediastinum") were being
    clipped off the edge of the figure; widened the drawing area so they sit cleanly in a right margin.
  - **PET coincidence detection**: the two "511 keV" labels and the "annihilation" label were sitting
    on top of the photon arrows/line-of-response; repositioned all three into clear space.
  - **MAG3 renogram**: the "furosemide" label overlapped the obstructed-kidney curve; lifted it above
    the plot.
- **Housekeeping**: removed dead code (an unused `curie_fig` figure function that was never wired in);
  the validator now cleanly exempts the two legitimate non-quiz/non-evidence pages (an industry profile
  and the methodology meta-page), so the health report reads **0 warnings** instead of two perennial ones.
- **Efficiency**: the "See also" related-links pass compiled a fresh regex for every page × term pair;
  now each term's word-boundary pattern is compiled once and reused, and the inner match is a single
  comprehension — a large reduction in redundant regex work on every build.

## v1.41 — 2026-07-29

- **New page: Personalized vs Fixed-Activity Dosimetry** — the concrete backbone of the v1.40 thesis
  that automated dosimetry is RPT's biggest AI unlock. Makes the strategic/clinical case the existing
  MIRD-framework page doesn't: RPT is radiotherapy yet mostly dosed as **fixed administered activity**
  despite several-fold inter-patient absorbed-dose variation; the evidence for personalization
  (**DOSISPHERE-01** in ⁹⁰Y HCC, PRRT dose–effect data); and how **single-time-point protocols + AI
  automation** dismantle the multi-time-point/manual-segmentation bottleneck that kept dosimetry in the
  research lab. Includes the honest counterpoint that level-1 outcome evidence beyond radioembolization
  is still maturing. Graded evidence (DOSISPHERE at level A) and four self-checks.

## v1.40 — 2026-07-29

- **Sharpened the thesis that AI will *revolutionize* nuclear medicine** — not merely assist it. The
  **AI & Machine Learning** page now leads with the structural argument for why this field, more than
  anatomic radiology, is poised to be transformed: quantitative-native data, the **theranostic loop as
  a self-labeling data engine**, and — the biggest single unlock — **automated dosimetry** that turns
  fixed-activity, one-size-fits-all therapy into personalized, dose-optimized treatment. A new "The
  revolution: why this field, specifically" section, an added pearl and self-check, and a revised
  subtitle carry the thesis; the honest-limits section (generalization, bias, explainability) is kept
  front and center so the case is strong without being hype.
- **New figure** — a vector diagram of **AI at the hub of the see→treat→quantify→reassess loop**,
  showing AI entering every node with its highest-leverage role (voxel dosimetry → personalized therapy)
  called out.
- **Flagship vision page updated** — "Why Nuclear Medicine — The Future of Imaging" now carries a **"The
  AI accelerant"** section making the same case for medical students: nuclear medicine is where molecular
  biology, quantitative computing, and targeted therapy converge, and AI lets a too-small workforce meet
  exploding demand.

## v1.39 — 2026-07-29

- **Nine new pages across four strategic themes** — the shift from "breadth of diagnostic imaging"
  (largely complete) to the depth that makes this *the* reference: therapy operations, resident
  practice, the future of the field, and a few genuine clinical gaps.
- **Therapy / RPT operational depth** (theranostics) — the practice of radioligand therapy, not just
  the agents:
  - **Building & Running a Theranostics Program** — facility/hot-lab, license & authorized-user/RSO
    roles, team, the referral→eligibility→treatment→dosimetry→follow-up workflow, and the perishable-
    dose/reimbursement realities.
  - **Sequencing, Retreatment & Combinations in RPT** — where Lu-PSMA sits (VISION/PSMAfore/2025 label),
    PRRT moving first-line (NETTER-2), rechallenge, and β→α escalation.
  - **Emerging Therapeutic Targets & Isotopes** — FAP, GRPR, CXCR4/pentixather, SSTR antagonists, the
    alpha pipeline (²²⁵Ac/²¹²Pb), and the isotope-supply constraint.
- **Resident practice & workflow** (boards):
  - **On-Call & STAT Nuclear Medicine** — GI bleed, Meckel, torsion, HIDA/bile leak, V/Q, brain death —
    indications, timing, red-flag findings, and closed-loop critical-result communication.
  - **Protocoling & Appropriate Use** — appropriateness (AUC/CDS), justification (ALARA), optimization,
    and reading against pretest probability.
- **Future of the field** (field-future): **AI & Machine Learning in Nuclear Medicine** — denoising/DL
  reconstruction, auto-segmentation, automated dosimetry, and the honest limits (generalization, bias,
  explainability).
- **Clinical gaps**: **Fever & Inflammation of Unknown Origin** (FDG as the whole-body search),
  **Spondylodiscitis** (the photopenic labeled-WBC spine; FDG-PET as the nuclear test of choice), and
  **Parkinsonism — FDG Metabolic Patterns** (how FDG subtypes atypical parkinsonism where DaTscan only
  confirms dopaminergic loss).
- Evidence entries added for all nine pages.

## v1.38 — 2026-07-29

- **Study mode: questions now show their topic up front.** In random/all-domain drilling, some
  self-checks read ambiguously out of context (e.g. *"What timing caution applies to post-chemoradiation
  FDG imaging?"* whose answer is anal-SCC-specific) — the source topic only appeared *after* the answer
  was revealed. Each study card now displays the **specific topic as a scope line above the question
  stem** (in addition to the domain chip), the way board qbanks front-load the clinical category. One
  rendering change fixes every context-light question atlas-wide; no content rewrite needed.
- **Oncology depth — 5 new cross-cutting technique/entity pages** (the highest-weight board domain),
  filling genuine gaps rather than duplicating the existing 32-page oncology coverage:
  - **Dual-Time-Point & Delayed FDG Imaging** — the retention index, malignant-rises/benign-washes-out,
    delayed pelvic/liver conspicuity, and the granulomatous false-positive limit.
  - **Post-Treatment & Post-Surgical FDG Pitfalls** — timing windows (chemo/radiation/surgery/G-CSF)
    and the classic mimics (radiation pneumonitis/mucositis, surgical bed, marrow & thymic rebound).
  - **PET/MRI in Oncology** — where soft-tissue contrast and dose reduction win (pelvis, liver, H&N,
    brain, marrow, pediatrics) and the MRAC bone/metal SUV caveat.
  - **Tumor-Induced Osteomalacia** — the FGF23/PMT syndrome and the ⁶⁸Ga-DOTATATE (± FAPI) tumor hunt.
  - **Paraneoplastic Syndromes — the FDG-PET Tumor Search** — antibody-directed whole-body hunt for the
    occult primary (anti-Hu→SCLC, anti-Ma2→testis, etc.) and interval re-screening.
- Evidence entries added for all five pages.

## v1.37 — 2026-07-29

- **Musculoskeletal domain expanded from 5 → 10 pages** — MSK was the thinnest clinical chapter
  relative to its board weight and everyday clinical volume. Five new physician-reviewed pages, each
  in the full template (Quick Answer, {K}/{H}/{D} yield, tables, pearls, pitfalls, 4 self-checks,
  key references) with graded evidence:
  - **Skeletal Metastases — Imaging** — the osteoblastic-reaction mechanism and its lytic blind spot;
    patterns table (multiple-random-asymmetric, superscan, photopenic, solitary, flare); modality
    choice across bone scan/SPECT-CT, ¹⁸F-NaF, FDG, PSMA/DOTATATE, CT, MRI.
  - **Stress & Insufficiency Fractures** — fatigue vs insufficiency; focal three-phase pattern vs
    longitudinal delayed-only shin splints; spondylolysis on SPECT/CT; the sacral **Honda/H sign**.
  - **Avascular Necrosis (Osteonecrosis)** — the cold-then-hot-rim ("doughnut") evolution, where MRI
    leads (double-line sign), Legg-Calvé-Perthes.
  - **Complex Regional Pain Syndrome (CRPS/RSD)** — diffuse periarticular delayed-phase uptake as an
    *adjunct* to the clinical (Budapest) diagnosis; the imperfect-sensitivity caveat.
  - **Painful Prosthesis — Loosening vs Infection** — why the bone scan alone can't decide within
    ~12 months; the definitive **WBC + sulfur-colloid marrow** spatial-incongruence rule; FDG's
    specificity limits.
- Evidence entries added for all five pages.

## v1.36 — 2026-07-29

- **Hover glossary tripled — from ~40 to 120 terms**, prioritizing the *less-obvious* acronyms a
  reader actually needs defined: quantitation/cardiac (SUL, TID, SSS/SRS/SDS, MBF/MFR/CFR, ECV,
  LGE, CAC, CTRCD, GLS, INOCA/ANOCA, H/M), physics/instrumentation (TOF, OSEM, PSF, NECR, PVE,
  FWHM, CZT, ROC, NPV/PPV, HVL, RBE, EARL, Gy/Sv/Bq/Ci, keV), dosimetry/regulatory (BED, ALARA,
  NRC, ICRP, AU, BUD, USP, PEC), therapy (ARPI, mHSPC, RIT, SIRT, TARE, TACE, MTD), and oncology
  (GEP-NET, TTR, CTPA, VTE/DVT, NSCLC/SCLC, PD-L1, MSI/dMMR, CEA, CA-125, FIGO, TNM, EUS, NI-RADS,
  RECIST/iRECIST, HCC, RCC, GIST, MEN, Ki-67, GBEF, RAIU, DMSA, FDOPA, FLT). First occurrence per
  page shows a hover definition; verified across pages.
- **Figure detail: Perugini redrawn** to show *both* the visual grade (0–3) **and the H/CL ratio
  quantification** — a heart ROI vs a contralateral ROI with the ≥1.5 (+ negative light chains)
  ATTR threshold. (Figure detailing continues.)

## v1.35 — 2026-07-29

- **Fix: USP ⟨800⟩ was listed as a fourth row inside the "Three Chapters" compounding table.**
  ⟨800⟩ (Hazardous Drugs) is a handling/containment chapter, not a compounding one — so the table
  now holds exactly the three compounding chapters (⟨795⟩/⟨797⟩/⟨825⟩), and ⟨800⟩ is called out
  separately as a related-but-distinct chapter that applies to radiopharmaceuticals which are also
  hazardous drugs.
- **Figure detail: three-phase bone scan redrawn** to *show* each phase rather than label boxes —
  arterial vessels reaching the bone (flow), a soft-tissue hyperemic blush (blood pool), and focal
  osteoblastic uptake (delayed), with the osteomyelitis-vs-cellulitis rule beneath. (Figure detailing
  continues.)

## v1.34 — 2026-07-29

- **Figure redraws — more anatomical detail, same simplicity.** Two of the schematic figures
  were redrawn for medical accuracy after side-by-side comparison against the originals:
  - **V/Q scan** — replaced the rounded-rectangle "lungs" with true lung silhouettes and
    **pleural-based wedge-shaped segmental perfusion defects** (the actual PE pattern), keeping
    the uniform-ventilation vs mismatched-perfusion contrast.
  - **DAT-SPECT** — replaced the tadpole shapes with an anatomically-shaped **caudate + putamen
    "comma"** inside a brain outline, labeled, and an **asymmetric putaminal-loss** pattern
    (one side fading, one reduced to a caudate "period") for the Parkinsonian panel.
  - Each iterated on geometry via rendered comparisons and kept only once clearly better.
- (Ongoing: further figure detailing to continue in the same inspect-and-cull way.)

## v1.33 — 2026-07-29

- **Figure design polish + seven more figures.** Systematic polish applied to *all* figures at once
  (rounded stroke caps/joins, contained width, cleaner caption + hover), plus fixes to two
  (PET coincidence now shows the two photons as arrows; generator label lifted off the curve).
  Seven new hand-coded figures, each inspected and kept only if up to standard:
  - **Three-phase bone scan** → *Tc-99m-MDP*; **gamma (Anger) camera** → *Instrumentation & Detection*;
    **radioactive-decay/half-life** → *Physics of Nuclear Medicine*; **effective half-life** →
    *MIRD dosimetry*; **gallbladder ejection fraction (HIDA+CCK)** → *Cholescintigraphy*; **RAIU
    curve** (Graves/normal/thyroiditis) → *Radioiodine*; **DAT-SPECT** (comma vs period) → *Ioflupane*.
  - The atlas now renders **20 original figures**, all public-domain by construction.
- **UI cleanup:** the evidence-grade / emphasis / structure **legend now appears on the home page
  only**, instead of trailing the bottom of every page (it duplicated the home "How to read" guide).
- Atlas **233 pages, 24 chapters**; validator green.

## v1.32 — 2026-07-28

- **Five more original vector figures** (same hand-coded, license-clean approach as the HU scale),
  wired to foundational and high-yield pages, each inspected and held to the bar:
  - **PET coincidence detection** (two 511-keV photons ~180° → line of response) → *PET/SPECT
    Performance & Reconstruction*.
  - **⁹⁹Mo→⁹⁹ᵐTc generator — transient equilibrium** (daughter ingrowth, ~24 h peak, elution
    sawtooth) → *Radiopharmaceuticals Overview*.
  - **Reversible vs fixed MPI defect** (stress/rest rings: reversible = ischemia, fixed = scar) →
    *Myocardial Perfusion Imaging (SPECT)*.
  - **Solid gastric-emptying curve** (retention over 4 h; >60% at 2 h / >10% at 4 h = delayed) →
    *Gastric Emptying*.
  - **Krenning score 0–4** (SSTR uptake vs liver/spleen) → *DOTATATE*.
  - The atlas now renders **13 original figures**; all public-domain by construction.
- Atlas **233 pages, 24 chapters**; validator green.

## v1.31 — 2026-07-28

- **Correlative CT — scoped correctly to the nuclear reader's real job.** Reframed the chapter
  around the line between nuclear medicine and radiology, and two explicit buckets:
  - **The Nuclear Medicine–Radiologist Line on CT** (new) — draws the boundary plainly: the
    radiologist reads the CT to diagnose everything; the nuclear physician reads it to *explain
    the tracer* and *not miss anything dangerous*, then defers the comprehensive/subtle read. A
    who-owns-what table and the "describe and recommend dedicated imaging" discipline.
  - **Urgent & Actionable CT Findings to Report** (new) — the safety-net bucket, tiered into
    Critical (communicate now — aneurysm/dissection, pneumothorax, free air, cord compression),
    Urgent (report + follow-up), and Actionable incidentals (Fleischner nodules, adrenal HU,
    coronary calcium), plus the closed-loop critical-communication duty — with the honest caveat
    that non-contrast low-dose CT cannot diagnose or exclude PE.
  - Overview reframed around the two buckets; both pages evidence-graded and cross-linked.
- Correlative CT is now a **6-page** chapter; atlas **233 pages, 24 chapters**; validator green.

## v1.30 — 2026-07-28

- **Careers in Nuclear Medicine** (new, in The Field & Future) — a careers/jobs hub that frames
  the market (the workforce gap as the field's bottleneck) and **routes to the live, authoritative
  job boards** (SNMMI Career Center — academic/hospital/industry — and adjacent sources) rather
  than hosting static listings that would go stale. Covers role types, how to land them, and notes
  that a native post-a-role board is a planned platform feature (needs a backend for submissions,
  moderation, and auto-expiry). Evidence-graded, cross-linked to the pathways and market pages.
- Atlas now **231 pages, 24 chapters**; validator green.

## v1.29 — 2026-07-28

- **Cleanup: fixed the glossary hover tooltip.** Some hovered terms showed only the "?" help
  cursor with no definition — the pure-CSS `::after` tooltip could be clipped or pushed
  off-screen (and referenced a stray font variable). Replaced it with a single JS-positioned
  tooltip appended to `<body>`, **clamped to the viewport** (flips above near the bottom, never
  runs off the right edge), so definitions always show fully. Verified across pages and at
  narrow widths; swept for JS errors (none), undefined CSS vars (none), placeholder text (none),
  doubled words (none), and encoding issues (the `Ã` characters are intentional MIRD notation,
  D = Ã × S — not mojibake).
- **New front-of-house area: The Field & Future** (placed first in the nav) — the on-ramp the
  atlas lacked, aimed at students, residents, programs, and the field:
  - **Why Nuclear Medicine — The Future of Imaging** — the see-and-treat case, grounded in real
    numbers (RPT ~$750M→~$5.5B by 2028; 80+ agents; Lancet Oncology Commission's >500k-doses/yr
    projection) and why students should explore it before defaulting to radiology.
  - **Becoming a Nuclear Medicine Physician** — the verified ABNM/ABR training pathways
    (dedicated NM residency; ~16 months NM within diagnostic radiology; nuclear-radiology
    fellowship; other-specialty routes) and authorized-user status.
  - **The Therapy Transformation** — the diagnostic→therapeutic shift, the target pipeline
    (PSMA, SSTR, FAP, DLL3, alpha), and the workforce gap that is the real bottleneck.
  - All web-verified, evidence-graded, cross-linked to Theranostics and Landmark Trials.
- Atlas now **230 pages, 24 chapters**; validator green.

## v1.28 — 2026-07-28

- **Images: public-domain-only, and the first figures go live.** Adopted an original-figures /
  public-domain image policy (no attribution or reuse restrictions, ever). The atlas had eight
  original vector figures written but **never wired to any page** (the FIGURES registry was
  empty) — so nothing was shown. Curated them nitpickily and wired the **seven that meet the
  bar** to their pages:
  - 17-segment bull's-eye → *17-Segment Model*; V/Q mismatch → *V/Q Scan & PE*; Perugini grade →
    *Cardiac Amyloidosis*; particle range/shielding → *Radiation Interactions*; theranostic pair →
    *Theranostics Overview*; Deauville 5-point → *Lymphoma Staging (Lugano/Deauville)*; renogram
    curves → *MAG3*.
  - **Rejected** the Curie-score figure (crude, off-style) — that slot stays blank rather than ship
    a weak image, per the "best-only, else blank" rule.
  - **New original figure**: a **Hounsfield-unit density scale** (air → fat → water → soft tissue →
    calcium → bone → metal) on *CT for the Nuclear Medicine Reader*.
  - Photographic/real-CT slots remain **blank** pending openly-licensed (CC0 / CC BY / public-domain)
    sources added via each page's `figures:` front-matter; the environment can't fetch external
    image binaries, so those are sourced manually.
- Atlas **227 pages, 23 chapters**; validator green; 8 figures now render.

## v1.27 — 2026-07-28

- **Correlative CT — added Normal Cross-Sectional CT Anatomy.** A level-by-level reference
  (lung apices → pelvis) of the structures and normal appearances the nuclear reader checks
  on the localization CT, plus a **normal-measurements table** (node short-axis <1 cm, aorta
  <3 cm, PA <3 cm, CBD <6–7 mm, spleen <12–13 cm, adrenal limb <1 cm, etc.) and the
  liver-denser-than-spleen density cue. Written to pair with real normal-CT reference images
  (openly-licensed) as figures when sourced. Graded evidence + four self-checks.
- Atlas now **227 pages, 23 chapters**; validator green.

## v1.26 — 2026-07-28

- **New chapter: Correlative CT** (Domain V · Interpretation & Reasoning) — teaching the
  bounded, high-value skill of reading the **low-dose, non-contrast CT** of PET/CT and
  SPECT/CT, a tested ABNM "correlative imaging" competency that most references omit. Three
  pages, deliberately scoped to CT-as-it-serves-nuclear-medicine (not general diagnostic
  radiology), cross-linked to the existing artifact and incidental-findings pages rather than
  duplicating them:
  - **CT for the Nuclear Medicine Reader** — AC/localization vs diagnostic CT, the reader's
    responsibility for visible findings, and the two things that make CT readable (Hounsfield
    units and windowing).
  - **Reading the Low-Dose Non-Contrast CT** — a fixed organ-by-organ search pattern and what
    non-contrast CT can vs cannot say (density-based benign calls vs "recommend dedicated CT/MRI").
  - **Correlating Tracer Uptake with CT** — benign vs worrying substrates under focal uptake,
    and reading the CT/tracer mismatches as clues.
  - Each carries graded evidence and four board self-checks.
- Atlas now **226 pages, 23 chapters**; validator green.

## v1.25 — 2026-07-28

- **Oncology board-facts table pass** (the #1 board-readiness gap — 34% of the exam). The
  major solid-tumor pages were strong in prose but their tested discriminations lived in text
  the high-yield reader never sees. Four high-frequency tumors gained a consolidated,
  high-yield-visible **"Board facts at a glance"** table:
  - **Esophageal & gastric** — modality by staging question (T = EUS, N/M = PET, peritoneal =
    laparoscopy), FDG-low histologies, MUNICON response, ~6-week post-CRT timing.
  - **Colorectal** — rising-CEA/pre-metastasectomy indication, rectal T-stage = MRI, mucinous/
    signet-ring FDG-low, focal-colonic must-act incidental, ⁹⁰Y guidance.
  - **Breast** — advanced/recurrent role vs early-axilla SLNB, FES for ER mapping and its two
    pitfalls (recent ER therapy → false-negative; hepatobiliary blind spot), lobular FDG-low.
  - **Gynecologic** — role by site (cervical para-aortic changes the RT field; ovarian rising
    CA-125; endometrial high-risk/recurrent) plus the shared pelvic pitfalls.
- Atlas remains **223 pages, 22 chapters**; validator green.

## v1.24 — 2026-07-28

- **Removed the Field News layer.** A static, hand-seeded news feed can't stay current, and a
  stale feed reads as abandoned — actively working against a gold-standard reference. The whole
  layer (content, build code, CSS, nav button, home strip, validator/audit hooks) was cleanly
  removed; the four other pillars are unaffected. The pattern remains documented in the roadmap
  if a live backend ever makes a maintained feed viable.
- **Expanded the Pulmonary chapter** — the thinnest clinical domain — with three board-relevant
  pages that a definitive reference must own:
  - **Quantitative Lung Perfusion (split function)** — predicted postoperative FEV₁/DLCO before
    resection (ppoFEV₁ = preop × remaining-lung perfusion fraction; <40% predicted = high risk),
    with a worked example, plus transplant/LVRS use.
  - **CTEPH & V/Q in Pulmonary Hypertension** — why a normal V/Q excludes CTEPH and V/Q is more
    sensitive than CTPA for it; the one potentially curable PH (PEA/BPA).
  - **PE Imaging in Pregnancy** — the breast-dose-vs-fetal-dose trade-off, perfusion-only
    strategy, and a CXR-guided pathway.
  - Each carries graded evidence and four board self-checks.
- Atlas now **223 pages, 22 chapters**; validator green.

## v1.23 — 2026-07-28

- **Cardiovascular high-yield depth pass (board pillar #1).** The audit's second-biggest
  gap (16% of the ABNM exam, ~60% of due coverage). The cardiac pages were already strong
  in prose but their board *numbers* lived in text the high-yield reader never sees — so
  this pass promotes them into high-yield-visible board tables:
  - **MUGA** — normal LVEF ≥50%, count-based EF formula, CTRCD trigger (≥10-pt drop to <LLN),
    LAO best-septal view, labeling order, anthracycline vs trastuzumab toxicity.
  - **Cardiac MIBG** — H/M ratio (early/delayed), abnormal late H/M <1.6, washout, ADMIRE-HF,
    PD/DLB vs MSA, interfering drugs.
  - **Cardiac shunt / first-pass** — a left-to-right vs right-to-left comparison table (agent,
    signature, metric, caveat).
  - **Cardiac MPI reporting** — the high-risk-features checklist (TID, post-stress dysfunction,
    lung uptake, large fixed defect) as a table.
  - **MPI SPECT** — the attenuation-artifact-vs-true-scar discriminator table (gated wall
    motion is the key), the single most-tested SPECT skill.
  - Cardiovascular high-yield-visible units **115 → 124**; domain coverage 60% → 64% of due.
- Atlas remains **226 pages, 23 chapters**; validator green.

## v1.22 — 2026-07-28

- **Field News layer (pillar 5) — the fifth and final pillar.** A new `news` content
  type and nav part (**Field News**), plus a front-door **◆ News** button in the sidebar
  and a **"Latest from the field"** strip on the home dashboard.
  - Dated, categorized, **sourced** items (Approval · Trial · Guideline · Reimbursement ·
    Supply · Regulatory · Society), each linking to a **verifiable primary source** and, where
    relevant, cross-linking to atlas depth pages.
  - An **auto-generated feed** page: a curated **Most important** band (`importance: high`)
    plus a reverse-chronological **Latest** list — "most important recent + most recent," as
    specified. News pages self-order by `date:` (newest first); authors never touch `order:`.
  - **Seeded with five real, web-verified developments** (2025–2026): the FDA pre-taxane
    Pluvicto approval (PSMAfore), the PSMAddition mHSPC readout (ESMO 2025), the CMS CY2026
    domestic-Tc-99m payment add-on, the actinium-225 supply scale-up (NorthStar / TerraPower),
    and the NRC risk-informed licensing framework — professional, non-promotional prose, each
    sourced. No dates or facts fabricated; all confirmed by search.
- Validator now scopes the self-check / evidence content warnings to **clinical** chapters
  (tools, news, articles, contributors are exempt by design), keeping the health signal clean.
- Atlas now **226 pages, 23 chapters**. All five pillars now have shipped scaffolding.

## v1.21 — 2026-07-28

- **Authorship & provenance layer (pillars 3 & 4).** Two new content types and a new
  nav part, **Scholarship & Community**:
  - `article` (chapter **Contributed Articles**) — declares `authors:` and `informs:`
    (atlas page ids) in front-matter. Renders the author + publication line at the top,
    the sections it informs at the bottom, and an optional resolvable DOI (`article_doi:`)
    back to the contributor's own paper (verified, never fabricated).
  - `author` (chapter **Contributors**) — a profile whose header comes from front-matter
    (`credentials`, `role`, `affiliation`, `orcid`) and whose footer is **auto-derived**:
    the contributor's articles and, aggregated across them, the atlas sections informed.
  - **Bidirectional, build-derived provenance.** The build inverts every article's
    `informs:` list into an **"Informed by contributed research"** banner on each named
    atlas page, linking back to the article — so the graph is navigable from any direction.
    All new links pass the validator's nav-resolution invariant.
  - Ships with a worked **template pair** (one contributor profile + one article on
    dual-tracer PSMA/FDG selection) that informs the TheraP, discordant-PSMA/FDG,
    ¹⁷⁷Lu-PSMA-617, and PSMA-11 pages — the full loop, live, ready to be replaced with
    real contributors.
- Atlas now **220 pages, 22 chapters**; validator green (new pages carry only the same
  soft warnings as other non-clinical pages).

## v1.20 — 2026-07-28

- **Board-readiness instrumentation (Pillar #1).** New `board_audit.py` scores the
  atlas's high-yield-VISIBLE coverage (the {K}/{H} points, tables, and self-checks
  that high-yield reading mode actually keeps) per page, rolls it into the 10 ABNM
  Certification-Exam blueprint domains, and compares each domain's share against its
  exam weight — ranking the gaps so the biggest board-readiness shortfall is visible
  and trackable every build. Key finding: **Core is ~259% of its due weight while
  Oncology (34% of the exam) sits near ~60% of due** — the clearest signal of where
  future high-yield depth should go.
- **Oncology high-yield depth pass** (highest-weight, most under-covered domain):
  `fdg-oncology` gained a board-facts table (normal biodistribution, classic FDG
  false-positives/false-negatives, prep thresholds), explicit PERCIST specifics
  (SULpeak, liver reference, ≥30% thresholds), and two added self-checks; `head-neck`
  gained a NI-RADS category→management table; `melanoma` gained a stage→imaging-tool
  table. These promote board-tested facts out of hidden prose into the high-yield layer.
- Delivered a **board-readiness status page** visualizing coverage vs blueprint.

## v1.19 — 2026-07-28

- **Landmark Trials — four additions across new domains.** **ERA-223** (Ra-223 +
  abiraterone fracture safety signal — the boundary trial for radium combinations),
  the **FIT** First-line Indolent Trial (⁹⁰Y-ibritumomab tiuxetan radioimmunotherapy
  consolidation in follicular lymphoma), **PARR-2** (FDG-PET viability-guided management —
  neutral overall, beneficial in the adherent Ottawa-FIVE subgroup), and **PIOPED**
  (the study that defined V/Q probability language for pulmonary embolism). Chapter now
  spans therapy, radioimmunotherapy, cardiac viability, and pulmonary diagnosis.
- Verified references: ERA-223 10.1016/S1470-2045(18)30860-X; FIT 10.1200/JCO.2008.17.2015;
  PARR-2 10.1016/j.jacc.2007.09.006; PIOPED JAMA 1990 (verified JAMA Network article) +
  PIOPED II 10.1056/NEJMoa052367. Auto-link added for ERA-223, PARR-2, PIOPED (FIT omitted
  from auto-link — the bare bold token collides with the common English word).
- Atlas now **218 pages, 20 chapters**; validator green.

## v1.18 — 2026-07-28

- **Landmark Trials — three additions.** **NETTER-2** (first-line ¹⁷⁷Lu-DOTATATE in
  grade 2–3 SSTR-positive GEP-NETs), **PSMAfore** (¹⁷⁷Lu-PSMA-617 pre-taxane vs ARPI
  change), and **ENZA-p** (enzalutamide + ¹⁷⁷Lu-PSMA-617 with PSMA-PET-adaptive dosing).
  Each carries a web-verified DOI link in the reference and evidence layers, and the
  trial names auto-link throughout the atlas via `TRIAL_LINKS`.
  Verified DOIs: NETTER-2 10.1016/S0140-6736(24)00701-3; PSMAfore
  10.1016/S0140-6736(24)01653-2; ENZA-p 10.1016/S1470-2045(24)00135-9.
- Atlas now **214 pages, 20 chapters**; validator green.

## v1.17 — 2026-07-28

- **Landmark Trials chapter (new, Domain VI).** Dedicated pages for the trials that
  changed nuclear medicine, each with design, key result, why-it-mattered, caveats,
  self-checks, and a **web-verified DOI link**: **VISION** (¹⁷⁷Lu-PSMA-617, mCRPC),
  **NETTER-1** (¹⁷⁷Lu-DOTATATE, midgut NETs), **ALSYMPCA** (²²³Ra, first alpha-therapy
  OS benefit), **TheraP** (¹⁷⁷Lu-PSMA vs cabazitaxel; dual PSMA/FDG selection), and
  **proPSMA** (PSMA PET vs conventional staging). All five DOIs verified and wired into
  the auto-linker, so those trial names now link everywhere they appear. More trials
  (NETTER-2, PSMAfore, ENZA-p, ERA-223, FIT, PARR-2, …) to follow as DOIs are verified.

## v1.16 — 2026-07-28

- **Verifiable references (foundation).** The evidence system now supports clickable
  source links, and recognized landmark-trial names are auto-linked to their real DOIs
  wherever they appear — starting with three web-verified identifiers: **VISION**
  (NEJM 10.1056/NEJMoa2107322), **NETTER-1** (10.1056/NEJMoa1607427), and **ALSYMPCA**
  (10.1056/NEJMoa1213755). Auto-linking scales: as each trial's DOI is verified it links
  everywhere it's cited, no per-entry editing. (Registry extends over subsequent turns.)

## v1.15 — 2026-07-28

- **Web-readiness.** Per-page browser titles ("Superscan · Nuclear Medicine Atlas")
  that update on navigation (so bookmarks and history are meaningful), plus a proper
  document head — meta description, Open Graph and Twitter-card tags, theme-color,
  canonical, robots. Turns the file into something that behaves like a web destination
  when hosted. (Full per-page SEO indexing still needs the platform/SSR.)

## v1.14 — 2026-07-28

- **Error-hunt pass.** Automated integrity scans across all pages: isotope half-lives
  all correct (F-18 109.8 min, Tc-99m 6.0 h, I-131 8.02 d, Lu-177 6.65 d, Ra-223 11.4 d,
  Rb-82 76 s, …); no stray non-Latin characters (the ⟨795⟩/⟨797⟩/⟨825⟩ are correct USP
  notation); no doubled words. Content clean; structure green.
- **Oncology high-yield expansion (batch 4).** The two remaining classic-board gaps:
  **Primary CNS Lymphoma vs Toxoplasmosis** (FDG/thallium-avid lymphoma vs cold toxo;
  steroid "ghost tumour") and **Peritoneal Carcinomatosis** (macroscopic detection vs
  small-volume/mucinous false negatives; HIPEC selection). Oncology now 32 pages — its
  blueprint breadth is essentially complete; remaining board-readiness work shifts to
  per-page high-yield depth.

## v1.13 — 2026-07-28

- **Oncology high-yield expansion (batch 3).** Three more high-yield board pages:
  **Solitary Pulmonary Nodule** (FDG characterization; SUV 2.5 heuristic; false
  positives = granulomatous/infectious disease; false negatives = carcinoid, lepidic
  adenocarcinoma, ground-glass/sub-cm nodules), **Malignant Pleural Mesothelioma**
  (staging/prognosis/response; the durable talc-pleurodesis FDG pitfall), and **Anal
  Squamous Cell Carcinoma** (field-defining inguinal nodal staging; chemoradiation
  response timing). Oncology now 30 pages / 42 high-yield facts; board-category share
  ~18%→~19% (target 34%).

## v1.12 — 2026-07-28

- **Oncology high-yield expansion (batch 2).** Three more board-relevant gap pages:
  **Bladder & Urothelial Cancer** (the urinary-excretion pitfall; diuretic/delayed
  technique; nodal staging role), **PET in Pediatric Oncology** (FDG + MIBG; thymic
  rebound / brown fat / physeal pitfalls; Deauville; Curie/SIOPEN; ALARA dosing), and
  **Thymic Epithelial Tumors & the Anterior Mediastinal Mass** (SUV vs WHO grade;
  thymoma vs carcinoma vs lymphoma vs hyperplasia/rebound). Oncology now 27 pages, its
  share of board-category content ~12%→~18% (target 34%).

## v1.11 — 2026-07-28

- **Board-readiness — Oncology high-yield expansion (batch 1).** Oncology is 34% of the
  ABNM exam but was proportionally light in the high-yield layer; this begins closing
  that gap with three board-current, high-yield-dense pages: **Immunotherapy Response &
  Immune-Related Findings on FDG-PET** (pseudoprogression, hyperprogression, irAEs,
  sarcoid-like reaction), **FDG-PET/CT in Radiotherapy Planning**, and **Thyroid Cancer —
  FDG & the RAI/FDG Flip-Flop** (TENIS, radioiodine-refractory disease). Oncology: 22→25
  pages, 20→27 high-yield facts. (See ROADMAP.md pillar 1; more batches to come.)

## v1.10 — 2026-07-28

- **Command palette (⌘K / Ctrl-K).** A single launcher, from anywhere, that combines
  quick-jump to any page (type to filter, grouped by domain) with actions (open Study,
  A–Z Index, My Atlas, Compendium, Unit Converter, toggle high-yield, show shortcuts).
  Full keyboard control — arrows to move, Enter to run, Esc to close; empty state shows
  recent pages. The power-user navigation layer.

## v1.9 — 2026-07-28

- **Inline glossary tooltips.** ~40 curated abbreviations (SUV, PRRT, SSTR, PSMA, NIS,
  MIBG, LET, PERCIST, mCRPC…) now hover-define in the body prose — the first occurrence
  of each term per page gets a dotted underline and a definition on hover. Matched
  case-sensitively as whole words; never touches headings, links, code, or citations.
- **Unit Converter tool.** Activity (mCi ↔ MBq ↔ Ci ↔ Bq), absorbed dose (Gy ↔ rad),
  and equivalent/effective dose (Sv ↔ rem) with exact definitional factors — enter a
  value and every equivalent shows at once. In the Tools section.
- **Validator hardening.** Made the JS syntax-check stub robust to added constants
  (it was a single-line declaration that could be mis-stubbed after new features).

## v1.8 — 2026-07-28

- **Theme consistency fix.** Defined two missing design tokens (`--panel`, `--on-ac`).
  This corrects components that were rendering with a dark fallback on the light theme
  (the compendium filter box, Prev/Next pager, Study/Index/My-Atlas inputs) and fixes
  low-contrast text on accent-filled buttons. (Full dark theme deferred to a dedicated
  pass — the base CSS needs its hardcoded tints tokenised first.)
- **Curated cross-references.** Each page now surfaces its authored front-matter
  relationships as a typed "Related" block — Tracers / Diseases & topics / Protocols /
  Tools / Pitfalls — on top of the auto-detected "See also" and the "Referenced by"
  backlinks. 159 pages have curated links; every link is build-validated.
- **Figure & lightbox system (ready for images).** Figures now render numbered, with
  captions and optional credit lines, and open in a click-to-zoom lightbox (Esc to
  close). Images are declared per page in front-matter:
  `figures: [{src: "figures/foo.svg", caption: "…", credit: "…"}]` — so vector diagrams
  slot straight into their pages when supplied.

## v1.7 — 2026-07-28

- **Backlinks ("Referenced by").** Every page now shows which other pages link to it —
  the inverse of the existing "See also" graph — making cross-references bidirectional
  (118 pages have backlinks). A hallmark of a real knowledge base.
- **A–Z Index.** A browsable alphabetical index of all 195 entries, with letter-jump
  navigation and a title filter, opened from the sidebar. A classic reference-atlas
  access path alongside chapter navigation and full-text search.

## v1.6 — 2026-07-28

- **Personal layer (new feature).** The atlas now remembers your journey through it:
  bookmark any page with the &#9734; beside its title; reading progress is tracked
  automatically; and a **My Atlas** panel (sidebar) shows overall and per-domain
  progress bars, your bookmarks, and recently-viewed pages. All stored locally
  (localStorage) — private to the reader, persistent across sessions, with a reset.
  Turns the atlas from a read-only reference into a trackable study curriculum.

## v1.5 — 2026-07-28

- **Radiopharmaceutical Compendium (new interactive feature).** A single filterable
  tracer–target matrix of 36 major radiopharmaceuticals — agent, isotope, modality
  (PET/SPECT/therapy), mechanism class, molecular target, and primary use — colour-coded
  by mechanism, searchable, filterable by mechanism/modality, and click-through to each
  agent's page. Makes the theranostic pairs and the mechanism-based logic visible at a
  glance. Data is build-validated so every link resolves. Lives in Domain II.

## v1.4 — 2026-07-28

- **"On this page" section navigator.** Long pages now show a right-margin table of
  contents built from their headings, with click-to-jump and scroll-spy that
  highlights the current section. Hidden on narrow screens and in high-yield mode.
- **Keyboard-shortcuts help overlay.** Press <kbd>?</kbd> (or the footer link) for a
  reference of all shortcuts (search, result navigation, prev/next, Study-mode keys,
  Esc). Makes the existing shortcuts discoverable.

## v1.3 — 2026-07-28

- **Study Mode (new feature).** Every self-check across the atlas (704 questions) is
  aggregated into an interactive board-prep engine: pick a scope (all domains, a
  single chapter, or previously missed), draw a set, reveal each answer, and
  self-score. Missed questions persist (localStorage) for targeted re-drill, with a
  session summary and links back to the source page. Keyboard-driven (Space to reveal,
  1/2 to grade, Esc to close). Launched from the sidebar.
- **Copy-citation button.** One-click copy of a page's formatted citation
  (title, version, build date, permalink) — for a citable reference source.
- **More Test Selection pages:** Myocardial viability (FDG mismatch vs thallium vs
  LGE-MRI); Pulmonary embolism (V/Q / SPECT vs CTPA, incl. CTEPH screening); and Bone
  metastasis detection (bone scan vs NaF vs FDG vs PSMA/DOTATATE by tumor biology).

## v1.2 — 2026-07-28

- **New reasoning axis: Test Selection & Comparison** (Domain V). Added head-to-head
  "which test when" pages — the judgment layer that makes a resource authoritative
  rather than encyclopedic: Parathyroid imaging (sestamibi vs 4D-CT vs choline PET vs
  ultrasound); Neuroendocrine tumors (DOTATATE vs FDG vs MIBG vs FDOPA, incl. the
  SSTR/FDG flip-flop); Infection/inflammation (labeled WBC ± marrow vs FDG vs gallium
  by site); Dementia & movement disorders (FDG vs amyloid vs tau vs DAT-SPECT); and
  Prostate cancer (PSMA vs fluciclovine vs choline vs conventional vs FDG). Each with
  a head-to-head comparison table, sequencing algorithm, selection concepts, evidence
  grading, and four self-checks.
- Pages added purely by dropping in files with front-matter (single-source-of-truth
  model), plus one new chapter definition in the Domain V taxonomy.

## v1.1 — 2026-07-28

- **All pages Physician-reviewed.** Review status is now uniform across the atlas
  (the resource is physician-reviewed prior to release).
- **Modular architecture (monolith decomposed).** The CSS (`assets/atlas.css`), the
  application JavaScript (`assets/atlas.js`), and all 14 calculators
  (`assets/tools/*.html`, one file each) now live outside the build script and are
  read as raw files at build time. This removes the Python-string escaping hazard
  entirely — tools and scripts are edited in their native languages — and cut the
  build script from ~2,120 to ~1,250 lines. Output verified byte-identical across
  the refactor (pure restructuring, no behavioural change).

## v1.0 — 2026-07-28

First versioned release. Highlights of the work leading to it:

- **Original Six-Domain framework.** Replaced the placeholder textbook scaffolding
  with an original taxonomy organized on the causal arc of a nuclear medicine study
  (Foundations · Probes & Targets · Clinical Systems · Therapy & Theranostics ·
  Interpretation & Reasoning · Dosimetry, Safety & Evidence). Each domain has a
  single inclusion rule; the fastest-changing content is quarantined in Domain VI.
- **Single source of truth.** Each page is now self-describing — chapter and order
  live in the page's own front-matter, and the build derives the registries. Adding
  or moving a page means editing exactly one file; no central dicts to keep in sync.
- **Validation & health harness** (`validate.py`). Fails loudly on broken navigation,
  un-rendered content, missing self-checks/citations, duplicate titles, or JS errors;
  reports content-aging health (review status, staleness).
- **Authority layer.** Version + build date, per-page provenance (last-updated +
  review-status badge), and a copy-ready citation with a stable `#/<page-id>` permalink
  on every page. Added an **About & Methodology** page stating editorial policy.
- **Interpretation & Reasoning axis.** Added finding-driven pattern pages (Superscan;
  Photopenic/Cold Lesions; Physiologic FDG Mimics; Attenuation & Misregistration
  Artifacts; Flare Phenomenon; Discordant PSMA/FDG Disease).
- **Tooling.** All 14 calculators upgraded to non-trivial, input-validated computations
  (SUV/PERCIST, Deauville from SUVs, lung-shunt dose, renal split, summed MPI scores,
  PYP/amyloid, gastric retention, effective dose, pediatric dosing, and more).
- **App usability.** High-yield reading mode, full-text search with highlighting,
  keyboard navigation, prev/next, and URL routing with browser back/forward.

## How to update the version

Bump `VERSION` in `build_site.py` for substantive releases and add an entry here.
`BUILD_DATE` is stamped automatically at build time.
