---
type: reference
title: "Contribute to the Atlas: Author Guide"
chapter: articles
order: 1
subtitle: How to submit a contributed article, how authorship and provenance work, and the editorial standards every entry meets
aliases: [author guidelines, contribute, submission guide, how to contribute, editorial standards, authorship, provenance, write for the atlas, contributor guide]
review_status: physician-reviewed
last_updated: 2026-07-29
tags: [scholarship, authorship, editorial, guide]
---

## What a contributed article is

{K} A contributed article is a **focused synthesis** — a few well-referenced sections in which a physician or scientist distills their area and, crucially, **connects it back to the atlas**. It is not a textbook chapter and not an opinion piece: it is a compact, evidence-graded argument that *updates* specific atlas pages. The system is built so that authorship and provenance are **fully derived** — you declare who wrote it and what it informs, and the build wires the credit, the back-links, and the author profile automatically. Nothing is hand-maintained.

## The provenance loop

{H} When your article names the pages it `informs:`, the build creates a **bidirectional link**: your article lists the sections it updates at the bottom, and each of those atlas pages gains an **"Informed by contributed research"** banner linking back to your article. Your article also aggregates onto your **author profile**. The effect is that a reader on a clinical page sees the scholarship behind it, and a reader of your article can jump straight to the sections it touches — a citation graph that maintains itself.

## Front-matter — the part that wires everything

Every article begins with a YAML front-matter block. The fields that drive the system:

| Field | Purpose |
|---|---|
| `type: article` | Marks the page as a contributed article (renders the author/publication header) |
| `title:` / `subtitle:` | The article's title and one-line summary |
| `authors: [id, …]` | Author profile IDs — each must match a file in the contributors section |
| `informs: [page-id, …]` | The atlas pages this work updates — each gets the back-link banner |
| `journal:` / `pub_date:` | The publication line shown at the top |
| `review_status:` | Set to `physician-reviewed` once vetted |
| `related_diseases:` etc. | Optional curated cross-links, same as any page |

A matching **author profile** (a short bio page with `credentials`, `role`, `affiliation`, and `orcid`) lives in the contributors section; the ORCID renders as a verifiable outbound link.

## Editorial standards

{H} Every entry — contributed or core — meets the same bar:

- **Evidence-graded claims.** Significant assertions carry a grade: **A** (high-quality/RCT), **B** (guideline/cohort), **C** (limited), or **INFERENCE** (reasoned from mechanism, labeled as such). Never present inference as data.
- **Verified references only.** Cite primary literature and society guidelines. **Do not fabricate DOIs or citations** — every DOI must resolve to the stated article. When in doubt, cite the guideline body and title without a URL rather than guess one.
- **Accurate, current, and honest about uncertainty.** State what is established, what is emerging, and what is debated. Present the counter-argument where one exists.
- **Physician-reviewed** before `review_status` is set — the review confirms clinical accuracy and that claims match their grade.

## House style

{D} Match the atlas voice so contributions read as one work:

- **Yield tokens** at the start of a paragraph or bullet mark emphasis: &#123;K&#125; → a key-point callout, &#123;H&#125; → a high-yield bold line, &#123;D&#125; → a small detail note. They must sit at the very start of the line with a blank line before them.
- **Prose over lists** for explanation; tables for structured comparisons; a short **Self-Check** (`<details>` Q&A) where the content supports it.
- **Link internally** with `[text](#/page-id)` so readers can follow the thread.
- Keep it **focused** — one clear argument, a handful of sections, and the pages it informs.

## How to submit

{K} Send your draft as a Markdown file with the front-matter above (or an outline plus your references and we'll format it), along with your author-profile details (name, credentials, role, affiliation, ORCID) and the list of atlas pages you believe your work informs. On acceptance and physician review, your article and profile join the **Scholarship & Community** section and the provenance banners appear on the pages you updated — with your name on the work.

## See it in practice

- The worked example: **[Dual-Tracer Selection for PSMA Radioligand Therapy](#/dual-tracer-selection-rlt)** — a real, referenced article that demonstrates the `authors:`/`informs:` loop end to end.
- A template profile: the example contributor page in the **Contributors** section.
