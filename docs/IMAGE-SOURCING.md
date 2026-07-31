# Image-Sourcing Guide

The atlas's diagrams are all **original vector schematics** (copyright-clean by
construction). What it lacks — and what an *imaging* atlas ultimately needs — is **real
scan images**: normal-template galleries and classic pathology for bone scans, PET/CT,
V/Q, DaTscan, PSMA/DOTATATE, MPI, thyroid, HIDA, and more. This guide lists **only
genuinely reusable** sources and exactly how to add images to a page.

> **Golden rule:** only use images with an explicit open license (public domain / CC0 /
> CC BY) or that you own and have de-identified with appropriate consent. Never use images
> from Google Images, textbooks, journal figures that aren't open-access, Radiopaedia
> non-free cases, or "found on the web" — a single copyrighted image undermines the whole
> resource's credibility and exposes you legally.

---

## How to add an image to a page

The build already supports per-page images via front-matter. In any `content/**/*.md`
file, add a `figures:` list; each entry is `{src, caption, credit, alt}`:

```yaml
figures:
  - src: /img/bone-superscan.jpg
    alt: Whole-body Tc-99m-MDP bone scan showing diffusely increased skeletal uptake with faint kidneys
    caption: Superscan — diffuse skeletal uptake with the "absent kidney sign" in extensive prostate metastases.
    credit: Wikimedia Commons, CC BY-SA 4.0 (author, link)
```

- **`src`** — put image files under a `/img/` folder at your site root (or use an absolute
  URL). Rebuild after adding.
- **`alt`** — required for accessibility; describe the finding, not just "bone scan."
- **`caption`** — the teaching point.
- **`credit`** — **always** record the source and license; it renders under the figure.
  This is both an attribution obligation and your audit trail.

Images render in the same numbered figure system as the vector diagrams, with the click-to-zoom lightbox.

**Keep a license ledger.** For every image, log source URL, author, license, and date
retrieved (a simple spreadsheet). If you ever need to prove provenance, you'll have it.

---

## Vetted sources (check each file's license individually)

**Public domain / CC0 — safest, reuse freely:**
- **Wikimedia Commons** (commons.wikimedia.org) — search "bone scan", "PET CT", "V/Q scan",
  "DaTSCAN", "thyroid scintigraphy". Each file page states its license (many are CC BY-SA,
  some CC0/PD). Use the license shown; attribute per that license.
- **NIH / NCI Visuals Online** and other **U.S. federal-government** works — generally
  public domain (confirm on the item page).
- **Wikipedia** medical articles — images are hosted on Commons; use the Commons license.

**Open-access literature figures (attribution required; check the specific CC variant):**
- **PMC Open Access Subset** (ncbi.nlm.nih.gov/pmc) — filter to the *Open Access* subset,
  then to **CC BY** or **CC0** articles; figures in those may be reused with attribution.
  Avoid **CC BY-NC** if the atlas may ever be commercial, and **CC BY-SA/ND** if share-alike
  or no-derivatives is a problem.
- **Open-i** (openi.nlm.nih.gov, NLM biomedical image search) — filterable by license; images
  come from PMC and other collections with **mixed** licenses, so verify each one.

**Raw imaging datasets you can render yourself (often CC BY):**
- **The Cancer Imaging Archive — TCIA** (cancerimagingarchive.net) — de-identified DICOM
  collections, many under **CC BY**. You can render representative PET/CT/SPECT slices from
  these and attribute the collection (great for *normal-template* and oncology examples).

**Your own / departmental teaching files:**
- The cleanest source: your own de-identified cases with appropriate institutional/patient
  consent. **Strip all PHI** — remove DICOM headers, burned-in names/MRNs, and any
  identifying annotations before use.

**Use with caution (read the license first):**
- **Radiopaedia** — most cases are **CC BY-NC-SA 3.0**: non-commercial only, attribution,
  and share-alike (which can force your whole resource to the same license). Only use if you
  are certain the atlas will remain non-commercial and you accept share-alike, and attribute exactly.

---

## De-identification checklist (for any patient image)

1. Remove DICOM metadata / EXIF (patient name, MRN, DOB, accession, institution, dates).
2. Remove burned-in text annotations that identify the patient.
3. Crop out wristbands, faces, or any identifiers in photographs.
4. Confirm consent/IRB status per your institution's policy for teaching/publication use.

---

## First-wave image wishlist (highest teaching value)

Prioritize normal templates + the classic "must-recognize" patterns already described in the atlas:

- **Bone:** normal whole-body MDP; superscan; multiple metastases; flare; photopenic (cold) lesion; three-phase osteomyelitis.
- **Oncology PET:** normal FDG biodistribution; nodal/distant metastatic FDG; brown-fat & physiologic uptake mimics; Deauville examples.
- **Cardiac:** normal MPI (SPECT bullseye); reversible vs fixed defect; Tc-PYP grade 2–3 cardiac amyloid.
- **Pulmonary:** normal V/Q; segmental mismatch (high-probability PE).
- **Neuro:** normal DaTscan "comma" vs putaminal loss; FDG dementia patterns.
- **Endocrine/therapy:** normal thyroid uptake/scan; Graves vs thyroiditis; PSMA-avid prostate; DOTATATE-avid NET (theranostic pairs).
- **GI:** normal HIDA; non-visualization (acute cholecystitis); Meckel/GI-bleed.

Each new image should carry a precise `alt`, a teaching `caption`, and a full `credit`.
Add them a few at a time and rebuild — the figure system handles the rest.
