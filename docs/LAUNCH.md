# Launch Kit

Everything to take the atlas from a finished file to a live, findable, improving site.

---

## 1. Pre-launch checklist

- [ ] Set **`SITE_URL`** and **`CONTACT_EMAIL`** at the top of `build_site.py`, then rebuild.
- [ ] Fill in the copyright holder / choose a license in **`LICENSE.md`**; reflect it in the footer + Disclaimer page if not all-rights-reserved.
- [ ] Read the **Disclaimer & Terms of Use** page and confirm it matches your terms.
- [ ] `python3 build_site.py && python3 validate.py` → must print **"All hard invariants pass."**
- [ ] Rename `nuclear-medicine-atlas.html` → **`index.html`**; place it with `robots.txt` and `sitemap.xml` at the web root.
- [ ] (Optional but recommended) at least a **first wave of peer review** on therapy/dosimetry pages before wide promotion (see `PEER-REVIEW.md`).

## 2. Hosting (pick one; all free for a static file)

- **GitHub Pages** — push the repo, Settings → Pages → deploy from branch root. Add a custom domain + enforce HTTPS.
- **Netlify / Cloudflare Pages / Vercel** — drag-and-drop the folder or connect the repo; no build command (it's prebuilt). Add domain in dashboard.
- After the domain is live, set `SITE_URL` to match and rebuild so canonical/OG/sitemap are correct.

## 3. SEO / discoverability

The whole atlas is one HTML document, so a crawler that fetches it indexes **all** the text — good for search. To maximize it:

- [ ] Confirm the `<title>`, meta description, canonical, and Open Graph tags render with your real domain (they're wired to `SITE_URL`).
- [ ] Submit the site to **Google Search Console** and **Bing Webmaster Tools**; submit `sitemap.xml`.
- [ ] Verify `robots.txt` allows crawling and points to the sitemap (it does, once `SITE_URL` is set).
- [ ] Consider a one-line description and a social preview image (the app icon works, or make an OG image).
- [ ] Because sub-"pages" are hash routes (`#/id`), they won't be separate search results — the content is still fully indexed on the main URL. If per-page SEO becomes a priority later, that's the trigger to move to a static-site generator with one file per page.

## 4. Analytics + feedback (know how it's used)

- **Privacy-friendly analytics** (no cookie banner needed): **Plausible**, **GoatCounter**,
  or **Cloudflare Web Analytics**. Add the one-line snippet before `</body>` in the template
  (add a `__ANALYTICS__` placeholder if you want it build-managed).
- **Feedback** is already wired: the footer "Report an issue" link uses `CONTACT_EMAIL`.
  Consider also a short form (Google Form / Tally) linked from the Disclaimer page for
  structured suggestions.
- Watch: most-visited pages, search terms (if your analytics captures them), and mock-exam
  usage — these tell you where to add depth and images first.

## 5. Announcement copy (edit to taste)

**Short (X / LinkedIn):**
> Launching the Nuclear Medicine Atlas — a free, evidence-graded reference for the whole
> field: every major tracer, protocol, disease, and therapy, plus interactive dosimetry
> tools, guided learning paths, and a timed board-style mock exam. Built for residents,
> attendings, and the therapy-driven future of the specialty. [URL] #NuclearMedicine #Theranostics

**Professional forum / listserv (SNMMI, program directors, residency lists):**
> Colleagues — I've built the Nuclear Medicine Atlas, a free, openly-accessible reference
> covering the field end to end (263 pages across 25 domains), with graded evidence and
> primary-source citations, interactive calculators (patient release, Y-90 activity, PRRT
> kidney BED, SUV, and more), guided learning paths for students/residents/boards, and a
> domain-weighted mock-exam engine. It's aimed squarely at board readiness and at the
> therapy transformation reshaping our specialty.
>
> It's a living resource and I'm actively seeking **named peer reviewers** and
> **contributors** — your section would be credited with an ORCID-linked profile. Feedback
> and corrections are welcome via the site. [URL]

**Residency program email:**
> For your residents: the Nuclear Medicine Atlas [URL] includes a structured core
> curriculum, a "Board Blitz" high-yield track, topic-labeled self-check questions, and a
> timed mock exam with a per-domain readiness breakdown — a free, self-contained study
> companion for ABNM/ABR prep.

## 6. First 90 days (suggested)

1. **Weeks 1–2:** host it; submit to search consoles; recruit the first reviewer cohort (therapy + oncology first).
2. **Weeks 3–8:** apply first-wave reviews; add the first real images to the highest-traffic pages; announce to one or two friendly channels.
3. **Weeks 9–12:** broader announcement (SNMMI/listservs/socials) once peer-reviewed pages carry named credit; open the contributor pipeline; set the maintenance cadence.
