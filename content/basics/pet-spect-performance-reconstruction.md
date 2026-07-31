---
type: physics
title: PET & SPECT Performance & Reconstruction
chapter: instrumentation
order: 30
subtitle: Resolution limits, coincidence physics, NECR, and iterative reconstruction — the working layer
aliases: [spatial resolution, FWHM, positron range, noncollinearity, coincidence, true scatter random, NECR, sensitivity, TOF, time of flight, iterative reconstruction, OSEM, PSF, resolution recovery, attenuation correction, scatter correction, partial volume, recovery coefficient, NEMA]
review_status: physician-reviewed
last_updated: 2026-07-27
reading_time: "16 min"
tags: [instrumentation, hybrid-imaging, physics, PET, SPECT]
related_tracers: []
related_diseases: []
related_therapies: []
related_calculators: []
related_pitfalls: [pearls-pitfalls]
---

## Quick Answer

**SPECT** resolution is limited chiefly by the **collimator** (resolution degrades with source-to-collimator distance) and combines with intrinsic detector resolution in quadrature. **PET** needs no physical collimator (coincidence detection) but is bounded by **positron range**, **photon non-collinearity**, and **detector element size**; its signal is the **true** coincidences against **scatter** and **randoms**, summarized by the **noise-equivalent count rate (NECR)**. **Iterative reconstruction (OSEM)** with **PSF** and **time-of-flight (TOF)** modeling, plus **attenuation/scatter/partial-volume** corrections, turn raw data into quantitative images.

## SPECT — Resolution & Sensitivity

**System resolution** combines detector (intrinsic) and collimator (geometric) terms in quadrature:

**R_system = √(R_intrinsic² + R_collimator²)**

- The **collimator dominates** and **degrades with distance** from the collimator face — so keep the detector close to the patient.
- **Resolution–sensitivity trade-off:** high-resolution collimators accept fewer photons (lower sensitivity); high-sensitivity collimators blur. A **converging (fan/cone)** collimator or **CZT/dedicated cardiac** geometry can improve one without fully sacrificing the other.
- **Pinhole** collimation magnifies for high-resolution small-organ imaging (thyroid, parathyroid, small-animal).

## PET — Intrinsic Resolution Limits

Even with electronic collimation, PET resolution is bounded by physics:

| Factor | Effect |
|---|---|
| **Positron range** | Positron travels before annihilation — larger for high-energy emitters (Rb-82, Ga-68) than F-18 |
| **Photon non-collinearity** | The two 511-keV photons are ~**0.5°** off 180°, blurring by an amount that **grows with detector-ring diameter** (~½ FWHM contribution at ~80 cm) |
| **Detector element size** | Contributes ~**(element size)/2** to intrinsic resolution |
| **Depth-of-interaction** | Parallax blurring off-center in the field |

These set a practical whole-body PET resolution around a few millimeters — the floor beneath which no reconstruction can recover true detail.

## PET — Coincidences: True, Scatter, Random

- **True coincidence:** both photons from one annihilation, unscattered — the signal.
- **Scatter coincidence:** one/both photons Compton-scattered — mispositioned; removed by **scatter correction**.
- **Random (accidental) coincidence:** two photons from **different** annihilations within the timing window — increase with the **square of activity**; corrected by the **delayed-window** technique.
- **Noise-equivalent count rate (NECR)** = T²/(T + S + R) — the effective signal-to-noise metric that **peaks then falls** as activity rises (randoms/dead-time dominate at high activity), guiding optimal injected activity.

## Time-of-Flight (TOF)

Fast detectors measure the **arrival-time difference** of the two photons and localize the annihilation **along the line of response**, narrowing the probable position. TOF **improves signal-to-noise** (effective sensitivity gain that scales with patient size) — most valuable in **larger patients**.

## Image Reconstruction

- **Filtered back-projection (FBP):** fast, linear, but streak-artifact-prone and noisy — largely historical for clinical use.
- **Iterative (OSEM):** models the acquisition (system matrix) and iterates toward the image; **subsets × iterations** trade convergence against noise. Incorporates:
  - **PSF / resolution recovery** — models spatially varying blur (sharper images; can introduce edge "Gibbs" overshoot and change SUV).
  - **TOF** (PET) — improves SNR/convergence.
- Reconstruction settings **change SUV**, so quantitative comparison requires **matched reconstruction** (or an EARL-harmonized reconstruction).

