---
type: physics
title: SUV Harmonization & EARL
chapter: instrumentation
order: 60
subtitle: Making SUV comparable across scanners, sites, and time
aliases: [SUV harmonization, EARL, EANM Research Ltd accreditation, quantitative PET, multicenter SUV, reconstruction harmonization, comparability, PSF, SUVpeak, PERCIST reference]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "10 min"
tags: [hybrid-imaging, physics, quantitation, PET]
related_tracers: [fdg]
related_diseases: []
related_therapies: []
---

## Quick Answer

**SUV** (standardized uptake value = tissue activity concentration ÷ injected activity/body weight) is only meaningful compared **like-with-like**, yet it varies with **scanner, reconstruction, uptake time, glucose, and calibration**. **Harmonization** — most formally through **EARL (EANM Research Ltd) accreditation** — standardizes acquisition and reconstruction so SUV is comparable across scanners, sites, and serial studies. This underpins **response assessment (PERCIST)**, multicenter trials, and any quantitative/AI use of SUV. The operational rule: never attribute an SUV change to biology when it may be a **reconstruction or protocol difference**.

## Why SUV Drifts

- **Reconstruction** — algorithm, iterations/subsets, post-filter, resolution recovery, and **point-spread-function (PSF)** modeling all change SUVmax substantially (sharper reconstructions **raise** SUVmax).
- **Uptake time** — FDG SUV rises over ~60–90 min; a 10-min timing difference shifts values.
- **Blood glucose** and **injected-activity/weight accuracy** (extravasation, residual in syringe, clock errors).
- **Scanner cross-calibration** with the dose calibrator must be current.
- **Partial-volume effect** underestimates small-lesion SUV; **SUVpeak** (a fixed ~1-cm³ volume) is more reproducible than the single-voxel **SUVmax**.

## The Metrics

| Metric | Definition | Property |
|---|---|---|
| SUVmax | Single hottest voxel | Sensitive, but noisy/reconstruction-dependent |
| SUVpeak | ~1 cm³ around the hottest region | More reproducible; PERCIST uses SULpeak |
| SUVmean | Average over a VOI | Depends on segmentation threshold |
| SUL (lean) | SUV normalized to **lean body mass** | Reduces body-composition bias; used in PERCIST |

## Harmonization in Practice

- **EARL** defines **phantom-based (NEMA image-quality) performance limits** and reconstruction settings; accredited sites produce comparable SUVs. Many sites run a **harmonized (EARL-compliant) reconstruction alongside** their sharpest clinical reconstruction — the sharp one for detection, the harmonized one for quantification.
- For **response assessment**, hold technique constant across a patient's serial scans — ideally the **same scanner and protocol** — and use a consistent reference region (**liver** for PERCIST, with blood pool as backup).
- Newer **PSF/ultra-high-resolution** reconstructions **raise SUV**, so a harmonized series is used specifically for quantitative comparison; EARL2 standards accommodate PSF-era scanners.

## Worked Point

A lesion reads **SUVmax 8.0** on an old OSEM reconstruction and **11.0** on a new PSF reconstruction of the *same* acquisition. That +38% is **pure reconstruction**, not tumor progression — comparing them as if equivalent would falsely call progressive disease. Compare the **harmonized-to-harmonized** series instead.

## Reporting Checklist

- State the **reconstruction** used (and whether a harmonized reconstruction was applied for quantitation).
- Report the **metric** (SUVmax vs SUVpeak/SUL) and the **reference region**.
- For serial studies, confirm **same scanner/protocol/uptake time**; flag any change.

## Common Pitfalls

- Attributing an SUV change to **biology** when it reflects a **reconstruction/protocol** difference.
- Comparing a **PSF/sharp** reconstruction to an older **harmonized** one.
- Ignoring **partial-volume** underestimation in small lesions.
- Uncorrected **extravasation** or timing errors inflating apparent change.

## Board Pearls

{K} SUV is only meaningful compared **like-with-like**, yet it drifts with **scanner, reconstruction (PSF/iterations/filter), uptake time, glucose, and calibration**. **Harmonization** — formally via **EARL accreditation** — standardizes acquisition/reconstruction so SUV is comparable across scanners, sites, and serial studies (many sites run a **harmonized reconstruction alongside** their sharpest clinical one). For **response assessment (PERCIST)**, hold technique constant and use a consistent **liver** reference.

{H} **Sharper reconstructions raise SUVmax** — a PSF series can read 30–40% higher than OSEM on the *same* data, mimicking progression. **SUVpeak/SUL** are more reproducible than the noisy single-voxel **SUVmax**, and **PERCIST uses SULpeak** normalized to lean body mass with a liver reference.

{D} Keep the drift sources straight: **reconstruction and uptake time** dominate, **partial-volume** underestimates small lesions, and **cross-calibration/extravasation** silently bias values. Never attribute an SUV change to biology when it may be a **protocol difference** — the whole point of EARL is to remove that ambiguity for multicenter and longitudinal work.

## Related Pages

- Tracer: **FDG**; reporting: **oncology response criteria (RECIST/PERCIST)**; physics: **PET/SPECT performance & reconstruction**.

## Figure / Diagram Suggestions

- A **same-data, two-reconstruction** SUV comparison (OSEM vs PSF) showing the artifactual rise.
- A **drift-source** fishbone (reconstruction, timing, glucose, calibration, partial volume).

## Self-Check

<details><summary><strong>Q1.</strong> A lesion's SUVmax rises from 8 to 11 after the site switches to a PSF reconstruction of the same scan. Is this progression?</summary>
<p><strong>Answer:</strong> <strong>No</strong> — sharper (PSF) reconstructions <strong>raise SUVmax</strong>; this is a reconstruction artifact, not biology. Compare harmonized-to-harmonized series.</p>
</details>

<details><summary><strong>Q2.</strong> Why is SUVpeak/SUL preferred over SUVmax for response assessment?</summary>
<p><strong>Answer:</strong> <strong>SUVpeak</strong> (a ~1-cm³ region) is <strong>more reproducible</strong> than the noisy single-voxel SUVmax; <strong>SUL</strong> normalizes to lean body mass, reducing body-composition bias (PERCIST uses SULpeak).</p>
</details>

<details><summary><strong>Q3.</strong> What does EARL accreditation standardize, and how is it verified?</summary>
<p><strong>Answer:</strong> It standardizes <strong>acquisition and reconstruction</strong> to defined <strong>phantom-based (NEMA) performance limits</strong>, so accredited sites produce comparable SUVs.</p>
</details>

<details><summary><strong>Q4.</strong> Which reference region does PERCIST use, and why hold technique constant across serial scans?</summary>
<p><strong>Answer:</strong> The <strong>liver</strong> (blood pool as backup); holding scanner/protocol/uptake time constant ensures an SUV change reflects <strong>biology, not technique</strong>.</p>
</details>
