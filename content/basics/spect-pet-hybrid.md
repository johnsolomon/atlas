---
type: physics
title: SPECT, PET & Hybrid Imaging
chapter: instrumentation
order: 50
subtitle: Reconstruction, attenuation and scatter correction, and hybrid SPECT/CT, PET/CT, PET/MR
aliases: [SPECT, PET, hybrid imaging, SPECT/CT, PET/CT, PET/MR, iterative reconstruction, OSEM, attenuation correction, scatter correction, time of flight, partial volume, PSF, resolution recovery]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "13 min"
tags: [hybrid-imaging, physics, basic-principles, PET, SPECT]
related_tracers: []
related_protocols: []
related_diseases: []
related_calculators: [suv]
related_pitfalls: [pearls-pitfalls]
---

## Quick Answer

**SPECT** reconstructs a 3D distribution from gamma-camera projections acquired around the patient; **PET** reconstructs from coincidence lines of response. Both require **attenuation** and **scatter correction** for quantitative accuracy — now supplied by the **CT** of hybrid scanners, which also adds anatomic localization. **PET/CT** is standard in oncology; **SPECT/CT** improves localization/characterization of equivocal foci; **PET/MR** adds soft-tissue contrast at lower radiation.

## Reconstruction

Modern systems use **iterative reconstruction** (e.g. **OSEM**) rather than filtered back-projection, incorporating models of system physics — **resolution recovery / point-spread-function (PSF)** modeling and, for PET, **TOF** — to improve signal-to-noise. Reconstruction settings **affect quantitation**, which is why **SUV** must be compared only across matched protocols.

## Corrections That Make Images Quantitative

- **Attenuation correction (AC):** photons are absorbed/scattered en route to the detector; the CT provides an **attenuation map**. **Misregistration** between CT and emission data (motion, respiration) creates classic artifacts (anterior/lateral cardiac defects).
- **Scatter correction:** removes mispositioned scattered photons that reduce contrast.
- **Partial-volume effect:** small structures (below ~**2–3× system resolution**) have **underestimated** activity — a key limit on small-lesion SUV.
- **Randoms/dead-time** (PET) and **decay/attenuation** corrections complete the quantitative chain.

## Hybrid Modalities

| Modality | Adds | Best-fit uses |
|---|---|---|
| **SPECT/CT** | Localization, AC, characterization | Bone SPECT/CT, parathyroid, DOTATATE/PSMA SPECT, cardiac-amyloid confirmation |
| **PET/CT** | AC + anatomy, whole-body | Oncologic FDG/PSMA/DOTATATE PET, cardiac PET |
| **PET/MR** | Soft-tissue contrast, lower dose | Pelvic/brain/pediatric imaging, research |

## The Corrections That Make Numbers Trustworthy

Attenuation and scatter correction are what turn a picture into a **quantitative** study; the hybrid **CT supplies the attenuation map *and* the anatomic overlay** in one step. Its predictable failure mode is **CT–emission misregistration** from motion/respiration — the classic cause of a spurious anterior/lateral cardiac "defect."

## Why SUV Is Not Portable

SUV depends on **reconstruction** (algorithm, iterations, PSF), **uptake time**, **glucose**, **cross-calibration**, and — for small lesions — the **partial-volume effect**. Compare SUV only within **matched protocols**, ideally the same scanner; use a **harmonized (EARL)** reconstruction for cross-site or serial quantitation (see the SUV-harmonization page).

## Choosing the Hybrid Modality

- **SPECT/CT** shines at localizing/characterizing equivocal foci (bone, parathyroid, DOTATATE/PSMA SPECT, cardiac-amyloid confirmation).
- **PET/CT** is the whole-body oncologic and cardiac-flow workhorse.
- **PET/MR** trades throughput for superior soft-tissue contrast and lower radiation (pelvic, brain, pediatric).

## Reporting / Practice Impact

- State the **reconstruction/AC method** and any **misregistration** limitation.
- Interpret small-lesion SUV with the **partial-volume** caveat.
- Use **SPECT/CT** to reclassify equivocal planar foci (frequently changes management).
- For serial/quantitative work, keep **technique constant** or use harmonized reconstruction.

## Common Pitfalls

- **CT/emission misregistration** artifacts from motion/respiration (classic on cardiac PET).
- Over-reading **small-lesion SUV** without accounting for partial-volume underestimation.
- Comparing **SUVs across different scanners/reconstructions** as if equivalent.
- Assuming an **AC-only** image is artifact-free — always review the **non-AC** images too (AC can introduce artifacts).

## Board Pearls

{K} Attenuation and scatter correction make images **quantitative**, and the hybrid CT does **double duty** (attenuation map + anatomic overlay). The predictable failure mode is **CT–emission misregistration** (motion/respiration) — the classic spurious anterior/lateral cardiac defect; always review **non-AC** images alongside AC.

{H} **SUV is protocol-dependent** (reconstruction/PSF, uptake time, glucose, cross-calibration) and, for small lesions, subject to the **partial-volume effect** (structures below ~2–3× resolution are underestimated). Compare like with like; use **EARL-harmonized** reconstruction across sites/serial scans.

{D} Choose the hybrid to the task: **SPECT/CT** for localizing/characterizing equivocal foci; **PET/CT** for whole-body oncology and cardiac flow; **PET/MR** for soft-tissue contrast and lower dose. **Iterative reconstruction (OSEM)** with **PSF/resolution recovery** and **TOF** improves signal-to-noise but also changes SUV — another reason quantitation must be protocol-matched.

## Related Pages

- Related: **Radiation detection & instrumentation**, **physics of nuclear medicine**, **SUV harmonization (EARL)**.
- Pitfalls: **Pearls, pitfalls & normal variants**; calculator: **SUV** tool.

## Figure / Diagram Suggestions

- An **iterative-reconstruction** loop schematic (forward/back projection with system model).
- A **misregistration artifact** teaching pair (AC vs non-AC cardiac images).
- A **hybrid-modality selector** (SPECT/CT vs PET/CT vs PET/MR by task).

## Self-Check (Board-Style)

<details><summary><strong>Q1.</strong> A cardiac PET shows an anterior defect only on the attenuation-corrected images; the non-AC images look normal. Likely cause?</summary>
<p><strong>Answer:</strong> <strong>CT–emission misregistration</strong> (motion/respiration) — an attenuation-correction artifact, not true disease. Always review non-AC images and re-align.</p>
</details>

<details><summary><strong>Q2.</strong> Why can a small lung nodule's SUV be misleadingly low?</summary>
<p><strong>Answer:</strong> The <strong>partial-volume effect</strong> — structures below ~2–3× the system resolution have <strong>underestimated</strong> activity/SUV.</p>
</details>

<details><summary><strong>Q3.</strong> When is it valid to compare SUV between two scans?</summary>
<p><strong>Answer:</strong> Only within <strong>matched protocols</strong> (reconstruction, uptake time, glucose, cross-calibration) — ideally the same scanner, or using an <strong>EARL-harmonized</strong> reconstruction for cross-site/serial comparison.</p>
</details>

<details><summary><strong>Q4.</strong> Which hybrid modality best characterizes an equivocal solitary rib focus on a bone scan?</summary>
<p><strong>Answer:</strong> <strong>SPECT/CT</strong> — it localizes and characterizes the focus (benign vs metastatic), frequently reclassifying equivocal planar findings.</p>
</details>
