---
type: reference
title: About & Methodology
chapter: boards
order: 5
subtitle: What this atlas is, how it is organized and graded, how to cite it, and how it stays current
aliases: [about, methodology, how to cite, editorial policy, framework, evidence grading, contributing, scope, colophon]
review_status: physician-reviewed
last_updated: 2026-07-28
reading_time: "6 min"
tags: [reference, methodology, editorial]
related_tracers: []
related_diseases: []
related_protocols: []
related_calculators: []
---

## Quick Answer

The Nuclear Medicine Atlas is a single, self-contained reference intended to be **exhaustive enough for a practising nuclear medicine physician and high-yield enough for a resident preparing for boards**. It is written in original prose, organized on an original **Six-Domain framework**, graded for evidence strength, and built by a reproducible pipeline from plain-text source so it can be maintained and extended over many years. This page states the editorial method so the resource can be judged, cited, and contributed to transparently.

## The Six-Domain framework

{K} The atlas is organized not by textbook tradition but by the **causal arc of a nuclear medicine study** — how the signal is made, what carries it, what it reveals, how it treats, how we read it, and how we quantify and verify it. Each domain has a single inclusion rule, so there is never ambiguity about where a new page belongs and the taxonomy scales without reorganization.

- **I · Foundations** — *how the signal is made.* Physics, radiobiology, instrumentation, image formation.
- **II · Probes & Targets** — *what carries the signal.* Radiochemistry, radiopharmacy, and molecular targets/mechanism classes.
- **III · Clinical Systems** — *what the signal reveals.* Diagnostic application by organ system.
- **IV · Therapy & Theranostics** — *how the signal treats.* Radionuclide therapy and imaging–therapy pairs.
- **V · Interpretation & Reasoning** — *how we read it.* Finding-driven patterns, variants, artifacts, structured reporting, response criteria.
- **VI · Dosimetry, Safety & Evidence** — *how we quantify, protect and verify.* The quantitative, regulatory, and evidentiary layer — deliberately the home for the fastest-changing facts, so the stable core rarely moves.

## How evidence is graded

{H} Every substantive clinical claim carries a grade so the reader can weigh it:

- **A** — a randomized trial or meta-analysis of randomized trials.
- **B** — a large cohort (roughly >400 patients) or a society guideline / procedure standard.
- **C** — a smaller or confounded cohort, or physiologic reasoning without outcome data.
- **INF** — *not a grade.* It marks a conclusion drawn by reasoning where no study addresses the question directly, so inference is never disguised as evidence.

## How emphasis encodes yield

The atlas uses a four-level emphasis hierarchy so the essentials stay prominent as pages go deep: a **KEY POINT** callout is the single must-know takeaway on a page; **bold** text marks high-yield, board-relevant facts; standard text is core detail; and smaller grey text is deeper reference detail. A **high-yield reading mode** (a toggle in the sidebar) collapses every page to just its key points, high-yield facts, tables, and self-checks — turning the physician reference into a resident cram sheet without duplicating content.

## Review status and provenance

Each page shows its **last-updated date** and a **review-status badge**. *AI-drafted* marks a page compiled from public primary literature and society guidance but not yet independently verified by a subject-matter expert; *Physician-reviewed* marks a page that has been checked by one. These labels are deliberately visible so the reader always knows the standard of assurance behind a page, and so the resource can move page-by-page from drafted to reviewed over time.

## Scope and limitations

{H} This atlas is compiled from **public, primary literature and society guidelines, expressed in original prose**. It is a reference and an educational resource — it **supports but does not replace** clinical judgement, local protocol, institutional dosimetry, or a written directive. Drug names, doses, thresholds, approvals, and trial results are **time-sensitive**; the fastest-changing of these are concentrated in Domain VI, but every such fact should be confirmed against current primary sources and local practice at the time of use. Nothing here is individualized medical advice.

## How to cite

Each page carries a copy-ready citation and a stable in-document permalink of the form `#/<page-id>`, so a specific page can be linked and referenced directly. A citation names the atlas, the page title, the version, and the build date — for example: *Nuclear Medicine Atlas. "Superscan." v1.0, 2026-07-28. Permalink #/superscan.* Versioning is explicit (shown on the home page and footer) so a reader always knows which edition they are reading.

## How the atlas stays maintainable

{D} The entire resource is generated by a reproducible build from plain-text Markdown, and every page is **self-describing**: its domain, order, evidence, and provenance live in the page's own front-matter, so adding or moving a page means editing exactly one file — there is no central registry to keep in sync. A validation harness runs after every build and fails loudly on broken navigation, un-rendered content, missing self-checks or citations, or JavaScript errors, and it reports content-aging health (what is oldest, what remains unreviewed). Together these make the atlas contributable and self-monitoring — the properties a reference needs to remain trustworthy as it grows.

## Self-Check

<details><summary><strong>Q1.</strong> What organizing principle underlies the Six-Domain framework?</summary>
<p><strong>Answer:</strong> The <strong>causal arc of a nuclear medicine study</strong> — how the signal is made (I), what carries it (II), what it reveals (III), how it treats (IV), how we read it (V), and how we quantify and verify it (VI) — with each domain given a single inclusion rule so the taxonomy scales without reorganization.</p>
</details>

<details><summary><strong>Q2.</strong> What does the "INF" label mean, and why is it kept distinct from A/B/C?</summary>
<p><strong>Answer:</strong> INF marks a conclusion reached by <strong>reasoning where no study addresses the question directly</strong>. It is deliberately <strong>not</strong> a grade, so inference is never disguised as graded evidence.</p>
</details>

<details><summary><strong>Q3.</strong> What is the difference between the AI-drafted and Physician-reviewed badges?</summary>
<p><strong>Answer:</strong> <strong>AI-drafted</strong> = compiled from public primary literature/guidance but not yet independently verified by a subject-matter expert; <strong>Physician-reviewed</strong> = checked by one. The badges keep the standard of assurance visible per page.</p>
</details>

<details><summary><strong>Q4.</strong> Why is adding a new page low-risk under the current design?</summary>
<p><strong>Answer:</strong> Because each page is <strong>self-describing</strong> — its domain, order, evidence, and provenance live in its own front-matter, so there is no central registry to keep in sync — and a <strong>validation harness</strong> checks every build for broken navigation, missing content, and errors.</p>
</details>

## Key References
- This page describes the atlas's own editorial method; the substantive clinical references are cited on their respective pages.
