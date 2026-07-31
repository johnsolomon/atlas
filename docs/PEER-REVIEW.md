# Peer-Review Packet

The atlas is content-complete and functional, but every page currently carries a
`review_status: physician-reviewed` tag that is **self-applied** — no named external
expert has yet vouched for it. Genuine, named peer review is the single biggest lever
for credibility with elite physicians and for citation. This packet is everything you
need to run that process.

---

## 1. How review flows into the atlas (already built)

The provenance system is in place; a review simply updates front-matter and, when a
reviewer contributes substantively, the authorship loop.

- **`review_status:`** on each page — set to `physician-reviewed` only after a named
  reviewer signs off (see the tracker below). Consider adding the reviewer's initials
  and date in the commit message.
- **`last_updated:`** — bump to the review date so `validate.py`'s staleness report
  stays honest.
- **Contributor profiles + `authors:` / `informs:`** — when a reviewer rewrites or
  substantially authors a section, add them as a contributor (see *Contribute to the
  Atlas* in the app) and list the pages their work `informs:`. The build then credits
  them and back-links automatically.
- **Corrections** flow through the footer "Report an issue" link / `CONTACT_EMAIL`.

Run `python3 validate.py` after any review edits — it reports review status counts and
flags anything stale.

---

## 2. Recruitment email (template)

> **Subject: Invitation to peer-review a section of the Nuclear Medicine Atlas**
>
> Dear Dr. [Name],
>
> I'm building the Nuclear Medicine Atlas — a free, evidence-graded reference spanning
> every major tracer, protocol, disease, and therapy, with interactive tools and a
> board-prep study engine. It's aimed at residents, attendings, and the fast-moving
> therapy side of the field.
>
> I'd be grateful if you would peer-review the **[chapter / N pages]** in your area of
> expertise (**[e.g., cardiac amyloidosis, PRRT dosimetry]**). Reviewing a page takes
> ~10–15 minutes against a short checklist (accuracy, evidence grade, currency, safety).
> Reviewers are **named and credited** on a contributor profile and on every page they
> vouch for, with an ORCID link.
>
> Estimated commitment: **[e.g., 6 pages, ~90 minutes]**, on your own schedule. I can
> send pages as a link or PDF, whichever you prefer.
>
> Would you be willing? Happy to answer any questions.
>
> With thanks,
> [Your name, credentials, affiliation]

**Where to find reviewers:** SNMMI / EANM committees and councils, your training-program
faculty, co-authors on the trials cited in the atlas, active voices on nuclear-medicine
professional forums, and subspecialty society leadership. Aim for **two independent
reviewers per clinical domain** where feasible.

---

## 3. Per-page review checklist

Ask each reviewer to rate every page on these, and note any required changes:

1. **Clinical accuracy** — Is every statement correct and current standard of care?
   Flag anything outdated, oversimplified to the point of error, or wrong.
2. **Evidence grade** — Do the graded claims (A/B/C/INFERENCE) match the strength of the
   cited source? Is anything presented as fact that is actually inference or debated?
3. **Citations** — Are the references appropriate and real? Should a landmark be added?
4. **Safety** — For therapy/dosimetry/dose pages: are thresholds, limits, and cautions
   correct and adequately caveated? (Especially the calculators and release/dosimetry pages.)
5. **Currency** — Any new approval, guideline, or trial since the `last_updated` date that
   should be reflected?
6. **Completeness & balance** — Any critical omission? Any claim needing a counterpoint?
7. **Verdict** — ☐ Approve as-is ☐ Approve with the noted edits ☐ Needs major revision.

A reviewer should be able to do this per page in ~10–15 minutes.

---

## 4. Review-tracking workflow

Keep a simple tracker (a spreadsheet or the table below in a working doc). Suggested columns:

| Page (id) | Domain | Reviewer | Date sent | Date returned | Verdict | Changes needed | Applied? | review_status set |
|---|---|---|---|---|---|---|---|---|

Process per page: **assign → reviewer completes checklist → you apply required edits →
bump `last_updated` and set `review_status: physician-reviewed` → mark applied.** Prioritize
the highest-traffic / highest-risk pages first: the **therapy & dosimetry** pages and their
calculators, the **oncology** workhorses, **cardiac**, and anything with a dose or safety
threshold.

**Suggested first wave (highest yield):** the Theranostics chapter + the three therapy
calculators (patient release, Y-90 activity, Lu-177 kidney BED); FDG oncology core;
nuclear cardiology core; radioiodine/thyroid; the reporting-criteria pages.

---

## 5. Governance notes

- **Conflicts of interest** — ask reviewers to disclose industry relationships; note them
  on the contributor profile where relevant.
- **Independence** — a page's author should not be its sole reviewer.
- **Re-review cadence** — set a review-refresh interval (e.g., every 12–24 months, sooner
  for fast-moving therapy pages). `validate.py`'s staleness report surfaces aging pages.
- **Disclaimer stands regardless** — review improves quality but the *Disclaimer & Terms
  of Use* (educational, not medical advice, verify against primary sources) always applies.