## Quantitative Corrections

| Correction | Purpose | Failure mode |
|---|---|---|
| **Attenuation (CT map)** | Recover photons absorbed en route | **CT–emission misregistration** → false cardiac defects |
| **Scatter** | Remove mispositioned scattered photons | Loss of contrast if uncorrected |
| **Randoms (PET)** | Subtract accidental coincidences | Elevated background at high activity |
| **Dead time** | Correct count-rate losses | Underestimation at high rates |
| **Partial-volume** | Recover activity in small structures | Small-lesion SUV **underestimated** (recovery coefficient < 1 below ~2–3× resolution) |

## The Partial-Volume Effect & Recovery Coefficient

Structures smaller than **~2–3× the system resolution (FWHM)** have their activity **underestimated** (spill-out) and background **overestimated** (spill-in). The **recovery coefficient** (measured/true activity) falls below 1 as size decreases — the physical reason a small avid nodule can show a falsely low SUV, and a caution in serial small-lesion quantitation.

## NEMA Performance Standards

**NEMA NU-2 (PET)** and **NU-1 (SPECT)** standardize measurement of **spatial resolution, sensitivity, scatter fraction, NECR, count-rate performance, and image quality**, enabling scanner comparison and acceptance testing.

## Board-Level Synthesis

{K} **SPECT** resolution is collimator-limited and **degrades with distance** — combine intrinsic and collimator terms in quadrature and keep the detector close. **PET** floor is set by **positron range**, **non-collinearity** (~0.5°, worse at larger ring diameter), and **detector element size** — no reconstruction recovers detail below it.

{H} PET signal is **true coincidences** against **scatter** and **randoms** (randoms ∝ activity²); **NECR = T²/(T+S+R)** peaks then falls with activity, guiding optimal dose. **TOF** localizes the annihilation along the line of response, improving SNR most in **larger patients**.

{D} **Iterative reconstruction (OSEM)** with **PSF/resolution recovery** and **TOF** — plus **attenuation/scatter/randoms/partial-volume** corrections — makes images quantitative, but **changes SUV**, so serial comparison needs matched (or EARL-harmonized) reconstruction. The **partial-volume effect** underestimates SUV in structures below **~2–3× FWHM** (recovery coefficient < 1) — the physics behind falsely low small-lesion SUV and the CT–emission **misregistration** artifact behind spurious cardiac defects.

## Related Pages

- Physics: **Radiation detection & instrumentation**, **SPECT/PET & hybrid imaging**, **physics of nuclear medicine** (positron range).
- Reference: **SUV harmonization (EARL)**; pitfalls: **Pearls, pitfalls & normal variants**.

## Figure / Diagram Suggestions

- A **PET resolution-budget** diagram (positron range + non-collinearity + detector size).
- A **NECR curve** (true/scatter/random vs activity).
- A **recovery-coefficient** curve (SUV recovery vs lesion size / FWHM).

## Self-Check

<details><summary><strong>Q1.</strong> Why does SPECT resolution worsen as the patient is farther from the collimator?</summary>
<p><strong>Answer:</strong> The <strong>collimator geometric resolution degrades with source-to-collimator distance</strong> and dominates system resolution — so the detector should be kept as close to the patient as possible.</p>
</details>

<details><summary><strong>Q2.</strong> Name the three physical factors limiting PET spatial resolution.</summary>
<p><strong>Answer:</strong> <strong>Positron range</strong>, photon <strong>non-collinearity</strong> (~0.5°, worse with larger ring diameter), and <strong>detector element size</strong> (plus depth-of-interaction/parallax).</p>
</details>

<details><summary><strong>Q3.</strong> What is NECR and why does it matter for injected activity?</summary>
<p><strong>Answer:</strong> <strong>Noise-equivalent count rate</strong> = T²/(T+S+R); it <strong>peaks then falls</strong> as activity rises (randoms/dead-time), identifying the activity that optimizes effective signal-to-noise.</p>
</details>

<details><summary><strong>Q4.</strong> Below what size are lesion SUVs underestimated, and what quantity describes this?</summary>
<p><strong>Answer:</strong> Below roughly <strong>2–3× the system resolution (FWHM)</strong>, due to the <strong>partial-volume effect</strong>; the <strong>recovery coefficient</strong> (measured/true) falls below 1.</p>
</details>
